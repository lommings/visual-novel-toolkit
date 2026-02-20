#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快取管理工具

用法:
    python manage_cache.py list          # 列出所有快取
    python manage_cache.py clear         # 清除所有快取
    python manage_cache.py clear <name>  # 清除特定快取
    python manage_cache.py init          # 初始化預設快取
    python manage_cache.py status        # 顯示快取狀態和節省估算
"""

import sys
import json
from pathlib import Path

# 加入專案路徑
sys.path.insert(0, str(Path(__file__).parent))

from shared.ai_client import AIClient, GeminiProvider


def load_config():
    """載入設定"""
    config_path = Path(__file__).parent / 'config.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def list_caches():
    """列出所有快取"""
    config = load_config()
    client = AIClient(config)
    
    caches = client.list_caches()
    
    if not caches:
        print("目前沒有任何快取")
        return
    
    print("\n📦 快取列表:")
    print("-" * 60)
    
    for cache in caches:
        status = "✅ 有效" if cache['is_valid'] else "❌ 已過期"
        print(f"  {cache['name']}")
        print(f"    狀態: {status}")
        print(f"    過期時間: {cache['expire_time']}")
        print()


def clear_caches(name=None):
    """清除快取"""
    config = load_config()
    client = AIClient(config)
    
    if name:
        print(f"正在清除快取: {name}")
        client.clear_cache(name)
        print("完成！")
    else:
        print("正在清除所有快取...")
        client.clear_cache()
        print("完成！所有快取已清除")


def init_caches():
    """初始化預設快取"""
    config = load_config()
    
    if config.get('ai', {}).get('provider') != 'gemini':
        print("Context Caching 目前只支援 Gemini")
        return
    
    gemini_config = config.get('ai', {}).get('gemini', {})
    cache_config = config.get('ai', {}).get('cache', {})
    
    provider = GeminiProvider(
        api_key=gemini_config.get('api_key', ''),
        model=gemini_config.get('model', 'gemini-3-flash-preview'),
        cache_ttl_minutes=cache_config.get('ttl_minutes', 60)
    )
    
    print("正在初始化預設快取...")
    print()
    
    for name, prompt in GeminiProvider.SYSTEM_PROMPTS.items():
        print(f"  建立快取: {name}")
        try:
            provider.create_cached_content(name, prompt)
            print(f"    ✅ 成功")
        except Exception as e:
            print(f"    ❌ 失敗: {e}")
    
    print()
    print("初始化完成！")


def show_status():
    """顯示快取狀態"""
    config = load_config()
    client = AIClient(config)
    
    caches = client.list_caches()
    valid_count = sum(1 for c in caches if c['is_valid'])
    
    print("\n📊 Context Caching 狀態")
    print("=" * 60)
    
    cache_enabled = config.get('ai', {}).get('cache', {}).get('enabled', True)
    print(f"  快取功能: {'✅ 啟用' if cache_enabled else '❌ 停用'}")
    print(f"  有效快取: {valid_count} 個")
    print(f"  總快取數: {len(caches)} 個")
    
    print()
    print("💰 成本節省說明:")
    print("-" * 60)
    print("  Context Caching 可以大幅降低重複使用相同 System Prompt 的成本")
    print()
    print("  Gemini 定價 (2024):")
    print("    - 一般輸入: $0.075 / 1M tokens")
    print("    - 快取輸入: $0.01875 / 1M tokens (節省 75%)")
    print("    - 快取儲存: $1.00 / 1M tokens / 小時")
    print()
    print("  建議:")
    print("    - 對於重複的分析任務，使用預設的 cache_name")
    print("    - TTL 設定根據使用頻率調整（預設 60 分鐘）")
    print("    - 不常用的快取會自動過期，無需手動清理")
    print()
    
    if caches:
        print("目前快取:")
        for cache in caches:
            status = "✅" if cache['is_valid'] else "❌"
            print(f"    {status} {cache['name']}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        list_caches()
    elif command == 'clear':
        name = sys.argv[2] if len(sys.argv) > 2 else None
        clear_caches(name)
    elif command == 'init':
        init_caches()
    elif command == 'status':
        show_status()
    else:
        print(f"未知命令: {command}")
        print(__doc__)


if __name__ == '__main__':
    main()
