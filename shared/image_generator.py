#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""圖片生成封裝模組"""

import base64
import requests
from pathlib import Path
from typing import Optional
from abc import ABC, abstractmethod


class ImageProvider(ABC):
    """圖片提供者抽象類別"""
    
    @abstractmethod
    def generate(self, prompt: str, output_path: str, **kwargs) -> bool:
        """生成圖片"""
        pass


class StableDiffusionProvider(ImageProvider):
    """Stable Diffusion WebUI API 提供者"""
    
    def __init__(self, api_url: str, defaults: dict = None):
        self.api_url = api_url.rstrip('/')
        self.defaults = defaults or {
            'steps': 30,
            'cfg_scale': 7.5,
            'width': 512,
            'height': 768,
            'sampler_name': 'DPM++ 2M Karras'
        }
    
    def generate(self, prompt: str, output_path: str, 
                 negative_prompt: str = "", seed: int = -1, **kwargs) -> bool:
        """
        生成圖片
        
        Args:
            prompt: 正向提示詞
            output_path: 輸出路徑
            negative_prompt: 負向提示詞
            seed: 種子值，-1 為隨機
            **kwargs: 其他參數（覆蓋預設值）
        
        Returns:
            是否成功
        """
        payload = {
            'prompt': prompt,
            'negative_prompt': negative_prompt or "low quality, bad anatomy, blurry",
            'seed': seed,
            **self.defaults,
            **kwargs
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/sdapi/v1/txt2img",
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            result = response.json()
            if 'images' in result and result['images']:
                image_data = base64.b64decode(result['images'][0])
                
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                
                return True
        except Exception as e:
            print(f"SD 生成失敗: {e}")
        
        return False
    
    def generate_img2img(self, prompt: str, reference_path: str, output_path: str,
                         negative_prompt: str = "", denoising_strength: float = 0.5,
                         seed: int = -1, **kwargs) -> bool:
        """
        img2img 生成（用參考圖）
        
        Args:
            prompt: 正向提示詞
            reference_path: 參考圖路徑
            output_path: 輸出路徑
            negative_prompt: 負向提示詞
            denoising_strength: 去噪強度（0-1，越低越像原圖）
            seed: 種子值
        
        Returns:
            是否成功
        """
        try:
            # 讀取參考圖並轉為 base64
            with open(reference_path, 'rb') as f:
                ref_image = base64.b64encode(f.read()).decode('utf-8')
            
            payload = {
                'init_images': [ref_image],
                'prompt': prompt,
                'negative_prompt': negative_prompt or "low quality, bad anatomy, blurry",
                'denoising_strength': denoising_strength,
                'seed': seed,
                **self.defaults,
                **kwargs
            }
            
            response = requests.post(
                f"{self.api_url}/sdapi/v1/img2img",
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            result = response.json()
            if 'images' in result and result['images']:
                image_data = base64.b64decode(result['images'][0])
                
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                
                return True
        except Exception as e:
            print(f"SD img2img 生成失敗: {e}")
        
        return False
    
    def check_connection(self) -> bool:
        """檢查 API 連線"""
        try:
            response = requests.get(f"{self.api_url}/sdapi/v1/sd-models", timeout=5)
            return response.status_code == 200
        except:
            return False


class GeminiImagenProvider(ImageProvider):
    """Gemini Imagen API 提供者（成本較高，備用）"""
    
    def __init__(self, api_key: str, model: str = "imagen-4.0-generate-001"):
        self.api_key = api_key
        self.model = model
    
    def generate(self, prompt: str, output_path: str, **kwargs) -> bool:
        """使用 Imagen 生成圖片"""
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=self.api_key)
            
            response = client.models.generate_images(
                model=self.model,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    output_mime_type="image/png",
                    safety_filter_level="BLOCK_LOW_AND_ABOVE",
                    person_generation="ALLOW_ADULT"
                )
            )
            
            if response.generated_images:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                image = response.generated_images[0].image
                image.save(output_path)
                
                print(f"   [OK] Imagen saved to {output_path}")
                return True
            
            print(f"   [WARN] No image in response")
            return False
                
        except Exception as e:
            print(f"Imagen 生圖失敗: {e}")
        
        return False


