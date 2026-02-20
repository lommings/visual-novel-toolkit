#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 成本分析工具
分析專案的 API 使用情況，找出成本來源
"""

import json
import re
from pathlib import Path
from collections import defaultdict


# Gemini API 價格表（美金，2024 年）
PRICING = {
    # === 圖片生成 (最貴！) ===
    'imagen-4.0-generate-001': {
        'per_image': 0.05,  # ~$0.04-0.06
        'type': 'image',
        'description': 'Imagen 4 圖片生成'
    },
    'imagen-3.0-generate-002': {
        'per_image': 0.04,
        'type': 'image',
        'description': 'Imagen 3 圖片生成'
    },
    'gemini-3-pro-image-preview': {
        'per_image': 0.03,  # 包含輸入+輸出圖片
        'type': 'image',
        'description': 'Gemini 3 Pro 圖片生成/編輯'
    },
    
    # === 文字生成 (便宜) ===
    'gemini-3-flash-preview': {
        'input_per_1m': 0.075,
        'output_per_1m': 0.30,
        'type': 'text',
        'description': 'Gemini 3 Flash 文字'
    },
    'gemini-2.0-flash': {
        'input_per_1m': 0.075,
        'output_per_1m': 0.30,
        'type': 'text',
        'description': 'Gemini 2.0 Flash 文字'
    },
    'gemini-2.0-flash-exp': {
        'input_per_1m': 0.075,
        'output_per_1m': 0.30,
        'type': 'text',
        'description': 'Gemini 2.0 Flash Exp 文字'
    },
}


def analyze_project_structure():
    """分析專案結構，找出 API 調用位置"""
    
    project_dir = Path(".")
    api_calls = defaultdict(list)
    
    # 掃描所有 Python 檔案
    for py_file in project_dir.rglob("*.py"):
        if '__pycache__' in str(py_file):
            continue
            
        try:
            content = py_file.read_text(encoding='utf-8')
        except:
            continue
        
        # 檢查圖片生成
        if 'generate_images' in content or 'imagen' in content.lower():
            # 找出使用的模型
            for model in ['imagen-4.0-generate-001', 'imagen-3.0-generate-002']:
                if model in content:
                    api_calls['imagen'].append({
                        'file': str(py_file),
                        'model': model,
                        'type': 'image'
                    })
        
        # 檢查 Gemini 圖片編輯
        if 'gemini-3-pro-image-preview' in content:
            api_calls['gemini_image'].append({
                'file': str(py_file),
                'model': 'gemini-3-pro-image-preview',
                'type': 'image'
            })
        
        # 檢查文字生成
        if 'generate_content' in content or 'GenerativeModel' in content:
            for model in ['gemini-3-flash-preview', 'gemini-2.0-flash', 'gemini-2.0-flash-exp']:
                if model in content:
                    api_calls['gemini_text'].append({
                        'file': str(py_file),
                        'model': model,
                        'type': 'text'
                    })
    
    return api_calls


def estimate_costs_per_workflow():
    """估算每個工作流程的成本"""
    
    print("=" * 70)
    print("📊 Visual Novel Toolkit - API 成本分析")
    print("=" * 70)
    
    # 讀取 config
    config_path = Path("config.json")
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        config = {}
    
    print("\n📋 專案配置:")
    print("-" * 50)
    
    # AI 配置
    ai_config = config.get('ai', {})
    print(f"   文字模型: {ai_config.get('gemini', {}).get('model', 'unknown')}")
    
    # 圖片配置
    img_config = config.get('image_generation', {})
    print(f"   角色圖片: {img_config.get('character_provider', 'unknown')}")
    print(f"   場景圖片: {img_config.get('scene_provider', 'unknown')}")
    
    imagen_model = img_config.get('gemini_imagen', {}).get('model', 'imagen-4.0-generate-001')
    print(f"   Imagen 模型: {imagen_model}")
    
    # 分析 API 調用位置
    print("\n📍 API 調用位置:")
    print("-" * 50)
    
    api_calls = analyze_project_structure()
    
    for category, calls in api_calls.items():
        print(f"\n   {category}:")
        files = set(c['file'] for c in calls)
        for f in files:
            print(f"      - {f}")
    
    # 估算單次工作流程成本
    print("\n💰 單次工作流程成本估算:")
    print("-" * 50)
    
    # 假設一個典型的視覺小說專案
    # 2 個角色 x 5 種表情 = 10 張角色圖
    # 5 個場景 = 5 張場景圖
    # 多次文字分析
    
    scenarios = [
        {
            'name': '小型專案 (2 角色, 5 場景)',
            'character_images': 2 * 5,  # 2 角色 x 5 表情
            'scene_images': 5,
            'text_calls': 10,
        },
        {
            'name': '中型專案 (4 角色, 10 場景)',
            'character_images': 4 * 5,
            'scene_images': 10,
            'text_calls': 20,
        },
        {
            'name': '大型專案 (8 角色, 20 場景)',
            'character_images': 8 * 5,
            'scene_images': 20,
            'text_calls': 40,
        }
    ]
    
    imagen_price = PRICING.get(imagen_model, {}).get('per_image', 0.05)
    gemini_img_price = PRICING.get('gemini-3-pro-image-preview', {}).get('per_image', 0.03)
    
    for scenario in scenarios:
        print(f"\n   📁 {scenario['name']}:")
        
        # 角色圖片成本 (Imagen)
        char_cost = scenario['character_images'] * imagen_price
        print(f"      角色立繪: {scenario['character_images']} 張 x ${imagen_price} = ${char_cost:.2f}")
        
        # 表情變化 (Gemini Pro Image)
        # 假設每個角色 normal 用原圖，其他 4 種表情用 Gemini 生成
        expr_count = scenario['character_images'] - (scenario['character_images'] // 5)
        expr_cost = expr_count * gemini_img_price
        print(f"      表情變化: {expr_count} 張 x ${gemini_img_price} = ${expr_cost:.2f}")
        
        # 場景圖片 (SD = 免費)
        scene_cost = 0
        print(f"      場景背景: {scenario['scene_images']} 張 (SD 免費)")
        
        # 文字分析
        text_cost = scenario['text_calls'] * 0.001  # 估計每次 $0.001
        print(f"      文字分析: {scenario['text_calls']} 次 = ${text_cost:.3f}")
        
        total = char_cost + expr_cost + scene_cost + text_cost
        print(f"      ────────────────────")
        print(f"      💵 總計: ${total:.2f}")
    
    # 反推 $62/天 的使用量
    print("\n🔍 反推 $62/天 的使用情況:")
    print("-" * 50)
    
    daily_cost = 62.0
    
    # 假設全部是 Imagen 圖片
    imagen_only = daily_cost / imagen_price
    print(f"   如果全是 Imagen 4 圖片: {imagen_only:.0f} 張/天")
    
    # 假設全部是 Gemini Pro Image
    gemini_img_only = daily_cost / gemini_img_price
    print(f"   如果全是 Gemini Pro 圖片: {gemini_img_only:.0f} 張/天")
    
    # 混合情況
    print(f"\n   🎯 最可能的情況:")
    print(f"      - Imagen 角色生成: 約 500-800 張/天")
    print(f"      - 或 Gemini 表情生成: 約 1000-1500 張/天")
    print(f"      - 可能在重複生成角色/表情")
    
    # 建議
    print("\n💡 成本優化建議:")
    print("-" * 50)
    print("""
   🔴 最大成本來源: 圖片生成 (Imagen 4 / Gemini Pro Image)
   
   優化方案:
   
   1. 【減少生成次數】
      - 檢查是否有重複生成同樣的圖片
      - 快取已生成的圖片，避免重複調用 API
   
   2. 【使用更便宜的模型】
      - Imagen 3 比 Imagen 4 便宜 ~20%
      - 或考慮用 Stable Diffusion 生成角色（免費）
   
   3. 【減少表情數量】
      - 標準 5 種表情 (normal, happy, sad, angry, surprised)
      - 不需要的表情可以跳過
   
   4. 【使用 SD 生成角色】
      - 修改 config.json:
        "character_provider": "stable_diffusion"
      - 完全免費，但風格可能需要調整
   
   5. 【本地快取】
      - 確保已生成的圖片有正確快取
      - 避免同一個角色/表情重複生成
