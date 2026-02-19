#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""預覽圖生成器"""

import sys
import random
from pathlib import Path
from typing import List, Dict

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.image_generator import ImageGenerator
from shared.expression_generator import ExpressionGenerator
from shared.file_utils import ensure_dir


class PreviewGenerator:
    """預覽圖生成器"""
    
    def __init__(self, config: dict):
        self.config = config
        self.image_gen = ImageGenerator(config)
        self.expr_gen = ExpressionGenerator(config)
        
        previewer_config = config.get('asset_previewer', {})
        self.char_concepts_count = previewer_config.get('character_concepts_count', 4)
        self.scene_concepts_count = previewer_config.get('scene_concepts_count', 3)
    
    def generate_character_previews(self, characters: List[Dict], 
                                    output_dir: str,
                                    callback=None) -> Dict:
        """
        為所有角色生成預覽圖
        
        Args:
            characters: 角色列表
            output_dir: 輸出目錄
            callback: 進度回呼函式 callback(current, total, message)
        
        Returns:
            生成結果 {角色ID: [圖片路徑列表]}
        """
        output_dir = Path(output_dir)
        results = {}
        
        total = len(characters) * self.char_concepts_count
        current = 0
        
        for char in characters:
            char_id = char.get('id', 'unknown')
            char_dir = output_dir / 'characters' / char_id
            ensure_dir(char_dir)
            
            paths = []
            for i in range(self.char_concepts_count):
                current += 1
                if callback:
                    callback(current, total, f"生成 {char.get('name', char_id)} 概念圖 {i+1}")
                
                output_path = char_dir / f"concept_{i+1}.png"
                
                success = self._generate_character_concept(char, output_path, seed=i*1000)
                
                if success:
                    paths.append(str(output_path))
            
            results[char_id] = paths
        
        return results
    
    def generate_scene_previews(self, scenes: List[Dict],
                                output_dir: str,
                                callback=None) -> Dict:
        """
        為所有場景生成預覽圖
        
        Args:
            scenes: 場景列表
            output_dir: 輸出目錄
            callback: 進度回呼函式
        
        Returns:
            生成結果 {場景ID: [圖片路徑列表]}
        """
        output_dir = Path(output_dir)
        results = {}
        
        total = len(scenes) * self.scene_concepts_count
        current = 0
        
        for scene in scenes:
            scene_id = scene.get('id', 'unknown')
            scene_dir = output_dir / 'scenes' / scene_id
            ensure_dir(scene_dir)
            
            paths = []
            for i in range(self.scene_concepts_count):
                current += 1
                if callback:
                    callback(current, total, f"生成 {scene.get('name', scene_id)} 場景 {i+1}")
                
                output_path = scene_dir / f"concept_{i+1}.jpg"
                
                success = self._generate_scene_concept(scene, output_path, seed=i*1000)
                
                if success:
                    paths.append(str(output_path))
            
            results[scene_id] = paths
        
        return results
    
    def _generate_character_concept(self, character: Dict, 
                                    output_path: Path, seed: int = -1) -> bool:
        """生成單一角色概念圖"""
        return self.image_gen.generate_character(
            character=character,
            expression='normal',  # 概念圖用 normal
            output_path=str(output_path)
        )
    
    def _generate_scene_concept(self, scene: Dict,
                               output_path: Path, seed: int = -1) -> bool:
        """生成單一場景概念圖"""
        return self.image_gen.generate_scene(
            scene=scene,
            output_path=str(output_path)
        )
    
    def generate_character_preview(self, character: Dict, output_dir: str,
                                   count: int = 4) -> List[str]:
        """
        為單一角色生成預覽圖（API 用）
        
        Args:
            character: 角色資料（含 visual_description）
            output_dir: 輸出目錄
            count: 生成數量
        
        Returns:
            生成的圖片路徑列表
        """
        output_dir = Path(output_dir)
        ensure_dir(output_dir)
        
        paths = []
        for i in range(count):
            output_path = output_dir / f"concept_{i+1}.png"
            
            success = self._generate_character_concept(character, output_path, seed=i*1000)
            
            if success:
                paths.append(str(output_path))
        
        return paths
    
    def generate_scene_preview(self, scene: Dict, output_dir: str,
                               count: int = 3, 
                               model: str = None,
                               style: str = None) -> List[str]:
        """
        為單一場景生成預覽圖（API 用，支援指定模型和風格）
        
        Args:
            scene: 場景資料（含 visual_description）
            output_dir: 輸出目錄
            count: 生成數量
            model: 指定使用的模型（如 gemini-3-pro-image-preview, stable_diffusion）
            style: 指定視覺風格
        
        Returns:
            生成的圖片路徑列表
        """
        import copy
        output_dir = Path(output_dir)
        ensure_dir(output_dir)
        
        # 建立臨時設定
        temp_config = copy.deepcopy(self.config)
        
        if model:
            # 根據模型名稱決定 provider（使用 scene_provider）
            if model == 'stable_diffusion':
                temp_config['image_generation']['scene_provider'] = 'stable_diffusion'
            else:
                temp_config['image_generation']['scene_provider'] = 'gemini_imagen'
                temp_config['image_generation']['gemini_imagen'] = {'model': model}
        
        if style:
            temp_config['visual_style'] = temp_config.get('visual_style', {})
            temp_config['visual_style']['current'] = style
        
        # 建立臨時生成器
        temp_gen = ImageGenerator(temp_config)
        
        paths = []
        for i in range(count):
            output_path = output_dir / f"concept_{i+1}.png"
            
            try:
                success = temp_gen.generate_scene(
                    scene=scene,
                    output_path=str(output_path)
                )
                
                if success:
                    paths.append(str(output_path))
            except Exception as e:
                print(f"   ⚠️ 場景生成失敗: {e}")
        
        return paths
    
    def generate_final_character(self, character: Dict, 
                                 reference_path: str,
                                 output_dir: str,
                                 callback=None) -> Dict:
        """
        根據選定的概念圖，生成角色的所有表情
        使用 Gemini 圖片編輯功能保持角色一致性
        
        Args:
            character: 角色資料
            reference_path: 選定的概念圖路徑（基準外觀）
            output_dir: 輸出目錄
            callback: 進度回呼
        
        Returns:
            生成結果 {表情: 路徑}
        """
        char_id = character.get('id', 'unknown')
        
        expressions = character.get('expressions_needed', 
                                    character.get('expressions', ['normal']))
        
        # 取得角色描述（用於保持一致性）
        char_prompt = character.get('visual_description', '') or character.get('visual_prompt', '') or ''
        
        # 使用 ExpressionGenerator 保持角色一致性
        results = self.expr_gen.generate_all_expressions(
            reference_path=reference_path,
            expressions=expressions,
            output_dir=str(output_dir),
            character_id=char_id,
            character_prompt=char_prompt,
            callback=callback
        )
        
        return results
    
    def generate_final_scene(self, scene: Dict,
                            reference_path: str,
                            output_dir: str) -> str:
        """
        生成最終場景圖（直接使用選定的概念圖）
        
        Args:
            scene: 場景資料
            reference_path: 選定的概念圖路徑
            output_dir: 輸出目錄
        
        Returns:
            最終圖片路徑
        """
        import shutil
        
        output_dir = Path(output_dir)
        scene_id = scene.get('id', 'unknown')
        
        output_path = output_dir / 'scenes' / f"{scene_id}.jpg"
        ensure_dir(output_path.parent)
        
        # 直接複製選定的概念圖
        shutil.copy(reference_path, output_path)
        
        return str(output_path)
