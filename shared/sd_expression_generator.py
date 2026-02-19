#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SD Expression Generator - 使用 Stable Diffusion img2img 生成表情變化
透過低 denoising strength 保持角色一致性
"""

import base64
import requests
from pathlib import Path
from typing import Dict, List, Optional
from PIL import Image
import io
import json


class SDExpressionGenerator:
    """SD 表情生成器 - 使用 img2img 保持角色一致性"""
    
    # 表情對應的 prompt 修飾詞（放在 prompt 最前面優先處理）
    EXPRESSION_PROMPTS = {
        'normal': 'neutral expression, calm face, relaxed',
        'happy': '(smiling:1.3), (happy expression:1.2), bright eyes, cheerful, mouth open smile',
        'sad': '(sad expression:1.3), (melancholic:1.2), downcast eyes, frowning, gloomy',
        'angry': '(angry expression:1.3), (furrowed brows:1.2), intense glare, gritting teeth, frustrated',
        'surprised': '(surprised expression:1.3), (wide eyes:1.2), open mouth, shocked, astonished',
        'shy': '(shy expression:1.3), (blushing:1.2), looking away, embarrassed, flustered',
        'worried': '(worried expression:1.3), (anxious:1.2), concerned look, nervous',
        'thinking': '(thinking expression:1.3), (contemplative:1.2), looking up, pondering',
        'smirk': '(smirking:1.3), (confident smile:1.2), sly expression, one side smile',
        'crying': '(crying:1.3), (tears:1.2), tears streaming down face, sorrowful'
    }
    
    # 表情對應的負面 prompt（強化排除不要的表情）
    EXPRESSION_NEGATIVE = {
        'normal': 'smiling, crying, tears, angry, sad',
        'happy': 'sad, crying, tears, angry, neutral, frown, melancholic',
        'sad': 'happy, smiling, laughing, cheerful, tears, crying',
        'angry': 'happy, smiling, calm, crying, tears, cheerful',
        'surprised': 'calm, neutral, bored, crying, tears, sleepy',
        'shy': 'confident, bold, crying, tears, angry',
        'worried': 'calm, relaxed, happy, crying, tears, smiling',
        'thinking': 'confused, empty stare, crying, tears',
        'smirk': 'neutral, sad, crying, tears, frown',
        'crying': 'happy, smiling, cheerful'
    }
    
    def __init__(self, config: dict):
        self.config = config
        sd_config = config.get('image_generation', {}).get('stable_diffusion', {})
        self.api_url = sd_config.get('api_url', 'http://localhost:7860')
        self.default_model = sd_config.get('default_model', '')
        
        # img2img 參數（針對表情變化優化）
        self.denoising_strength = 0.35  # 低值保持角色一致性
        self.steps = 25
        self.cfg_scale = 7
        
    def _image_to_base64(self, image_path: str) -> str:
        """將圖片轉為 base64"""
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    
    def _base64_to_image(self, b64_data: str, output_path: str):
        """將 base64 存為圖片"""
        image_data = base64.b64decode(b64_data)
        with open(output_path, 'wb') as f:
            f.write(image_data)
    
    def generate_expression(self, 
                           reference_path: str,
                           target_expression: str,
                           output_path: str,
                           base_prompt: str = "",
                           denoising_strength: float = None) -> bool:
        """
        使用 SD img2img 生成表情變化
        
        Args:
            reference_path: 參考圖路徑
            target_expression: 目標表情
            output_path: 輸出路徑
            base_prompt: 基礎 prompt（角色描述）
            denoising_strength: 去噪強度（越低越像原圖）
        
        Returns:
            是否成功
        """
        try:
            # 取得表情 prompt
            expr_prompt = self.EXPRESSION_PROMPTS.get(target_expression, '')
            expr_negative = self.EXPRESSION_NEGATIVE.get(target_expression, '')
            
            # 組合 prompt（表情放最前面優先處理）
            if base_prompt:
                # 移除原 prompt 中可能的表情描述
                cleaned_prompt = base_prompt
                for remove_word in ['neutral expression', 'normal expression', 'calm expression', 'smiling', 'happy', 'sad', 'angry']:
                    cleaned_prompt = cleaned_prompt.replace(remove_word, '')
                prompt = f"{expr_prompt}, {cleaned_prompt}" if expr_prompt else cleaned_prompt
            else:
                prompt = f"{expr_prompt}, anime character portrait, high quality, detailed face"
            
            negative_prompt = f"{expr_negative}, low quality, blurry, deformed, bad anatomy, bad hands"
            
            print(f"   [SD] Prompt: {prompt[:100]}...")
            print(f"   [SD] Negative: {negative_prompt[:80]}...")
            
            # 讀取參考圖
            ref_b64 = self._image_to_base64(reference_path)
            
            # 取得圖片尺寸
            with Image.open(reference_path) as img:
                width, height = img.size
            
            # img2img API 請求
            payload = {
                "init_images": [ref_b64],
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "denoising_strength": denoising_strength or self.denoising_strength,
                "steps": self.steps,
                "cfg_scale": self.cfg_scale,
                "width": width,
                "height": height,
                "sampler_name": "DPM++ 2M Karras",
                "seed": -1,
            }
            
            print(f"   [SD] Generating {target_expression} (denoising: {payload['denoising_strength']})")
            
            response = requests.post(
                f"{self.api_url}/sdapi/v1/img2img",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('images'):
                    # 儲存第一張圖
                    output_path = Path(output_path)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    self._base64_to_image(result['images'][0], str(output_path))
                    print(f"   [SD OK] Generated {target_expression}")
                    return True
            
            print(f"   [SD ERROR] Status {response.status_code}: {response.text[:200]}")
            return False
            
        except requests.exceptions.ConnectionError:
            print(f"   [SD ERROR] Cannot connect to SD WebUI at {self.api_url}")
            return False
        except Exception as e:
            print(f"   [SD ERROR] {e}")
            return False
    
    def generate_all_expressions(self,
                                  reference_path: str,
                                  expressions: List[str],
                                  output_dir: str,
                                  base_prompt: str = "",
                                  denoising_strength: float = None,
                                  callback=None) -> Dict[str, str]:
        """
        生成所有表情
        
        Args:
            reference_path: 參考圖路徑
            expressions: 表情列表
            output_dir: 輸出目錄
            base_prompt: 角色描述 prompt
            denoising_strength: 去噪強度
            callback: 進度回呼
        
        Returns:
            {表情: 路徑} 字典
        """
        import shutil
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        results = {}
        total = len(expressions)
        
        for i, expr in enumerate(expressions):
            if callback:
                callback(i + 1, total, f"Generating {expr}")
            
            output_path = output_dir / f"{expr}.png"
            
            # normal 直接複製原圖
            if expr == 'normal':
                shutil.copy(reference_path, output_path)
                results[expr] = str(output_path)
                print(f"   [OK] Using reference as normal")
                continue
            
            success = self.generate_expression(
                reference_path=reference_path,
                target_expression=expr,
                output_path=str(output_path),
                base_prompt=base_prompt,
                denoising_strength=denoising_strength
            )
            
            if success:
                results[expr] = str(output_path)
            else:
                # 失敗時複製原圖
                shutil.copy(reference_path, output_path)
                results[expr] = str(output_path)
                print(f"   [FALLBACK] Copied reference for {expr}")
        
        return results
    
    def test_connection(self) -> bool:
        """測試 SD WebUI 連線"""
        try:
            response = requests.get(f"{self.api_url}/sdapi/v1/options", timeout=5)
            return response.status_code == 200
        except:
            return False


if __name__ == "__main__":
    # 測試
    import json
    
    with open("config.json", encoding='utf-8') as f:
        config = json.load(f)
    
    gen = SDExpressionGenerator(config)
    
    if gen.test_connection():
        print("SD WebUI 連線成功！")
    else:
        print("SD WebUI 未運行")