""")
    
    print("\n" + "=" * 70)


def check_output_directories():
    """檢查輸出目錄，統計生成的圖片數量"""
    
    print("\n📂 檢查已生成的圖片:")
    print("-" * 50)
    
    output_dir = Path("output")
    if not output_dir.exists():
        print("   找不到 output 目錄")
        return
    
    total_images = 0
    
    for project_dir in output_dir.iterdir():
        if not project_dir.is_dir():
            continue
            
        print(f"\n   📁 {project_dir.name}:")
        
        # 統計各類型圖片
        for category in ['characters', 'scenes', 'preview']:
            category_dir = project_dir / category
            if category_dir.exists():
                images = list(category_dir.rglob("*.png")) + list(category_dir.rglob("*.jpg"))
                count = len(images)
                total_images += count
                print(f"      {category}: {count} 張")
    
    print(f"\n   📊 總計: {total_images} 張圖片")
    
    # 估算成本
    imagen_cost = total_images * 0.05
    print(f"   💰 如果全用 Imagen 4: ${imagen_cost:.2f}")


def main():
    """主程式"""
    print("\n[ANALYSIS] Visual Novel Toolkit - API Cost Analysis Tool")
    print("=" * 70)
    
    # 估算成本
    estimate_costs_per_workflow()
    
    # 檢查已生成的圖片
    check_output_directories()
    
    print("\n✅ 分析完成！")
    print("\n建議下一步:")
    print("   1. 執行 python cost_tracker.py --breakdown 查看詳細成本分類")
    print("   2. 檢查是否有重複生成的圖片")
    print("   3. 考慮將角色生成改用 Stable Diffusion（免費）")
    print()


if __name__ == '__main__':
    main()
