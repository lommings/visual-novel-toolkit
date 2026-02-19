#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AI API 封裝模組"""

import json
import re
from typing import Optional
from abc import ABC, abstractmethod


class AIProvider(ABC):
    """AI 提供者抽象類別"""
    
    @abstractmethod
    def analyze(self, prompt: str) -> dict:
        """發送分析請求，返回 JSON"""
        pass
    
    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """生成文字"""
        pass


class GeminiProvider(AIProvider):
    """Gemini API 提供者"""
    
    def __init__(self, api_key: str, model: str = "gemini-3-flash-preview"):
        self.api_key = api_key
        self.model = model
        self._client = None
    
    def _get_client(self):
        """延遲初始化 Gemini 客戶端"""
        if self._client is None:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._client = genai.GenerativeModel(self.model)
            except ImportError:
                raise ImportError("請安裝 google-generativeai: pip install google-generativeai")
        return self._client
    
    def generate_text(self, prompt: str) -> str:
        """生成文字"""
        client = self._get_client()
        response = client.generate_content(prompt)
        return response.text
    
    def analyze(self, prompt: str) -> dict:
        """
        發送分析請求，返回 JSON
        會自動從回應中提取 JSON
        """
        text = self.generate_text(prompt)
        return self._extract_json(text)
    
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
    
    def generate_text(self, prompt: str) -> str:
        """生成文字"""
        client = self._get_client()
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    def analyze(self, prompt: str) -> dict:
        """發送分析請求，返回 JSON"""
        # 加入 JSON 格式提示
        json_prompt = prompt + "\n\n請用 JSON 格式回答。"
        text = self.generate_text(json_prompt)
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
        
        if provider_name == 'gemini':
            gemini_config = ai_config.get('gemini', {})
            self.provider = GeminiProvider(
                api_key=gemini_config.get('api_key', ''),
                model=gemini_config.get('model', 'gemini-3-flash-preview')
            )
        elif provider_name == 'openai':
            openai_config = ai_config.get('openai', {})
            self.provider = OpenAIProvider(
                api_key=openai_config.get('api_key', ''),
                model=openai_config.get('model', 'gpt-4')
            )
        else:
            raise ValueError(f"不支援的 AI 提供者: {provider_name}")
    
    def analyze(self, prompt: str) -> dict:
        """
        發送分析請求
        
        Args:
            prompt: 提示詞
        
        Returns:
            解析後的 JSON 字典
        """
        return self.provider.analyze(prompt)
    
    def generate_text(self, prompt: str) -> str:
        """
        生成文字
        
        Args:
            prompt: 提示詞
        
        Returns:
            生成的文字
        """
        return self.provider.generate_text(prompt)
