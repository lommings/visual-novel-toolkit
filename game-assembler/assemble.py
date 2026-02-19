#!/usr/bin/env python3
"""
遊戲組裝主程式
整合 Twee 分析、增強和遊戲組裝的完整流程
"""

import argparse
import json
from pathlib import Path
import sys

# 確保可以 import 相關模組
sys.path.insert(0, str(Path(__file__).parent.parent))

from game_assembler.twee_analyzer import TweeAnalyzer
from game_assembler.twee_enhancer import TweeEnhancer
from game_assembler.game_builder import GameBuilder
from shared.config_manager import ConfigManager


def main():
    parser = argparse.ArgumentParser(
        description='組裝視覺小說遊戲',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  # 完整流程（分析 + 增強 + 組裝）
  python assemble.py story.twee assets-needed.json assets/ -o output/game/
  
  # 只做場景對應（不分析對話）
  python assemble.py story.twee assets-needed.json assets/ -o output/game/ --scene-only
  
  # 使用已有的分析結果
  python assemble.py story.twee assets-needed.json assets/ -o output/game/ \\
      --scene-mapping scene-mapping.json --dialogue-markers dialogue-markers.json
'''
    )
    
    parser.add_argument('twee_path', help='Twee 故事檔案')
    parser.add_argument('assets_json', help='assets-needed.json 素材需求檔')
    parser.add_argument('assets_dir', help='素材目錄（含 characters/ 和 scenes/）')
    parser.add_argument('-o', '--output', required=True, help='輸出目錄')
    
    parser.add_argument('--scene-only', action='store_true', 
                       help='只生成場景對應，不分析對話')
    parser.add_argument('--scene-mapping', help='使用已有的場景對應 JSON')
    parser.add_argument('--dialogue-markers', help='使用已有的對話標記 JSON')
    parser.add_argument('--skip-analysis', action='store_true',
                       help='跳過 AI 分析，使用預設對應')
    parser.add_argument('--dialogue-limit', type=int,
                       help='限制分析的段落數量（用於測試）')
    
    args = parser.parse_args()
    
    twee_path = Path(args.twee_path)
    assets_json = Path(args.assets_json)
    assets_dir = Path(args.assets_dir)
    output_dir = Path(args.output)
    
    # 驗證輸入
    if not twee_path.exists():
        print(f"❌ Twee 檔案不存在: {twee_path}")
        return 1
    if not assets_json.exists():
        print(f"❌ 素材需求檔不存在: {assets_json}")
        return 1
    if not assets_dir.exists():
        print(f"❌ 素材目錄不存在: {assets_dir}")
        return 1
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 載入素材資料
    with open(assets_json, 'r', encoding='utf-8') as f:
        assets_data = json.load(f)
    
    print("=" * 50)
    print("🎮 視覺小說遊戲組裝器")
    print("=" * 50)
    
    # ===== 步驟 1: 分析 Twee =====
    scene_mapping = {}
    dialogue_markers = {}
    
    if args.scene_mapping:
        # 使用已有的場景對應
        print(f"\n📂 載入場景對應: {args.scene_mapping}")
        with open(args.scene_mapping, 'r', encoding='utf-8') as f:
            scene_mapping = json.load(f)
    elif args.skip_analysis:
        # 使用預設對應（場景代碼直接當作場景 ID）
        print("\n⚡ 跳過分析，使用預設對應")
        config = ConfigManager.load()
        analyzer = TweeAnalyzer(config)
        twee_data = analyzer.parse_twee(twee_path)
        for passage in twee_data['passages'].values():
            if passage['scene_code']:
                scene_mapping[passage['scene_code']] = passage['scene_code']
    else:
        # 使用 AI 分析
        print("\n🔍 步驟 1/3: 分析 Twee 檔案...")
        config = ConfigManager.load()
        analyzer = TweeAnalyzer(config)
        
        twee_data = analyzer.parse_twee(twee_path)
        print(f"   段落數: {len(twee_data['passages'])}")
        
        print("   生成場景對應...")
        scene_mapping = analyzer.generate_scene_mapping(twee_data, assets_data)
        
        # 儲存場景對應
        mapping_path = output_dir / 'scene-mapping.json'
        with open(mapping_path, 'w', encoding='utf-8') as f:
            json.dump(scene_mapping, f, ensure_ascii=False, indent=2)
        print(f"   ✓ 儲存至: {mapping_path}")
        
        if not args.scene_only:
            print("   分析對話標記...")
            dialogue_markers = analyzer.analyze_dialogues(
                twee_data,
                assets_data.get('characters', []),
                limit=args.dialogue_limit
            )
            
            dialogue_path = output_dir / 'dialogue-markers.json'
            with open(dialogue_path, 'w', encoding='utf-8') as f:
                json.dump(dialogue_markers, f, ensure_ascii=False, indent=2)
            print(f"   ✓ 儲存至: {dialogue_path}")
    
    if args.dialogue_markers:
        print(f"\n📂 載入對話標記: {args.dialogue_markers}")
        with open(args.dialogue_markers, 'r', encoding='utf-8') as f:
            dialogue_markers = json.load(f)
    
    # ===== 步驟 2: 增強 Twee =====
    print("\n✨ 步驟 2/3: 增強 Twee 檔案...")
    enhanced_twee_path = output_dir / 'enhanced-story.twee'
    
    enhancer = TweeEnhancer(scene_mapping, dialogue_markers)
    enhancer.enhance_twee(twee_path, enhanced_twee_path)
    print(f"   ✓ 增強版 Twee: {enhanced_twee_path}")
    
    # ===== 步驟 3: 組裝遊戲 =====
    print("\n🎮 步驟 3/3: 組裝遊戲...")
    builder = GameBuilder(output_dir)
    game_path = builder.build_game(enhanced_twee_path, assets_dir)
    
    print("\n" + "=" * 50)
    print("✅ 組裝完成！")
    print(f"   遊戲檔案: {game_path}")
    print(f"   用瀏覽器開啟即可遊玩")
    print("=" * 50)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
