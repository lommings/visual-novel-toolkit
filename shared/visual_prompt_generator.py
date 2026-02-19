#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visual Prompt Generator - 將故事描述轉換為視覺生成用的 Prompt
"""

import json
import re
from typing import Dict, List, Optional

from .ai_client import AIClient


class VisualPromptGenerator:
    """視覺 Prompt 生成器"""
    
    def __init__(self, config: dict):
        self.config = config
        self.ai_client = AIClient(config)
    
    def generate_character_visual_prompt(self, character: dict, 
                                         story_context: str = "") -> dict:
        """
        將角色故事描述轉換為視覺外觀描述
        
        Args:
            character: 角色資料 (含 name, description)
            story_context: 故事背景（可選，幫助 AI 推斷外觀）
        
        Returns:
            包含 visual_prompt 的角色資料
        """
        name = character.get('name', character.get('id', 'Unknown'))
        description = character.get('description', '')
        
        prompt = f"""你是一個專業的角色視覺設計師。請根據以下角色的故事描述，生成適合用於 AI 圖像生成的視覺外觀描述。

角色名稱：{name}
故事描述：{description}
{f"故事背景：{story_context}" if story_context else ""}

請生成一個詳細的視覺外觀描述，包含：
1. 性別與年齡外觀（如：年輕男性、約20歲）
2. 髮型與髮色（如：黑色短髮、略顯凌亂）
3. 眼睛顏色與特徵（如：深邃的黑眼、眼神銳利）
4. 膚色
5. 體型（如：高挑、瘦削、肌肉結實）
6. 服裝風格（根據角色背景推斷合理的服裝）
7. 整體氣質/氛圍（如：冷酷、溫柔、神秘）
8. 任何特殊標記或特徵

請用英文輸出，格式為適合圖像生成的描述性文字。
不要包含動作或故事情節，只描述靜態外觀。

請回覆 JSON 格式：
{{
    "gender": "性別",
    "age_appearance": "年齡外觀描述",
    "hair": "髮型與髮色描述",
    "eyes": "眼睛描述",
    "skin": "膚色",
    "body_type": "體型描述",
    "clothing": "服裝描述",
    "atmosphere": "整體氣質",
    "special_features": "特殊特徵（若無則為空）",
    "visual_prompt": "完整的英文視覺描述（用於圖像生成）"
}}"""
        
        try:
            result = self.ai_client.analyze(prompt)
            
            # 合併結果到角色資料
            character_updated = character.copy()
            character_updated['visual_details'] = {
                'gender': result.get('gender', ''),
                'age_appearance': result.get('age_appearance', ''),
                'hair': result.get('hair', ''),
                'eyes': result.get('eyes', ''),
                'skin': result.get('skin', ''),
                'body_type': result.get('body_type', ''),
                'clothing': result.get('clothing', ''),
                'atmosphere': result.get('atmosphere', ''),
                'special_features': result.get('special_features', '')
            }
            character_updated['visual_prompt'] = result.get('visual_prompt', '')
            
            return character_updated
            
        except Exception as e:
            print(f"   [WARN] Failed to generate visual prompt for {name}: {e}")
            return character
    
    def generate_scene_visual_prompt(self, scene: dict) -> dict:
        """
        優化場景描述為視覺生成用的 Prompt
        
        Args:
            scene: 場景資料 (含 name, description, time_of_day, mood)
        
        Returns:
            包含 visual_prompt 的場景資料
        """
        name = scene.get('name', scene.get('id', 'Unknown'))
        description = scene.get('description', '')
        time_of_day = scene.get('time_of_day', '')
        mood = scene.get('mood', '')
        
        prompt = f"""你是一個專業的場景視覺設計師。請根據以下場景描述，生成適合用於 AI 圖像生成的視覺描述。

場景名稱：{name}
場景描述：{description}
時間：{time_of_day}
氛圍：{mood}

請生成一個詳細的視覺場景描述，包含：
1. 場景類型（室內/室外/半開放）
2. 主要建築/環境元素
3. 光線條件（自然光/人工光、方向、顏色）
4. 色調與氛圍
5. 天氣/環境效果（如適用）
6. 重要的視覺細節
7. 構圖建議（遠景/中景/特寫）

請用英文輸出，格式為適合圖像生成的描述性文字。
不要包含人物，只描述環境場景。

請回覆 JSON 格式：
{{
    "scene_type": "場景類型",
    "main_elements": "主要元素",
    "lighting": "光線描述",
    "color_tone": "色調",
    "weather_effects": "天氣/環境效果",
    "key_details": "重要細節",
    "composition": "構圖建議",
    "visual_prompt": "完整的英文視覺描述（用於圖像生成）"
}}"""
        
        try:
            result = self.ai_client.analyze(prompt)
            
            # 合併結果到場景資料
            scene_updated = scene.copy()
            scene_updated['visual_details'] = {
                'scene_type': result.get('scene_type', ''),
                'main_elements': result.get('main_elements', ''),
                'lighting': result.get('lighting', ''),
                'color_tone': result.get('color_tone', ''),
                'weather_effects': result.get('weather_effects', ''),
                'key_details': result.get('key_details', ''),
                'composition': result.get('composition', '')
            }
            scene_updated['visual_prompt'] = result.get('visual_prompt', '')
            
            return scene_updated
            
        except Exception as e:
            print(f"   [WARN] Failed to generate visual prompt for {name}: {e}")
            return scene
    
    def process_all_characters(self, characters: List[dict], 
                               story_context: str = "",
                               callback=None) -> List[dict]:
        """
        批次處理所有角色
        
        Args:
            characters: 角色列表
            story_context: 故事背景
            callback: 進度回呼 callback(current, total, message)
        
        Returns:
            更新後的角色列表
        """
        results = []
        total = len(characters)
        
        for i, char in enumerate(characters):
            if callback:
                callback(i + 1, total, f"生成 {char.get('name', char.get('id'))} 視覺描述")
            
            updated = self.generate_character_visual_prompt(char, story_context)
            results.append(updated)
        
        return results
    
    def process_all_scenes(self, scenes: List[dict], 
                           callback=None) -> List[dict]:
        """
        批次處理所有場景
        
        Args:
            scenes: 場景列表
            callback: 進度回呼
        
        Returns:
            更新後的場景列表
        """
        results = []
        total = len(scenes)
        
        for i, scene in enumerate(scenes):
            if callback:
                callback(i + 1, total, f"生成 {scene.get('name', scene.get('id'))} 視覺描述")
            
            updated = self.generate_scene_visual_prompt(scene)
            results.append(updated)
        
        return results
