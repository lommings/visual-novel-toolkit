#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""設定管理模組"""

import json
from pathlib import Path
from typing import Any, Optional


class ConfigManager:
    """設定管理器 - 單例模式"""
    
    _instance = None
    _config = None
    _config_path = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def load(cls, config_path: str = None) -> dict:
        """
        載入設定檔
        
        Args:
            config_path: 設定檔路徑，預設為專案根目錄的 config.json
        
        Returns:
            設定字典
        """
        if config_path is None:
            # 預設路徑：專案根目錄
            config_path = Path(__file__).parent.parent / 'config.json'
        
        cls._config_path = Path(config_path)
        
        if not cls._config_path.exists():
            # 建立預設設定
            cls._config = cls._get_default_config()
            cls.save()
        else:
            with open(cls._config_path, 'r', encoding='utf-8') as f:
                cls._config = json.load(f)
        
        return cls._config
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        取得設定值，支援點號分隔的路徑
        
        Args:
            key: 設定鍵，如 'ai.gemini.api_key'
            default: 找不到時的預設值
        
        Returns:
            設定值
        """
        if cls._config is None:
            cls.load()
        
        keys = key.split('.')
        value = cls._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """
        設定值
        
        Args:
            key: 設定鍵
            value: 設定值
        """
        if cls._config is None:
            cls.load()
        
        keys = key.split('.')
        config = cls._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    @classmethod
    def save(cls, config_path: str = None) -> None:
        """儲存設定檔"""
        if config_path:
            cls._config_path = Path(config_path)
        
        if cls._config_path and cls._config:
            with open(cls._config_path, 'w', encoding='utf-8') as f:
                json.dump(cls._config, f, ensure_ascii=False, indent=2)
    
    @classmethod
    def _get_default_config(cls) -> dict:
        """取得預設設定"""
        return {
            "version": "1.0",
            
            "ai": {
                "provider": "gemini",
                "gemini": {
                    "api_key": "",
                    "model": "gemini-3-flash-preview"
                },
                "openai": {
                    "api_key": "",
                    "model": "gpt-4"
                }
            },
            
            "image_generation": {
                "provider": "stable_diffusion",
                "stable_diffusion": {
                    "api_url": "http://localhost:7860",
                    "default_model": "animagine-xl",
                    "defaults": {
                        "steps": 30,
                        "cfg_scale": 7.5,
                        "width": 512,
                        "height": 768
                    }
                },
                "gemini_imagen": {
                    "model": "gemini-3-pro-image-preview"
                }
            },
            
            "visual_style": {
                "current": "anime",
                "styles": {
                    "anime": {
                        "name": "動漫風格",
                        "character_prompt_suffix": "anime style, visual novel sprite, detailed, transparent background",
                        "scene_prompt_suffix": "anime style, detailed background, visual novel, no characters"
                    },
                    "semi_realistic": {
                        "name": "半寫實",
                        "character_prompt_suffix": "semi-realistic, detailed portrait, soft lighting",
                        "scene_prompt_suffix": "semi-realistic, cinematic lighting, detailed environment"
                    }
                }
            },
            
            "novel_to_twee": {
                "default_branches": 2,
                "min_passage_length": 100,
                "max_passage_length": 500,
                "language": "zh-TW"
            },
            
            "twee_processor": {
                "max_line_length": 50,
                "split_on_punctuation": True,
                "detect_dialogue": True,
                "default_expression": "normal"
            },
            
            "asset_previewer": {
                "character_concepts_count": 4,
                "scene_concepts_count": 3,
                "preview_port": 8080,
                "auto_open_browser": True
            },
            
            "game_assembler": {
                "engine_template": "templates/monogatari",
                "default_text_speed": 30,
                "auto_save_interval": 10000
            },
            
            "paths": {
                "output_dir": "output",
                "preview_dir": "preview",
                "templates_dir": "templates"
            }
        }
    
    @classmethod
    def get_config(cls) -> dict:
        """取得完整設定"""
        if cls._config is None:
            cls.load()
        return cls._config


# 便捷函式
def get_config() -> dict:
    """取得設定"""
    return ConfigManager.get_config()

def get_setting(key: str, default: Any = None) -> Any:
    """取得單一設定值"""
    return ConfigManager.get(key, default)
