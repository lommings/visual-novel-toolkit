#!/usr/bin/env python3
"""
Monogatari 匯出器
將故事轉換為 twine-monogatari 格式
"""

import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional


class MonogatariExporter:
    """將故事匯出為 twine-monogatari 格式"""
    
    def __init__(self, assets_dir: Path, assets_data: Dict):
        self.assets_dir = assets_dir
        self.assets_data = assets_data
    
    def generate_characters_passage(self) -> str:
        """生成 [Characters] 段落"""
        characters = {}
        
        for char in self.assets_data.get('characters', []):
            char_id = char['id']
            char_name = char.get('name', char_id)
            
            # 收集表情圖片
            char_dir = self.assets_dir / 'characters' / char_id
            images = {}
            
            for expr in ['normal', 'happy', 'sad', 'angry', 'surprised']:
                img_path = char_dir / f'{expr}.png'
                if img_path.exists():
                    images[expr.capitalize()] = f'{expr}.png'
            
            # 如果有 base.png，用作 Normal
            base_path = char_dir / 'base.png'
            if base_path.exists() and 'Normal' not in images:
                images['Normal'] = 'base.png'
            
            characters[char_id] = {
                'Name': char_name,
                'Color': self._get_char_color(char_id),
                'Directory': char_id,
                'Images': images
            }
        
        # 加入旁白
        characters['narrator'] = {
            'Name': '',
            'Color': '#ffffff'
        }
        
        yaml_content = yaml.dump(characters, allow_unicode=True, default_flow_style=False)
        return f":: [Characters]\n{yaml_content}"
    
    def _get_char_color(self, char_id: str) -> str:
        """根據角色 ID 分配顏色"""
        colors = {
            'kazuya': '#8b5cf6',  # 紫色
            'aiba': '#22c55e',    # 綠色
        }
        return colors.get(char_id, '#ffffff')
    
    def generate_scenes_passage(self) -> str:
        """生成 [Scenes] 段落"""
        scenes = {}
        
        for scene in self.assets_data.get('scenes', []):
            scene_id = scene['id']
            
            # 檢查場景圖片
            scene_dir = self.assets_dir / 'scenes' / scene_id
            bg_path = scene_dir / 'background.png'
            
            if bg_path.exists():
                scenes[scene_id] = f'scenes/{scene_id}/background.png'
            else:
                # 檢查其他可能的路徑
                for ext in ['.png', '.jpg']:
                    alt_path = self.assets_dir / 'scenes' / f'{scene_id}{ext}'
                    if alt_path.exists():
                        scenes[scene_id] = f'scenes/{scene_id}{ext}'
                        break
        
        yaml_content = yaml.dump(scenes, allow_unicode=True, default_flow_style=False)
        return f":: [Scenes]\n{yaml_content}"
    
    def generate_settings_passage(self, assets_url: str) -> str:
        """生成 [Settings] 段落"""
        settings = {
            'AssetsPath': {
                'root': assets_url
            },
            'Name': self.assets_data.get('title', 'Visual Novel'),
            'Version': '1.0.0'
        }
        
        yaml_content = yaml.dump(settings, allow_unicode=True, default_flow_style=False)
        return f":: [Settings]\n{yaml_content}"
    
    def convert_passage(self, name: str, scene_id: Optional[str], 
                       text: str, choices: List[Dict],
                       characters_in_scene: List[str] = None) -> str:
        """轉換段落為 Monogatari 格式"""
        lines = []
        
        # 場景切換
        if scene_id:
            lines.append(f"show scene {scene_id} fadeIn")
        
        # 顯示角色（如果有指定）
        if characters_in_scene:
            for char_id in characters_in_scene:
                lines.append(f"show character {char_id} Normal center fadeIn")
        
        # 處理文字內容
        # 分割成句子
        sentences = self._split_sentences(text)
        
        for sentence in sentences:
            if sentence.strip():
                # 嘗試識別說話者
                speaker, dialogue = self._parse_dialogue(sentence)
                if speaker:
                    lines.append(f'{speaker} {dialogue}')
                else:
                    lines.append(f'narrator {sentence}')
        
        # 加入選項
        if choices:
            for choice in choices:
                choice_text = choice.get('text', '')
                target = choice.get('target', '')
                lines.append(f'[[{choice_text}->{target}]]')
        
        content = '\n'.join(lines)
        return f":: {name}\n{content}"
    
    def _split_sentences(self, text: str) -> List[str]:
        """分割文字為句子"""
        # 用中文標點符號分割
        sentences = re.split(r'([。！？])', text)
        
        # 重新組合（保留標點）
        result = []
        for i in range(0, len(sentences)-1, 2):
            if i+1 < len(sentences):
                result.append(sentences[i] + sentences[i+1])
            else:
                result.append(sentences[i])
        
        return [s.strip() for s in result if s.strip()]
    
    def _parse_dialogue(self, text: str) -> tuple:
        """解析對話，嘗試識別說話者"""
        # 匹配引號內的對話
        # 格式：「對話內容」或 "對話內容"
        patterns = [
            r'「(.+?)」',
            r'「(.+?)」',
            r'"(.+?)"',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                dialogue = match.group(1)
                # 檢查前面是否有角色名
                before = text[:match.start()]
                
                # 嘗試識別角色
                if '和也' in before or '他低聲' in before or '他說' in before:
                    return ('kazuya', dialogue)
                elif '相葉' in before or '她說' in before:
                    return ('aiba', dialogue)
                
                return (None, dialogue)
        
        return (None, None)


def convert_to_monogatari(
    twee_path: Path,
    scene_mapping: Dict[str, str],
    assets_dir: Path,
    assets_data: Dict,
    output_path: Path,
    assets_url: str = './assets'
):
    """將 Twee 轉換為 twine-monogatari 格式"""
    
    exporter = MonogatariExporter(assets_dir, assets_data)
    
    # 讀取原始 Twee
    content = twee_path.read_text(encoding='utf-8')
    
    # 提取標題
    title_match = re.search(r':: StoryTitle\r?\n(.+?)(?=\r?\n::|\Z)', content, re.DOTALL)
    title = title_match.group(1).strip() if title_match else "Visual Novel"
    
    # 生成特殊段落
    output_parts = []
    output_parts.append(f":: StoryTitle\n{title}")
    
    # StoryData - 使用 twine-monogatari 格式
    story_data = {
        "ifid": "AUTO-GENERATED",
        "format": "twine-monogatari",
        "format-version": "0.2.0",
        "start": "Start"
    }
    output_parts.append(f":: StoryData\n{json.dumps(story_data, indent=2)}")
    
    # 加入 Monogatari 特殊段落
    output_parts.append(exporter.generate_settings_passage(assets_url))
    output_parts.append(exporter.generate_characters_passage())
    output_parts.append(exporter.generate_scenes_passage())
    
    # 轉換故事段落
    pattern = r':: (\w+)\r?\n(.*?)(?=\r?\n:: |\Z)'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for name, body in matches:
        if name in ['StoryTitle', 'StoryData']:
            continue
        
        # 提取場景代碼
        scene_match = re.search(r'\{\s*/\*\s*scene:\s*(\w+)\s*\*/\s*\}', body)
        scene_code = scene_match.group(1) if scene_match else None
        scene_id = scene_mapping.get(scene_code) if scene_code else None
        
        # 移除場景標記
        clean_body = re.sub(r'\{\s*/\*\s*scene:\s*\w+\s*\*/\s*\}\r?\n?', '', body).strip()
        
        # 提取選項
        choices = []
        choice_matches = re.findall(r'\[\[(.+?)->(\w+)\]\]', clean_body)
        for choice_text, target in choice_matches:
            choices.append({'text': choice_text, 'target': target})
        
        # 移除選項後的純文字
        text = re.sub(r'\[\[.+?->\w+\]\]', '', clean_body).strip()
        
        # 轉換段落
        passage = exporter.convert_passage(name, scene_id, text, choices)
        output_parts.append(passage)
    
    # 寫入輸出
    output_content = '\n\n'.join(output_parts)
    output_path.write_text(output_content, encoding='utf-8')
    
    print(f"[Done] Monogatari Twee saved: {output_path}")
    return output_path


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert to twine-monogatari format')
    parser.add_argument('twee_path', help='Original Twee file')
    parser.add_argument('scene_mapping', help='Scene mapping JSON')
    parser.add_argument('assets_dir', help='Assets directory')
    parser.add_argument('assets_json', help='assets-needed.json')
    parser.add_argument('-o', '--output', required=True, help='Output Twee file')
    parser.add_argument('--assets-url', default='./assets', help='Assets URL for Monogatari')
    
    args = parser.parse_args()
    
    # 載入場景對應
    with open(args.scene_mapping, 'r', encoding='utf-8') as f:
        scene_mapping = json.load(f)
    
    # 載入素材資料
    with open(args.assets_json, 'r', encoding='utf-8') as f:
        assets_data = json.load(f)
    
    convert_to_monogatari(
        Path(args.twee_path),
        scene_mapping,
        Path(args.assets_dir),
        assets_data,
        Path(args.output),
        args.assets_url
    )


if __name__ == '__main__':
    main()
