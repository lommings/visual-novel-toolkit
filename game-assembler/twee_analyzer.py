#!/usr/bin/env python3
"""
Twee 故事分析器
分析 Twee 檔案，產生場景對應和對話標記
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional
import sys

# 加入 shared 模組路徑
sys.path.insert(0, str(Path(__file__).parent.parent))
from shared.config_manager import ConfigManager
from shared.ai_client import AIClient


class TweeAnalyzer:
    """分析 Twee 故事檔"""
    
    def __init__(self, config: ConfigManager):
        self.config = config
        # AIClient 需要 dict 格式的 config
        self.ai = AIClient(config.config if hasattr(config, 'config') else config)
    
    def parse_twee(self, twee_path: Path) -> Dict:
        """解析 Twee 檔案，提取段落和場景標記"""
        content = twee_path.read_text(encoding='utf-8')
        
        # 提取 StoryTitle
        title_match = re.search(r':: StoryTitle\r?\n(.+?)(?=\r?\n::|\Z)', content, re.DOTALL)
        title = title_match.group(1).strip() if title_match else "Untitled"
        
        # 提取所有段落
        passages = {}
        # 匹配 :: PassageName 到下一個 :: 之間的內容
        pattern = r':: (\w+)\r?\n(.*?)(?=\r?\n:: |\Z)'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for name, body in matches:
            if name in ['StoryTitle', 'StoryData']:
                continue
                
            # 提取場景標記
            scene_match = re.search(r'\{\s*/\*\s*scene:\s*(\w+)\s*\*/\s*\}', body)
            scene_code = scene_match.group(1) if scene_match else None
            
            # 移除場景標記後的內容
            clean_body = re.sub(r'\{\s*/\*\s*scene:\s*\w+\s*\*/\s*\}\r?\n?', '', body).strip()
            
            # 提取選項
            choices = re.findall(r'\[\[(.+?)->(\w+)\]\]', clean_body)
            
            # 移除選項後的純文字
            text = re.sub(r'\[\[.+?->\w+\]\]', '', clean_body).strip()
            
            passages[name] = {
                'scene_code': scene_code,
                'text': text,
                'choices': [{'text': c[0], 'target': c[1]} for c in choices]
            }
        
        return {
            'title': title,
            'passages': passages
        }
    
    def create_scene_mapping_prompt(self, passages: Dict, available_scenes: List[Dict]) -> str:
        """建立場景對應的 AI prompt"""
        scene_list = "\n".join([
            f"- {s['id']}: {s['name']} - {s['description'][:50]}..."
            for s in available_scenes
        ])
        
        passage_info = []
        for name, data in passages.items():
            if data['scene_code']:
                text_preview = data['text'][:100] + "..." if len(data['text']) > 100 else data['text']
                passage_info.append(f"{data['scene_code']} ({name}): {text_preview}")
        
        return f"""請根據故事段落內容，將場景代碼對應到實際場景 ID。

可用的場景 ID：
{scene_list}

故事段落（場景代碼 -> 段落名稱: 內容預覽）：
{chr(10).join(passage_info[:20])}

請以 JSON 格式回覆場景對應，格式如下：
{{
  "S01": "場景ID",
  "S02": "場景ID",
  ...
}}

注意：
1. 多個場景代碼可以對應同一個場景 ID（例如多個段落發生在同一地點）
2. 如果找不到適合的場景，使用最接近的
3. 只回覆 JSON，不要其他文字"""

    def analyze_dialogue_prompt(self, passage_name: str, text: str, characters: List[Dict]) -> str:
        """建立對話分析的 AI prompt"""
        char_info = "\n".join([f"- {c['id']}: {c['name']}" for c in characters])
        
        return f"""分析以下視覺小說段落，標記說話者和表情。

角色清單：
{char_info}
- narrator: 旁白（無人說話時）

段落名稱：{passage_name}
段落內容：
{text}

請將文字分割成多個區塊，每個區塊標記說話者和表情。
表情選項：normal, happy, sad, angry, surprised