class GeminiProImageProvider(ImageProvider):
    """Gemini 3 Pro Image Preview - 支援圖片生成，成本較低"""
    
    def __init__(self, api_key: str, model: str = "gemini-3-pro-image-preview"):
        self.api_key = api_key
        self.model = model
    
    def generate(self, prompt: str, output_path: str, **kwargs) -> bool:
        """使用 Gemini 3 Pro Image Preview 生成圖片"""
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=self.api_key)
            
            # 使用 generate_content 並指定 IMAGE 輸出
            response = client.models.generate_content(
                model=self.model,
                contents=f"Generate an image: {prompt}",
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"]
                )
            )
            
            # 從回應中提取圖片
            if response.candidates:
                for part in response.candidates[0].content.parts:
                    if part.inline_data and part.inline_data.mime_type.startswith('image/'):
                        image_data = part.inline_data.data
                        
                        output_path = Path(output_path)
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        with open(output_path, 'wb') as f:
                            f.write(image_data)
                        
                        print(f"   [OK] Gemini Pro Image saved to {output_path}")
                        return True
            
            print(f"   [WARN] No image in Gemini Pro response")
            return False
                
        except Exception as e:
            print(f"Gemini Pro Image 生圖失敗: {e}")
        
        return False
    
    def generate_img2img(self, prompt: str, reference_path: str, output_path: str,
                         **kwargs) -> bool:
        """使用參考圖生成（圖片編輯）"""
        try:
            from google import genai
            from google.genai import types
            from PIL import Image
            import io
            
            client = genai.Client(api_key=self.api_key)
            
            # 載入參考圖
            ref_image = Image.open(reference_path)
            img_byte_arr = io.BytesIO()
            ref_image.save(img_byte_arr, format='PNG')
            img_bytes = img_byte_arr.getvalue()
            
            response = client.models.generate_content(
                model=self.model,
                contents=[
                    types.Part.from_bytes(data=img_bytes, mime_type="image/png"),
                    f"Edit this image: {prompt}"
                ],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"]
                )
            )
            
            if response.candidates:
                for part in response.candidates[0].content.parts:
                    if part.inline_data and part.inline_data.mime_type.startswith('image/'):
                        image_data = part.inline_data.data
                        
                        output_path = Path(output_path)
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        with open(output_path, 'wb') as f:
                            f.write(image_data)
                        
                        return True
            
            print("   [INFO] 無法編輯圖片，改用生成")
            return self.generate(prompt, output_path, **kwargs)
                
        except Exception as e:
            print(f"Gemini Pro img2img 失敗: {e}")
        
        return False


