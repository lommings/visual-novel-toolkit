#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI API 封裝模組 - 支援 Context Caching"""

import json
import re
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class AIProvider(ABC):
    """AI 提供者抽象類別"""
    
    @abstractmethod
    def analyze(self, prompt: str, system_prompt: Optional[str] = None) -> dict:
        """發送分析請求，返回 JSON"""
        pass
    
    @abstractmethod
    def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """生成文字"""
        pass


class GeminiProvider(AIProvider):
    """Gemini API 提供者 - 支援 Context Caching"""
    
    # 預設的 System Prompts（可被快取）
    SYSTEM_PROMPTS = {
        'story_analyzer': '''你是一位專業的視覺小說編劇和故事分析師。
你的任務是分析小說文字，識別：
1. 主要角色及其特徵
2. 重要場景和地點
3. 對話和敘述
4. 故事分支點

請用繁體中文回答，並以 JSON 格式輸出結果。''',

        'scene_detector': '''你是一位視覺小說場景設計師。
你的任務是：
1. 從文字描述中識別場景變化
2. 為每個場景生成適合的視覺描述
3. 建議場景的氛圍和光線

請用繁體中文回答，並以 JSON 格式輸出結果。''',

        'character_analyzer': '''你是一位角色設計專家。
你的任務是：
1. 分析角色的外貌特徵
2. 識別角色的性格和情緒
3. 建議角色的視覺設計方向

請用繁體中文回答，並以 JSON 格式輸出結果。''',

        'dialogue_parser': '''你是一位對話分析專家。
你的任務是：
1. 識別說話者
2. 分析對話的情緒
3. 標記重要的劇情對話

請用繁體中文回答，並以 JSON 格式輸出結果。''',
    }
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash", 
                 cache_dir: Optional[Path] = None,
                 cache_ttl_minutes: int = 60):
        """
        初始化 Gemini Provider
        
        Args:
            api_key: Gemini API 金鑰
            model: 模型名稱
            cache_dir: 快取目錄（用於本地追蹤快取狀態）
            cache_ttl_minutes: 快取 TTL（分鐘）
        """
        self.api_key = api_key
        self.model = model
        self.cache_dir = cache_dir or Path.home() / '.cache' / 'visual-novel-toolkit'
        self.cache_ttl = timedelta(minutes=cache_ttl_minutes)
        self._client = None
        self._genai = None
        self._cached_contents: Dict[str, Any] = {}  # cache_name -> CachedContent
        
        # 確保快取目錄存在
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_client(self):
        """延遲初始化 Gemini 客戶端"""
        if self._client is None:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._genai = genai
                self._client = genai.GenerativeModel(self.model)
            except ImportError:
                raise ImportError("請安裝 google-generativeai: pip install google-generativeai")
        return self._client
    
    def _get_cache_key(self, content: str) -> str:
        """計算內容的快取鍵"""
        return hashlib.md5(content.encode('utf-8')).hexdigest()[:16]
    
    def _load_cache_registry(self) -> dict:
        """載入快取註冊表"""
        registry_path = self.cache_dir / 'cache_registry.json'
        if registry_path.exists():
            try:
                with open(registry_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_cache_registry(self, registry: dict):
        """儲存快取註冊表"""
        registry_path = self.cache_dir / 'cache_registry.json'
        with open(registry_path, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)
    
    def create_cached_content(self, name: str, content: str, ttl_minutes: Optional[int] = None) -> Any:
        """
        建立或取得快取內容
        
        Args:
            name: 快取名稱（如 'story_analyzer'）
            content: 要快取的內容（通常是 system prompt）
            ttl_minutes: 快取 TTL（分鐘），None 使用預設值
        
        Returns:
            CachedContent 物件
        """
        self._get_client()  # 確保初始化
        
        cache_key = self._get_cache_key(content)
        full_name = f"{name}_{cache_key}"
        
        # 檢查本地註冊表
        registry = self._load_cache_registry()
        
        if full_name in registry:
            cache_info = registry[full_name]
            expire_time = datetime.fromisoformat(cache_info['expire_time'])
            
            if datetime.now() < expire_time:
                # 快取仍有效，嘗試取得
                try:
                    cached = self._genai.caching.CachedContent.get(cache_info['cache_name'])
                    self._cached_contents[name] = cached
                    print(f"[Cache] 使用現有快取: {name}")
                    return cached
                except Exception as e:
                    print(f"[Cache] 快取已過期或不存在: {e}")
                    del registry[full_name]
                    self._save_cache_registry(registry)
        
        # 建立新快取
        try:
            ttl = timedelta(minutes=ttl_minutes) if ttl_minutes else self.cache_ttl
            
            cached = self._genai.caching.CachedContent.create(
                model=self.model,
                display_name=full_name,
                system_instruction=content,
                ttl=ttl
            )
            
            # 儲存到註冊表
            registry[full_name] = {
                'cache_name': cached.name,
                'expire_time': (datetime.now() + ttl).isoformat(),
                'content_hash': cache_key
            }
            self._save_cache_registry(registry)
            
            self._cached_contents[name] = cached
            print(f"[Cache] 建立新快取: {name} (TTL: {ttl})")
            return cached
            
        except Exception as e:
            print(f"[Cache] 建立快取失敗: {e}")
            print(f"[Cache] 將使用一般模式（無快取）")
            return None
    
    def get_cached_model(self, cache_name: str) -> Any:
        """
        取得使用特定快取的模型
        
        Args:
            cache_name: 快取名稱
        
        Returns:
            GenerativeModel 或 None
        """
        if cache_name not in self._cached_contents:
            # 嘗試建立預設快取
            if cache_name in self.SYSTEM_PROMPTS:
                self.create_cached_content(cache_name, self.SYSTEM_PROMPTS[cache_name])
        
        cached = self._cached_contents.get(cache_name)
        if cached:
            return self._genai.GenerativeModel.from_cached_content(cached)
        return None
    
    def generate_text(self, prompt: str, system_prompt: Optional[str] = None, 
                      cache_name: Optional[str] = None) -> str:
        """
        生成文字
        
        Args:
            prompt: 使用者提示詞
            system_prompt: 系統提示詞（如果提供，會嘗試快取）
            cache_name: 使用的快取名稱（優先於 system_prompt）
        
        Returns:
            生成的文字
        """
        # 優先使用指定的快取
        if cache_name:
            model = self.get_cached_model(cache_name)
            if model:
                response = model.generate_content(prompt)
                return response.text
        
        # 如果有 system_prompt，嘗試快取
        if system_prompt:
            cache_key = self._get_cache_key(system_prompt)
            cached_model = self.get_cached_model(f"custom_{cache_key}")
            
            if not cached_model:
                # 建立新快取
                self.create_cached_content(f"custom_{cache_key}", system_prompt)
                cached_model = self.get_cached_model(f"custom_{cache_key}")
            
            if cached_model:
                response = cached_model.generate_content(prompt)
                return response.text
        
        # 無快取，使用一般模式
        client = self._get_client()
        
        if system_prompt:
            # 使用 system_instruction
            model = self._genai.GenerativeModel(
                self.model,
                system_instruction=system_prompt
            )
            response = model.generate_content(prompt)
        else:
            response = client.generate_content(prompt)
        
        return response.text
    
    def analyze(self, prompt: str, system_prompt: Optional[str] = None,
                cache_name: Optional[str] = None) -> dict:
        """
        發送分析請求，返回 JSON
        
        Args:
            prompt: 使用者提示詞
            system_prompt: 系統提示詞
            cache_name: 使用的快取名稱
        
        Returns:
            解析後的 JSON 字典
        """
        text = self.generate_text(prompt, system_prompt, cache_name)
        return self._extract_json(text)
    
    def analyze_story(self, story_text: str) -> dict:
        """分析故事（使用快取的 story_analyzer 系統提示）"""
        return self.analyze(
            f"請分析以下故事：\n\n{story_text}",
            cache_name='story_analyzer'
        )
    
    def detect_scenes(self, text: str) -> dict:
        """偵測場景（使用快取的 scene_detector 系統提示）"""
        return self.analyze(
            f"請分析以下文字中的場景：\n\n{text}",
            cache_name='scene_detector'
        )
    
    def analyze_characters(self, text: str) -> dict:
        """分析角色（使用快取的 character_analyzer 系統提示）"""
        return self.analyze(
            f"請分析以下文字中的角色：\n\n{text}",
            cache_name='character_analyzer'
        )
    
    def parse_dialogue(self, text: str) -> dict:
        """解析對話（使用快取的 dialogue_parser 系統提示）"""
        return self.analyze(
            f"請分析以下對話：\n\n{text}",
            cache_name='dialogue_parser'
        )
    
    def clear_cache(self, name: Optional[str] = None):
        """
        清除快取
        
        Args:
            name: 要清除的快取名稱，None 清除全部
        """
        registry = self._load_cache_registry()
        
        if name:
            # 清除特定快取
            keys_to_remove = [k for k in registry if k.startswith(name)]
            for key in keys_to_remove:
                try:
                    cache_info = registry[key]
                    cached = self._genai.caching.CachedContent.get(cache_info['cache_name'])
                    cached.delete()
                    print(f"[Cache] 已刪除: {key}")
                except Exception as e:
                    print(f"[Cache] 刪除失敗 {key}: {e}")
                del registry[key]
        else:
            # 清除全部
            for key, cache_info in list(registry.items()):
                try:
                    cached = self._genai.caching.CachedContent.get(cache_info['cache_name'])
                    cached.delete()
                    print(f"[Cache] 已刪除: {key}")
                except Exception as e:
                    print(f"[Cache] 刪除失敗 {key}: {e}")
            registry.clear()
        
        self._save_cache_registry(registry)
        self._cached_contents.clear()
    
    def list_caches(self) -> list:
        """列出所有快取"""
        registry = self._load_cache_registry()
        result = []
        
        for name, info in registry.items():
            expire_time = datetime.fromisoformat(info['expire_time'])
            is_valid = datetime.now() < expire_time
            result.append({
                'name': name,
                'expire_time': info['expire_time'],
                'is_valid': is_valid,
                'cache_name': info['cache_name']
            })
        
        return result
    
    def _extract_json(self, text: str) -> dict:
        """從文字中提取 JSON"""
        # 嘗試直接解析
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # 嘗試找 JSON 區塊
        patterns = [
            r'```json\s*([\s\S]*?)\s*```',
            r'```\s*([\s\S]*?)\s*```',
            r'\{[\s\S]*\}'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    json_str = match.group(1) if '```' in pattern else match.group(0)
                    return json.loads(json_str)
                except (json.JSONDecodeError, IndexError):
                    continue
        
        # 返回空字典
        return {}


class OpenAIProvider(AIProvider):
    """OpenAI API 提供者"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self._client = None
    
    def _get_client(self):
        """延遲初始化 OpenAI 客戶端"""
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key)
            except ImportError:
                raise ImportError("請安裝 openai: pip install openai")
        return self._client
    
    def generate_text(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """生成文字"""
        client = self._get_client()
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content
    
    def analyze(self, prompt: str, system_prompt: Optional[str] = None) -> dict:
        """發送分析請求，返回 JSON"""
        # 加入 JSON 格式提示
        json_prompt = prompt + "\n\n請用 JSON 格式回答。"
        text = self.generate_text(json_prompt, system_prompt)
        return self._extract_json(text)
    
    def _extract_json(self, text: str) -> dict:
        """從文字中提取 JSON"""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        
        # 嘗試找 JSON 區塊
        match = re.search(r'```json\s*([\s\S]*?)\s*```', text)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
        
        return {}


class AIClient:
    """AI 客戶端 - 統一介面"""
    
    def __init__(self, config: dict):
        """
        初始化 AI 客戶端
        
        Args:
            config: 設定字典，需包含 'ai' 區塊
        """
        ai_config = config.get('ai', {})
        provider_name = ai_config.get('provider', 'gemini')
        
        # 快取設定
        cache_config = ai_config.get('cache', {})
        cache_enabled = cache_config.get('enabled', True)
        cache_ttl = cache_config.get('ttl_minutes', 60)
        
        if provider_name == 'gemini':
            gemini_config = ai_config.get('gemini', {})
            self.provider = GeminiProvider(
                api_key=gemini_config.get('api_key', ''),
                model=gemini_config.get('model', 'gemini-2.0-flash'),
                cache_ttl_minutes=cache_ttl if cache_enabled else 0
            )
        elif provider_name == 'openai':
            openai_config = ai_config.get('openai', {})
            self.provider = OpenAIProvider(
                api_key=openai_config.get('api_key', ''),
                model=openai_config.get('model', 'gpt-4')
            )
        else:
            raise ValueError(f"不支援的 AI 提供者: {provider_name}")
        
        self._cache_enabled = cache_enabled
    
    def analyze(self, prompt: str, system_prompt: Optional[str] = None,
                cache_name: Optional[str] = None) -> dict:
        """
        發送分析請求
        
        Args:
            prompt: 提示詞
            system_prompt: 系統提示詞
            cache_name: 快取名稱（僅 Gemini）
        
        Returns:
            解析後的 JSON 字典
        """
        if isinstance(self.provider, GeminiProvider):
            return self.provider.analyze(prompt, system_prompt, cache_name)
        return self.provider.analyze(prompt, system_prompt)
    
    def generate_text(self, prompt: str, system_prompt: Optional[str] = None,
                      cache_name: Optional[str] = None) -> str:
        """
        生成文字
        
        Args:
            prompt: 提示詞
            system_prompt: 系統提示詞
            cache_name: 快取名稱（僅 Gemini）
        
        Returns:
            生成的文字
        """
        if isinstance(self.provider, GeminiProvider):
            return self.provider.generate_text(prompt, system_prompt, cache_name)
        return self.provider.generate_text(prompt, system_prompt)
    
    # 便捷方法（使用預設快取）
    def analyze_story(self, story_text: str) -> dict:
        """分析故事"""
        if isinstance(self.provider, GeminiProvider):
            return self.provider.analyze_story(story_text)
        return self.analyze(f"請分析以下故事：\n\n{story_text}")
    
    def detect_scenes(self, text: str) -> dict:
        """偵測場景"""
        if isinstance(self.provider, GeminiProvider):
            return self.provider.detect_scenes(text)
        return self.analyze(f"請分析場景：\n\n{text}")
    
    def analyze_characters(self, text: str) -> dict:
        """分析角色"""
        if isinstance(self.provider, GeminiProvider):
            return self.provider.analyze_characters(text)
        return self.analyze(f"請分析角色：\n\n{text}")
    
    # 快取管理
    def clear_cache(self, name: Optional[str] = None):
        """清除快取"""
        if isinstance(self.provider, GeminiProvider):
            self.provider.clear_cache(name)
    
    def list_caches(self) -> list:
        """列出快取"""
        if isinstance(self.provider, GeminiProvider):
            return self.provider.list_caches()
        return []
