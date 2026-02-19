#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Game Assembler - 遊戲組裝工具

將處理好的文字資料與素材組合，輸出完整的 Monogatari 遊戲。
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.config_manager import ConfigManager
from shared.file_utils import load_json, ensure_dir

from monogatari_exporter import MonogatariExporter


def main():
    """主程式"""
    parser = argparse.ArgumentParser(
        description='組合文字與素材，輸出 Monogatari 遊戲'
    )
    parser.add_argument('input', help='processed.json 路徑')
    parser.add_argument('-a', '--assets', help='素材目錄', default=None)
    parser.add_argument('-o', '--output', help='輸出目錄', default=None)
    parser.add_argument('-t', '--template', help='Monogatari 模板目錄', default=None)
    parser.add_argument('-c', '--config', help='設定檔路徑', default=None)
    parser.add_argument('--title', help='遊戲標題', default=None)
    parser.add_argument('--no-engine', action='store_true', 
                       help='不複製引擎檔案（適用於已有引擎的情況）')
    
    args = parser.parse_args()
    
    # 載入設定
    config = ConfigManager.load(args.config)
    
    # 讀取處理後的資料
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ 檔案不存在: {input_path}")
        sys.exit(1)
    
    print(f"📖 讀取資料: {input_path.name}")
    processed_data = load_json(input_path)
    
    # 覆蓋標題
    if args.title:
        processed_data['title'] = args.title
    
    title = processed_data.get('title', input_path.stem)
    characters = processed_data.get('characters', [])
    scenes = processed_data.get('scenes', [])
    passages = processed_data.get('passages', [])
    
    print(f"   標題: {title}")
    print(f"   角色: {len(characters)} 人")
    print(f"   場景: {len(scenes)} 個")
    print(f"   段落: {len(passages)} 個")
    
    # 決定素材目錄
    if args.assets:
        assets_dir = Path(args.assets)
    else:
        assets_dir = input_path.parent / 'assets'
    
    if not assets_dir.exists():
        print(f"⚠️ 素材目錄不存在: {assets_dir}")
        print("   遊戲將沒有圖片")
    else:
        # 檢查素材
        chars_count = len(list((assets_dir / 'characters').glob('*'))) if (assets_dir / 'characters').exists() else 0
        scenes_count = len(list((assets_dir / 'scenes').glob('*'))) if (assets_dir / 'scenes').exists() else 0
        print(f"\n📁 素材目錄: {assets_dir}")
        print(f"   角色資料夾: {chars_count} 個")
        print(f"   場景圖片: {scenes_count} 個")
    
    # 決定輸出目錄
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = input_path.parent / 'game'
    
    # 決定模板目錄
    template_dir = None
    if not args.no_engine:
        if args.template:
            template_dir = args.template
        else:
            # 嘗試找 Monogatari 模板
            possible_paths = [
                Path(__file__).parent.parent / 'templates' / 'monogatari',
                Path.home() / 'Projects' / 'novel-to-visual-novel' / 'templates' / 'monogatari',
            ]
            for p in possible_paths:
                if p.exists():
                    template_dir = str(p)
                    break
    
    if template_dir:
        print(f"\n🎮 使用模板: {template_dir}")
    else:
        print("\n⚠️ 未找到 Monogatari 模板，將不包含引擎檔案")
    
    # 輸出遊戲
    print(f"\n🔨 組裝遊戲...")
    exporter = MonogatariExporter(config)
    
    output_path = exporter.export(
        processed_data=processed_data,
        assets_dir=str(assets_dir),
        output_dir=str(output_dir),
        template_dir=template_dir
    )
    
    print(f"\n✅ 遊戲組裝完成！")
    print(f"   輸出目錄: {output_path}")
    
    # 列出生成的檔案
    output_dir = Path(output_path)
    print(f"\n📂 生成的檔案:")
    print(f"   ✓ index.html")
    print(f"   ✓ js/script.js")
    print(f"   ✓ js/characters.js")
    print(f"   ✓ js/scenes.js")
    print(f"   ✓ js/options.js")
    print(f"   ✓ style/main.css")
    if template_dir:
        print(f"   ✓ dist/ (Monogatari 引擎)")
    print(f"   ✓ assets/ (素材)")
    
    print(f"\n🎮 遊玩方式:")
    print(f"   cd {output_path}")
    print(f"   python -m http.server 8080")
    print(f"   然後開啟 http://localhost:8080")


if __name__ == '__main__':
    main()