class ImageGenerator:
    """圖片生成器 - 統一介面，支援角色/場景使用不同 provider"""
    
    def __init__(self, config: dict):
        """
        初始化圖片生成器
        
        Args:
            config: 設定字典
        """
        self.config = config
        img_config = config.get('image_generation', {})
        
        # 支援分離的 provider 設定
        char_provider_name = img_config.get('character_provider', 'gemini_pro_image')
        scene_provider_name = img_config.get('scene_provider', 'stable_diffusion')
        expr_provider_name = img_config.get('expression_provider', 'stable_diffusion')
        
        # 建立 providers
        self.character_provider = self._create_provider(char_provider_name, img_config, config)
        self.scene_provider = self._create_provider(scene_provider_name, img_config, config)
        self.expression_provider = self._create_provider(expr_provider_name, img_config, config)
        
        # 向後兼容：預設使用角色 provider
        self.provider = self.character_provider
        
        # 表情生成設定
        sd_expr_config = img_config.get('stable_diffusion', {}).get('expression', {})
        self.expression_denoising = sd_expr_config.get('denoising_strength', 0.35)
        
        # 視覺風格
        style_config = config.get('visual_style', {})
        self.current_style = style_config.get('current', 'anime')
        self.styles = style_config.get('styles', {})
    
    def _create_provider(self, provider_name: str, img_config: dict, config: dict):
        """建立指定的 provider"""
        if provider_name == 'stable_diffusion':
            sd_config = img_config.get('stable_diffusion', {})
            return StableDiffusionProvider(
                api_url=sd_config.get('api_url', 'http://localhost:7860'),
                defaults=sd_config.get('defaults', {})
            )
        elif provider_name == 'gemini_pro_image':
            # Gemini 3 Pro Image Preview - 推薦用於角色生成
            gemini_config = config.get('ai', {}).get('gemini', {})
            pro_config = img_config.get('gemini_pro_image', {})
            return GeminiProImageProvider(
                api_key=gemini_config.get('api_key', ''),
                model=pro_config.get('model', 'gemini-3-pro-image-preview')
            )
        elif provider_name == 'gemini_imagen':
            # Imagen - 成本較高，備用
            gemini_config = config.get('ai', {}).get('gemini', {})
            imagen_config = img_config.get('gemini_imagen', {})
            return GeminiImagenProvider(
                api_key=gemini_config.get('api_key', ''),
                model=imagen_config.get('model', 'imagen-4.0-generate-001')
            )
        else:
            raise ValueError(f"不支援的圖片提供者: {provider_name}")
    
    def _get_style_suffix(self, style_type: str) -> str:
        """取得風格後綴"""
        style = self.styles.get(self.current_style, {})
        if style_type == 'character':
            return style.get('character_prompt_suffix', '')
        elif style_type == 'scene':
            return style.get('scene_prompt_suffix', '')
        return ''
    
    def generate(self, prompt: str, output_path: str, **kwargs) -> bool:
        """
        生成圖片
        
        Args:
            prompt: 提示詞
            output_path: 輸出路徑
        
        Returns:
            是否成功
        """
        return self.provider.generate(prompt, output_path, **kwargs)
    
    def generate_character(self, character: dict, expression: str,
                          output_path: str, reference: str = None) -> bool:
        """
        生成角色立繪
        
        Args:
            character: 角色資料（需有 name, visual_prompt 或 description）
            expression: 表情
            output_path: 輸出路徑
            reference: 參考圖路徑（可選，用於 img2img）
        
        Returns:
            是否成功
        """
        style_suffix = self._get_style_suffix('character')
        
        # 優先使用 visual_prompt 或 visual_description（AI 生成的視覺描述）
        visual_desc = character.get('visual_prompt', '') or character.get('visual_description', '') or character.get('description', '')
        
        print(f"[DEBUG] generate_character: visual_desc = {visual_desc[:50] if visual_desc else 'EMPTY'}...")
        
        prompt = f"""
        character portrait, {character.get('name', '')}, 
        {visual_desc},
        {expression} expression,
        front facing, upper body, transparent background,
        {style_suffix}
        """.strip()
        
        print(f"[DEBUG] Full prompt: {prompt[:100]}...")
        
        # 如果有參考圖，使用 img2img
        if reference and Path(reference).exists():
            if hasattr(self.character_provider, 'generate_img2img'):
                return self.character_provider.generate_img2img(
                    prompt=prompt,
                    reference_path=reference,
                    output_path=output_path,
                    denoising_strength=0.4,  # 較低的值 = 更像原圖
                    width=512,
                    height=768
                )
        
        # 沒有參考圖，使用角色 provider 生成
        return self.character_provider.generate(
            prompt=prompt,
            output_path=output_path,
            width=512,
            height=768
        )
    
    def generate_character_expression(self, character: dict, expression: str,
                                       reference_path: str, output_path: str) -> bool:
        """
        根據參考圖生成角色表情變化
        
        Args:
            character: 角色資料
            expression: 目標表情
            reference_path: 參考圖路徑（選定的角色基準圖）
            output_path: 輸出路徑
        
        Returns:
            是否成功
        """
        return self.generate_character(
            character=character,
            expression=expression,
            output_path=output_path,
            reference=reference_path
        )
    
    def generate_scene(self, scene: dict, output_path: str) -> bool:
        """
        生成場景背景
        
        Args:
            scene: 場景資料（需有 name, description, mood 等）
            output_path: 輸出路徑
        
        Returns:
            是否成功
        """
        style_suffix = self._get_style_suffix('scene')
        
        # 優先使用 visual_prompt 或 visual_description
        visual_desc = scene.get('visual_prompt', '') or scene.get('visual_description', '') or scene.get('description', '')
        
        prompt = f"""
        background, {scene.get('name', '')},
        {visual_desc},
        {scene.get('time_of_day', 'daytime')},
        {scene.get('mood', '')} atmosphere,
        no characters, no people,
        {style_suffix}
        """.strip()
        
        print(f"[DEBUG] generate_scene: using scene_provider")
        
        # 使用場景 provider 生成（適合 SD 的 16:9 尺寸）
        # 1024x576 適合大部分 SD 模型，之後可以放大
        return self.scene_provider.generate(
            prompt=prompt,
            output_path=output_path,
            width=1024,
            height=576
        )
    
    def set_style(self, style_name: str) -> None:
        """設定視覺風格"""
        if style_name in self.styles:
            self.current_style = style_name
        else:
            raise ValueError(f"不支援的風格: {style_name}")
