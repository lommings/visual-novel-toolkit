#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""故事分析器 - 使用 AI 分析小說內容"""

import sys
from pathlib import Path

# 加入 shared 模組路徑
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.ai_client import AIClient
from shared.models import Character, Scene


class StoryAnalyzer:
    """故事分析器"""
    
    def __init__(self, config: dict):
        self.config = config
        self.ai_client = AIClient(config)
    
    def analyze(self, text: str) -> dict:
        """
        分析小說文字
        
        Args:
            text: 小說原文
        
        Returns:
            分析結果字典，包含 characters, scenes, branch_points 等
        """
        # 分析角色
        characters = self._analyze_characters(text)
        
        # 分析場景
        scenes = self._analyze_scenes(text)
        
        # 分析故事結構和分支點
        structure = self._analyze_structure(text, characters, scenes)
        
        # 生成標題和摘要
        meta = self._generate_meta(text)
        
        return {
            'title': meta.get('title', '未命名故事'),
            'summary': meta.get('summary', ''),
            'characters': characters,
            'scenes': scenes,
            'branch_points': structure.get('branch_points', []),
            'story_structure': structure.get('story_structure', {}),
            'endings': structure.get('endings', [])
        }
    
    def _analyze_characters(self, text: str) -> list:
        """分析角色"""
        prompt = f"""
請分析以下小說中的角色，用 JSON 格式回答。

對於每個角色，請提供：
1. id: 英文ID（小寫，用底線連接，如 main_character）
2. name: 角色名稱
3. description: 角色描述（外貌、性格、身份）
4. suggested_expressions: 建議的表情列表（如 normal, happy, sad, angry, surprised 等）

只列出有名字或重要的角色，背景人物不需要。

回答格式：
{{
  "characters": [
    {{
      "id": "...",
      "name": "...",
      "description": "...",
      "suggested_expressions": ["normal", "..."]
    }}
  ]
}}

小說內容：
{text[:8000]}
"""
        
        result = self.ai_client.analyze(prompt)
        return result.get('characters', [])
    
    def _analyze_scenes(self, text: str) -> list:
        """分析場景"""
        prompt = f"""
請分析以下小說中出現的場景/地點，用 JSON 格式回答。

對於每個場景，請提供：
1. id: 英文ID（小寫，用底線連接，如 living_room）
2. name: 場景名稱
3. description: 場景視覺描述（用於生成背景圖）
4. location: 地點類型
5. time_of_day: 主要出現的時段（日間/夜間/黃昏/清晨）
6. mood: 場景氛圍

回答格式：
{{
  "scenes": [
    {{
      "id": "...",
      "name": "...",
      "description": "...",
      "location": "...",
      "time_of_day": "...",
      "mood": "..."
    }}
  ]
}}

小說內容：
{text[:8000]}
"""
        
        result = self.ai_client.analyze(prompt)
        return result.get('scenes', [])
    
    def _analyze_structure(self, text: str, characters: list, scenes: list) -> dict:
        """分析故事結構和分支點"""
        char_names = [c.get('name', '') for c in characters]
        
        prompt = f"""
請分析以下小說的故事結構，找出適合做成視覺小說分支的地方。

已識別的角色：{', '.join(char_names)}

請用 JSON 格式回答：
{{
  "story_structure": {{
    "opening": "開場描述",
    "development": "發展描述", 
    "climax": "高潮描述",
    "resolution": "結局描述"
  }},
  "branch_points": [
    {{
      "location": "這個分支點在故事中的位置（引用原文片段）",
      "description": "為什麼這裡適合分支",
      "choices": [
        {{
          "text": "選項文字",
          "consequence": "選擇後的走向"
        }}
      ]
    }}
  ],
  "endings": [
    {{
      "id": "ending_1",
      "name": "結局名稱",
      "type": "good/bad/neutral",
      "description": "結局描述"
    }}
  ]
}}

找出 2-4 個分支點，每個分支點 2-3 個選項。

小說內容：
{text[:10000]}
"""
        
        result = self.ai_client.analyze(prompt)
        return result
    
    def _generate_meta(self, text: str) -> dict:
        """生成標題和摘要"""
        prompt = f"""
請為以下小說生成標題和摘要。

回答格式：
{{
  "title": "故事標題",
  "summary": "100字以內的故事摘要"
}}

小說內容：
{text[:3000]}
"""
        
        result = self.ai_client.analyze(prompt)
        return result
