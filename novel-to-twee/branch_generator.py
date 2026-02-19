#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分支生成器 - 根據分析結果生成完整的分支劇情"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.ai_client import AIClient


class BranchGenerator:
    """分支生成器"""
    
    def __init__(self, config: dict):
        self.config = config
        self.ai_client = AIClient(config)
    
    def generate_branches(self, text: str, analysis: dict) -> list:
        """
        根據分析結果生成完整的分支劇情
        
        Args:
            text: 原始小說文字
            analysis: 故事分析結果
        
        Returns:
            段落列表，每個段落包含內容和選項
        """
        branch_points = analysis.get('branch_points', [])
        characters = analysis.get('characters', [])
        scenes = analysis.get('scenes', [])
        endings = analysis.get('endings', [])
        
        if not branch_points:
            # 沒有分支點，生成線性故事
            return self._generate_linear_story(text, characters, scenes)
        
        # 生成有分支的故事
        return self._generate_branching_story(text, analysis)
    
    def _generate_linear_story(self, text: str, characters: list, scenes: list) -> list:
        """生成線性故事（無分支）"""
        char_names = [c.get('name', '') for c in characters]
        scene_names = [s.get('name', '') for s in scenes]
        
        prompt = f"""
請將以下小說轉換為視覺小說腳本格式。

角色：{', '.join(char_names)}
場景：{', '.join(scene_names)}

輸出 JSON 格式，將故事分成多個段落（passage）：
{{
  "passages": [
    {{
      "name": "Start",
      "scene_id": "場景ID",
      "content": "這個段落的內容...",
      "next": "下一個段落名稱"
    }},
    {{
      "name": "Chapter1",
      "scene_id": "場景ID",
      "content": "...",
      "next": "End"
    }}
  ]
}}

規則：
1. 第一個段落必須叫 "Start"
2. 每個段落 200-500 字
3. 場景變換時要標記 scene_id
4. 保持原文的對話和描述

小說內容：
{text[:12000]}
"""
        
        result = self.ai_client.analyze(prompt)
        return result.get('passages', [])
    
    def _generate_branching_story(self, text: str, analysis: dict) -> list:
        """生成有分支的故事"""
        branch_points = analysis.get('branch_points', [])
        characters = analysis.get('characters', [])
        scenes = analysis.get('scenes', [])
        endings = analysis.get('endings', [])
        
        char_names = [c.get('name', '') for c in characters]
        
        # 構建分支描述
        branch_desc = ""
        for i, bp in enumerate(branch_points):
            branch_desc += f"\n分支點 {i+1}：{bp.get('description', '')}\n"
            for choice in bp.get('choices', []):
                branch_desc += f"  - {choice.get('text', '')}: {choice.get('consequence', '')}\n"
        
        # 構建結局描述
        ending_desc = ""
        for ending in endings:
            ending_desc += f"- {ending.get('name', '')}: {ending.get('description', '')}\n"
        
        prompt = f"""
請將以下小說轉換為有分支的視覺小說腳本。

角色：{', '.join(char_names)}
分支設計：{branch_desc}
可能的結局：{ending_desc}

輸出 JSON 格式：
{{
  "passages": [
    {{
      "name": "Start",
      "scene_id": "場景ID",
      "content": "段落內容...",
      "choices": [
        {{"text": "選項文字", "target": "目標段落名稱"}}
      ]
    }},
    {{
      "name": "Route_A",
      "scene_id": "場景ID", 
      "content": "分支A的內容...",
      "next": "下一段落"
    }}
  ]
}}

規則：
1. 第一個段落必須叫 "Start"
2. 每個段落 200-400 字
3. 分支點要有 choices，非分支點用 next
4. 確保所有路線都能到達結局
5. 段落名稱用英文或拼音，不要空格
6. 保持原文風格，適當擴展分支內容

小說內容：
{text[:12000]}
"""
        
        result = self.ai_client.analyze(prompt)
        passages = result.get('passages', [])
        
        # 驗證和修正
        passages = self._validate_passages(passages)
        
        return passages
    
    def _validate_passages(self, passages: list) -> list:
        """驗證和修正段落結構"""
        if not passages:
            return [{'name': 'Start', 'content': '（空白故事）', 'next': 'End'},
                    {'name': 'End', 'content': '結束'}]
        
        # 確保有 Start
        has_start = any(p.get('name') == 'Start' for p in passages)
        if not has_start and passages:
            passages[0]['name'] = 'Start'
        
        # 確保段落名稱合法
        for passage in passages:
            name = passage.get('name', '')
            # 移除空格，轉換為底線
            passage['name'] = name.replace(' ', '_').replace('-', '_')
        
        # 更新引用
        name_map = {p.get('name', ''): p.get('name', '') for p in passages}
        for passage in passages:
            if 'next' in passage:
                old_next = passage['next']
                passage['next'] = old_next.replace(' ', '_').replace('-', '_')
            if 'choices' in passage:
                for choice in passage['choices']:
                    old_target = choice.get('target', '')
                    choice['target'] = old_target.replace(' ', '_').replace('-', '_')
        
        return passages
    
    def expand_branch(self, base_text: str, branch_point: dict, 
                      choice: dict, characters: list) -> str:
        """
        擴展單一分支的內容
        
        Args:
            base_text: 基礎文字
            branch_point: 分支點資訊
            choice: 選擇的選項
            characters: 角色列表
        
        Returns:
            擴展後的分支內容
        """
        char_names = [c.get('name', '') for c in characters]
        
        prompt = f"""
請根據以下資訊，撰寫視覺小說的分支劇情。

原始故事背景：
{base_text[:2000]}

分支點：{branch_point.get('description', '')}
玩家選擇：{choice.get('text', '')}
選擇後果：{choice.get('consequence', '')}

角色：{', '.join(char_names)}

請寫 300-500 字的分支內容，保持原作風格。
直接輸出文字內容，不需要 JSON 格式。
"""
        
        return self.ai_client.generate_text(prompt)