以 JSON 陣列格式回覆：
[
  {{"speaker": "narrator", "expression": null, "text": "旁白文字..."}},
  {{"speaker": "角色id", "expression": "表情", "text": "對話或動作描述..."}}
]

注意：
1. 用引號括起來的對話，識別說話者
2. 根據上下文推斷表情
3. 不要改動原文，只做分割和標記
4. 只回覆 JSON 陣列"""

    def generate_scene_mapping(self, twee_data: Dict, assets_data: Dict) -> Dict[str, str]:
        """使用 AI 生成場景對應表"""
        prompt = self.create_scene_mapping_prompt(
            twee_data['passages'],
            assets_data.get('scenes', [])
        )
        
        response = self.ai.generate_text(prompt)
        
        # 解析 JSON 回應
        try:
            # 嘗試提取 JSON
            json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
        
        return {}
    
    def analyze_dialogues(self, twee_data: Dict, characters: List[Dict], 
                         limit: int = None) -> Dict[str, List[Dict]]:
        """分析所有段落的對話"""
        results = {}
        passages = list(twee_data['passages'].items())
        
        if limit:
            passages = passages[:limit]
        
        for name, data in passages:
            if not data['text']:
                continue
                
            prompt = self.analyze_dialogue_prompt(name, data['text'], characters)
            
            try:
                response = self.ai.generate_text(prompt)
                
                # 解析 JSON 回應
                json_match = re.search(r'\[.*\]', response, re.DOTALL)
                if json_match:
                    results[name] = json.loads(json_match.group())
            except Exception as e:
                print(f"分析 {name} 失敗: {e}")
                results[name] = [{"speaker": "narrator", "expression": None, "text": data['text']}]
        
        return results


def main():
    """主程式"""
    import argparse
    
    parser = argparse.ArgumentParser(description='分析 Twee 故事檔')
    parser.add_argument('twee_path', help='Twee 檔案路徑')
    parser.add_argument('assets_json', help='assets-needed.json 路徑')
    parser.add_argument('-o', '--output', help='輸出目錄', default=None)
    parser.add_argument('--scene-only', action='store_true', help='只生成場景對應')
    parser.add_argument('--dialogue-limit', type=int, help='限制分析的段落數量')
    
    args = parser.parse_args()
    
    # 載入設定
    config = ConfigManager.load()
    analyzer = TweeAnalyzer(config)
    
    # 解析 Twee
    twee_path = Path(args.twee_path)
    twee_data = analyzer.parse_twee(twee_path)
    print(f"[Twee] {twee_data['title']}")
    print(f"  Passages: {len(twee_data['passages'])}")
    
    # 載入素材資料
    assets_path = Path(args.assets_json)
    with open(assets_path, 'r', encoding='utf-8') as f:
        assets_data = json.load(f)
    
    # 決定輸出目錄
    output_dir = Path(args.output) if args.output else twee_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成場景對應
    print("\n[AI] Generating scene mapping...")
    scene_mapping = analyzer.generate_scene_mapping(twee_data, assets_data)
    
    mapping_path = output_dir / 'scene-mapping.json'
    with open(mapping_path, 'w', encoding='utf-8') as f:
        json.dump(scene_mapping, f, ensure_ascii=False, indent=2)
    print(f"  Saved: {mapping_path}")
    
    if not args.scene_only:
        # 分析對話
        print("\n[AI] Analyzing dialogues...")
        dialogues = analyzer.analyze_dialogues(
            twee_data, 
            assets_data.get('characters', []),
            limit=args.dialogue_limit
        )
        
        dialogue_path = output_dir / 'dialogue-markers.json'
        with open(dialogue_path, 'w', encoding='utf-8') as f:
            json.dump(dialogues, f, ensure_ascii=False, indent=2)
        print(f"  Saved: {dialogue_path}")
    
    print("\n[Done] Analysis complete!")


if __name__ == '__main__':
    main()
