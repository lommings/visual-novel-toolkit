#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Expression Generator - 基於參考圖生成角色表情變化
使用 Gemini 圖片編輯功能保持角色一致性
"""

import base64
from pathlib import Path
from typing import Dict, List, Optional
from PIL import Image
import io


class ExpressionGenerator:
    """表情生成器 - 保持角色一致性"""
    
    # 表情對應的英文描述
    EXPRESSION_PROMPTS = {
        'normal': 'neutral expression, calm face',
        'happy': 'happy expression, genuine smile, bright eyes',
        'sad': 'sad expression, downcast eyes, slight frown',
        'angry': 'angry expression, furrowed brows, intense eyes',
        'surprised': 'surprised expression, wide eyes, raised eyebrows',
        'shy': 'shy expression, slight blush, averted gaze',
        'worried': 'worried expression, concerned look, tense face',
        'thinking': 'thinking expression, contemplative look, eyes looking up',
        'smirk': 'smirking expression, confident half-smile',
        'crying': 'crying expression, tears in eyes, sorrowful face'
    }
    
    def __init__(self, config: dict):
        self.config = config
        self.api_key = config.get('ai', {}).get('gemini', {}).get('api_key', '')
        
    def generate_expression(self, reference_path: str, 
                           target_expression: str,
                           output_path: str,
                           character_name: str = "",
                           character_prompt: str = "") -> bool:
        """
        基於參考圖生成指定表情
        使用 Gemini 3 Pro Image Preview
        
        Args:
            reference_path: 參考圖路徑（選定的角色基準圖）
            target_expression: 目標表情（如 'happy', 'sad'）
            output_path: 輸出路徑
            character_name: 角色名稱（可選，用於更好的提示）
            character_prompt: 角色完整描述（用於 fallback 保持一致性）
        
        Returns:
            是否成功
        """
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=self.api_key)
            
            # 載入參考圖
            ref_image = Image.open(reference_path)
            
            # 將圖片轉換為 bytes
            img_byte_arr = io.BytesIO()
            ref_image.save(img_byte_arr, format='PNG')
            img_bytes = img_byte_arr.getvalue()
            
            # 取得表情描述
            expr_desc = self.EXPRESSION_PROMPTS.get(
                target_expression, 
                f'{target_expression} expression'
            )
            
            # 使用 Gemini 3 Pro Image Preview
            edit_prompt = f"""Look at this anime character portrait image.
Generate a new version of this EXACT same character with a different expression.

KEEP EXACTLY THE SAME:
- Character's face shape and features
- Hair style, color and length  
- Clothing and accessories
- Pose and angle
- Art style and quality
- Background

ONLY CHANGE: The facial expression to show {expr_desc}

Output a new image of this same character with the new expression."""

            response = client.models.generate_content(
                model="gemini-3-pro-image-preview",
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_image(types.Image(image_bytes=img_bytes)),
                            types.Part.from_text(edit_prompt)
                        ]
                    )
                ],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"]
                )
            )
            
            # 儲存生成的圖片
            if response.candidates:
                for part in response.candidates[0].content.parts:
                    if part.inline_data and part.inline_data.mime_type.startswith('image/'):
                        image_data = part.inline_data.data
                        
                        output_path = Path(output_path)
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        with open(output_path, 'wb') as f:
                            f.write(image_data)
                        
                        print(f"   [OK] Generated {target_expression} expression with Gemini 3 Pro")
                        return True
            
            print(f"   [WARN] No image in response for {target_expression}")
            return self._fallback_generate(reference_path, target_expression, output_path, expr_desc, character_prompt)
            
        except Exception as e:
            print(f"   [ERROR] Expression generation failed: {e}")
            return self._fallback_generate(reference_path, target_expression, output_path, 
                                          self.EXPRESSION_PROMPTS.get(target_expression, target_expression),
                                          character_prompt)
    
    def _fallback_generate(self, reference_path: str, expression: str, 
                          output_path: str, expr_desc: str,
                          character_prompt: str = "") -> bool:
        """備用方案：使用 Stable Diffusion img2img（免費）"""
        try:
            # 優先使用 SD（免費）
            from .sd_expression_generator import SDExpressionGenerator
            
            sd_gen = SDExpressionGenerator(self.config)
            
            if sd_gen.test_connection():
                print(f"   [FALLBACK] Using Stable Diffusion img2img (FREE)")
                success = sd_gen.generate_expression(
                    reference_path=reference_path,
                    target_expression=expression,
                    output_path=output_path,
                    base_prompt=character_prompt
                )
                if success:
                    print(f"   [FALLBACK OK] Generated {expression} with SD")
                    return True
            else:
                print(f"   [FALLBACK] SD not available, trying copy")
                
        except ImportError:
            print(f"   [FALLBACK] SD module not found")
        except Exception as e:
            print(f"   [FALLBACK ERROR]: {e}")
        
        # 最後手段：複製原圖（免費，保持一致性）
        try:
            import shutil
            shutil.copy(reference_path, output_path)
            print(f"   [COPY] Copied reference image for {expression}")
            return True
        except:
            return False
    
    def generate_all_expressions(self, reference_path: str,
                                  expressions: List[str],
                                  output_dir: str,
                                  character_id: str = "",
                                  character_prompt: str = "",
                                  callback=None) -> Dict[str, str]:
        """
        生成角色的所有表情
        
        Args:
            reference_path: 參考圖路徑
            expressions: 需要的表情列表
            output_dir: 輸出目錄
            character_id: 角色 ID
            character_prompt: 角色完整描述（用於保持一致性）
            callback: 進度回呼 callback(current, total, message)
        
        Returns:
            {表情: 輸出路徑} 字典
        """
        output_dir = Path(output_dir)
        # 直接使用 output_dir，不再加 characters/id（由呼叫者決定路徑）
        char_dir = output_dir
        char_dir.mkdir(parents=True, exist_ok=True)
        
        results = {}
        total = len(expressions)
        
        for i, expr in enumerate(expressions):
            if callback:
                callback(i + 1, total, f"Generating {expr} expression")
            
            output_path = char_dir / f"{expr}.png"
            
            # normal 表情直接使用參考圖
            if expr == 'normal':
                import shutil
                shutil.copy(reference_path, output_path)
                results[expr] = str(output_path)
                print(f"   [OK] Using reference as {expr}")
                continue
            
            success = self.generate_expression(
                reference_path=reference_path,
                target_expression=expr,
                output_path=str(output_path),
                character_prompt=character_prompt
            )
            
            if success:
                results[expr] = str(output_path)
        
        return results


def test_expression_generator():
    """測試表情生成器"""
    from config_manager import ConfigManager
    
    config = ConfigManager.load()
    gen = ExpressionGenerator(config)
    
    # 測試（需要有參考圖）
    ref_path = "test_reference.png"
    if Path(ref_path).exists():
        result = gen.generate_expression(
            reference_path=ref_path,
            target_expression='happy',
            output_path='test_happy.png'
        )
        print(f"Test result: {result}")
    else:
        print("No test reference image found")


if __name__ == '__main__':
    test_expression_generator()
