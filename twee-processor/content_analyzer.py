#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""內容分析器 - 分析角色、場景、對話"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Optional, Set

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.ai_client import AIClient
from shared.models import Character, Scene


class ContentAnalyzer:
    """內容分析器"""
    
    # 對話模式
    DIALOGUE_PATTERNS = [
        # 「對話」角色說/道/問
        re.compile(r'「([^」]+)」([^，。！？\s]{1,10})(說|道|問|答|喊|叫|嘆|笑|哭)'),
        # 角色：「對話」或 角色:「對話」
        re.compile(r'([^\s，。！？]{1,10})[:：]\s*「([^」]+)」'),
        # 角色「對話」
        re.compile(r'([^\s，。！？「」]{1,6})「([^」]+)」'),
        # 「對話」（單獨的對話，需要從上下文判斷說話者）
        re.compile(r'「([^」]+)」'),
    ]
    
    def __init__(self, config: dict):
        self.config = config
        self.ai_client = AIClient(config) if config.get('ai') else None
    
    def analyze_passages(self, passages: List[Dict], 
                        existing_analysis: Dict = None) -> Dict:
        """
        分析所有段落
        
        Args:
            passages: 段落列表（從 TweeParser 來）
            existing_analysis: 已有的分析結果（可選）
        
        Returns:
            分析結果
        """
        # 合併所有文字
        all_text = '\n\n'.join([p.get('content', '') for p in passages])
        
        # 如果有現成的分析結果，使用它
        if existing_analysis:
            characters = existing_analysis.get('characters', [])
            scenes = existing_analysis.get('scenes', [])
        else:
            # 用 AI 分析
            characters = self._analyze_characters_ai(all_text)
            scenes = self._analyze_scenes_ai(all_text)
        
        # 建立角色名稱到 ID 的映射
        char_name_to_id = {c.get('name', ''): c.get('id', '') for c in characters}
        
        # 分析每個段落的對話和場景
        processed_passages = []
        for passage in passages:
            processed = self._analyze_single_passage(
                passage, 
                char_name_to_id,
                [s.get('id', '') for s in scenes]
            )
            processed_passages.append(processed)
        
        return {
            'characters': characters,
            'scenes': scenes,
            'passages': processed_passages
        }
    
    def _analyze_characters_ai(self, text: str) -> List[Dict]:
        """用 AI 分析角色"""
        if not self.ai_client:
            return self._analyze_characters_rule(text)
        
        prompt = f"""
分析以下故事中的角色，用 JSON 格式回答：

{{
  "characters": [
    {{
      "id": "英文ID（小寫底線）",
      "name": "角色名稱",
      "description": "外貌和性格描述",
      "expressions": ["normal", "happy", "sad", "angry", "surprised"]
    }}
  ]
}}

只列出有名字的重要角色。

故事內容：
{text[:6000]}
"""
        result = self.ai_client.analyze(prompt)
        return result.get('characters', [])
    
    def _analyze_characters_rule(self, text: str) -> List[Dict]:
        """用規則分析角色（備用方案）"""
        # 簡單的角色名稱提取
        names = set()
        
        for pattern in self.DIALOGUE_PATTERNS[:3]:
            for match in pattern.finditer(text):
                groups = match.groups()
                for g in groups:
                    if g and len(g) <= 6 and not any(c in g for c in '，。！？'):
                        names.add(g)
        
        characters = []
        for i, name in enumerate(names):
            char_id = f"char_{i+1}"
            characters.append({
                'id': char_id,
                'name': name,
                'description': '',
                'expressions': ['normal', 'happy', 'sad']
            })
        
        return characters
    
    def _analyze_scenes_ai(self, text: str) -> List[Dict]:
        """用 AI 分析場景"""
        if not self.ai_client:
            return self._analyze_scenes_rule(text)
        
        prompt = f"""
分析以下故事中的場景/地點，用 JSON 格式回答：

{{
  "scenes": [
    {{
      "id": "英文ID（小寫底線）",
      "name": "場景名稱",
      "description": "視覺描述（用於生成背景圖）",
      "time_of_day": "日間/夜間/黃昏",
      "mood": "氛圍"
    }}
  ]
}}

故事內容：
{text[:6000]}
"""
        result = self.ai_client.analyze(prompt)
        return result.get('scenes', [])
    
    def _analyze_scenes_rule(self, text: str) -> List[Dict]:
        """用規則分析場景（備用）"""
        # 簡單的場景關鍵字提取
        keywords = ['房間', '客廳', '廚房', '學校', '教室', '辦公室', 
                   '公園', '街道', '咖啡廳', '餐廳', '店']
        
        scenes = []
        for i, kw in enumerate(keywords):
            if kw in text:
                scenes.append({
                    'id': f"scene_{i+1}",
                    'name': kw,
                    'description': kw,
                    'time_of_day': '日間',
                    'mood': '一般'
                })
        
        return scenes if scenes else [{'id': 'default', 'name': '場景', 
                                       'description': '一般場景', 
                                       'time_of_day': '日間', 'mood': '一般'}]
    
    def _analyze_single_passage(self, passage: Dict, 
                                char_name_to_id: Dict,
                                scene_ids: List[str]) -> Dict:
        """分析單一段落"""
        content = passage.get('content', '')
        name = passage.get('name', '')
        
        # 提取場景標記
        scene_id = None
        scene_markers = self._extract_scene_markers(content)
        if scene_markers:
            scene_id = scene_markers[0]
        
        # 提取連結/選項
        choices = passage.get('choices', [])
        if not choices:
            choices = self._extract_choices(content)
        
        # 分析內容行
        lines = self._analyze_content_lines(content, char_name_to_id)
        
        return {
            'name': name,
            'scene_id': scene_id,
            'lines': lines,
            'choices': choices
        }
    
    def _extract_scene_markers(self, content: str) -> List[str]:
        """提取場景標記"""
        patterns = [
            r'\{/\*\s*scene:\s*([^\*]+)\s*\*/\}',
            r'<!--\s*scene:\s*([^>]+)\s*-->',
            r'\[scene:\s*([^\]]+)\]'
        ]
        
        scenes = []
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            scenes.extend([m.strip() for m in matches])
        
        return scenes
    
    def _extract_choices(self, content: str) -> List[Dict]:
        """提取選項"""
        # Twee 連結格式
        pattern = r'\[\[([^\]|]+?)(?:\|[^\]]+?)?\s*(?:->\s*([^\]]+?))?\]\]'
        
        choices = []
        for match in re.finditer(pattern, content):
            text = match.group(1).strip()
            target = match.group(2).strip() if match.group(2) else text
            
            # 移除條件標記
            if '|?' in text:
                text = text.split('|?')[0].strip()
            
            choices.append({
                'text': text,
                'target': target.replace(' ', '_')
            })
        
        return choices
    
    def _analyze_content_lines(self, content: str, 
                               char_name_to_id: Dict) -> List[Dict]:
        """分析內容，識別對話和旁白"""
        lines = []
        
        # 移除連結標記
        clean_content = re.sub(r'\[\[[^\]]+\]\]', '', content)
        # 移除場景標記
        clean_content = re.sub(r'\{/\*[^\*]+\*/\}', '', clean_content)
        clean_content = re.sub(r'<!--[^>]+-->', '', clean_content)
        
        # 按行處理
        for line in clean_content.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # 嘗試識別對話
            dialogue = self._parse_dialogue(line, char_name_to_id)
            if dialogue:
                lines.append(dialogue)
            else:
                # 旁白
                lines.append({
                    'type': 'narration',
                    'text': line
                })
        
        return lines
    
    def _parse_dialogue(self, line: str, char_name_to_id: Dict) -> Optional[Dict]:
        """解析對話行"""
        # 模式1: 「對話」角色說
        match = re.search(r'「([^」]+)」([^\s，。！？]{1,6})(說|道|問|答|喊)', line)
        if match:
            text = match.group(1)
            speaker_name = match.group(2)
            char_id = char_name_to_id.get(speaker_name, speaker_name.lower())
            return {
                'type': 'dialogue',
                'character': char_id,
                'text': text,
                'expression': self._guess_expression(text)
            }
        
        # 模式2: 角色：「對話」
        match = re.search(r'([^\s，。！？]{1,6})[:：]\s*「([^」]+)」', line)
        if match:
            speaker_name = match.group(1)
            text = match.group(2)
            char_id = char_name_to_id.get(speaker_name, speaker_name.lower())
            return {
                'type': 'dialogue',
                'character': char_id,
                'text': text,
                'expression': self._guess_expression(text)
            }
        
        # 模式3: 角色「對話」（名字緊接引號）
        match = re.search(r'^([^\s，。！？「」]{1,4})「([^」]+)」', line)
        if match:
            speaker_name = match.group(1)
            text = match.group(2)
            if speaker_name in char_name_to_id:
                return {
                    'type': 'dialogue',
                    'character': char_name_to_id[speaker_name],
                    'text': text,
                    'expression': self._guess_expression(text)
                }
        
        return None
    
    def _guess_expression(self, text: str) -> str:
        """根據對話內容猜測表情"""
        # 簡單的關鍵字匹配
        if any(kw in text for kw in ['開心', '高興', '太好', '哈哈', '嘻']):
            return 'happy'
        if any(kw in text for kw in ['難過', '傷心', '哭', '嗚', '抱歉', '對不起']):
            return 'sad'
        if any(kw in text for kw in ['生氣', '可惡', '混蛋', '怒', '煩']):
            return 'angry'
        if any(kw in text for kw in ['什麼', '欸', '咦', '真的', '！？']):
            return 'surprised'
        if any(kw in text for kw in ['緊張', '怎麼辦', '糟糕']):
            return 'nervous'
        
        return 'normal'
