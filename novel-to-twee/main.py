#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Novel to Twee - 小說轉 Twee 格式工具

將純文字小說轉換為 Twee 格式，並由 AI 分析產生劇情分支。
"""

import sys
import argparse
from pathlib import Path

# 確保可以 import shared 模組
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.config_manager import ConfigManager
from shared.file_utils import read_text, save_json, ensure_dir, get_timestamp

from story_analyzer import StoryAnalyzer
from branch_generator import BranchGenerator
from twee_exporter import TweeExporter


def main():
    """主程式"""
    parser = argparse.ArgumentParser(
        description='將小說轉換為 Twee 格式（含 AI 分支）'
    )
    parser.add_argument('input', help='輸入小說檔案路徑')
    parser.add_argument('-o', '--output', help='輸出目錄', default='output')
    parser.add_argument('-c', '--config', help='設定檔路徑', default=None)
    parser.add_argument('--branches', type=int, help='分支數量', default=2)
    parser.add_argument('--interactive', action='store_true', help='互動模式')
    parser.add_argument('--no-branch', action='store_true', help='不生成分支')
    
    args = parser.parse_args()
    
    # 載入設定
    config = ConfigManager.load(args.config)
    
    # 讀取輸入檔案
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ 檔案不存在: {input_path}")
        sys.exit(1)
    
    print(f"📖 讀取小說: {input_path.name}")
    text = read_text(input_path)
    print(f"   共 {len(text)} 字")
    
    # 分析故事
    print("\n🔍 AI 分析故事...")
    analyzer = StoryAnalyzer(config)
    analysis = analyzer.analyze(text)
    
    print(f"   標題: {analysis.get('title', '未命名')}")
    print(f"   角色: {len(analysis.get('characters', []))} 人")
    print(f"   場景: {len(analysis.get('scenes', []))} 個")
    print(f"   分支點: {len(analysis.get('branch_points', []))} 個")
    
    # 顯示分析結果
    if args.interactive:
        print("\n📋 角色列表:")
        for char in analysis.get('characters', []):
            print(f"   - {char.get('name')}: {char.get('description', '')[:30]}...")
        
        print("\n🎬 場景列表:")
        for scene in analysis.get('scenes', []):
            print(f"   - {scene.get('name')}: {scene.get('description', '')[:30]}...")
        
        print("\n🔀 分支點:")
        for i, bp in enumerate(analysis.get('branch_points', [])):
            print(f"   {i+1}. {bp.get('description', '')[:50]}...")
            for choice in bp.get('choices', []):
                print(f"      → {choice.get('text')}")
        
        confirm = input("\n繼續生成？ [Y/n] ").strip().lower()
        if confirm == 'n':
            print("已取消")
            sys.exit(0)
    
    # 生成分支
    print("\n✍️ 生成分支劇情...")
    generator = BranchGenerator(config)
    
    if args.no_branch:
        passages = generator._generate_linear_story(
            text, 
            analysis.get('characters', []),
            analysis.get('scenes', [])
        )
    else:
        passages = generator.generate_branches(text, analysis)
    
    print(f"   生成 {len(passages)} 個段落")
    
    # 輸出
    output_dir = Path(args.output) / input_path.stem
    ensure_dir(output_dir)
    
    print(f"\n💾 輸出到: {output_dir}")
    
    # 輸出 Twee
    exporter = TweeExporter(config)
    twee_path = output_dir / 'story.twee'
    exporter.export(
        title=analysis.get('title', input_path.stem),
        passages=passages,
        output_path=twee_path
    )
    print(f"   ✓ {twee_path.name}")
    
    # 輸出分析結果
    analysis['generated_at'] = get_timestamp()
    analysis['source_file'] = str(input_path)
    analysis['passages_count'] = len(passages)
    
    analysis_path = output_dir / 'analysis.json'
    save_json(analysis, analysis_path)
    print(f"   ✓ {analysis_path.name}")
    
    # 輸出段落資料（供後續工具使用）
    passages_data = {
        'version': '1.0',
        'generated_at': get_timestamp(),
        'title': analysis.get('title', ''),
        'passages': passages
    }
    passages_path = output_dir / 'passages.json'
    save_json(passages_data, passages_path)
    print(f"   ✓ {passages_path.name}")
    
    print("\n✅ 完成！")
    print(f"\n下一步:")
    print(f"   1. 用 Twine 開啟 {twee_path.name} 編輯分支")
    print(f"   2. 編輯完成後，使用 twee-processor 處理")


if __name__ == '__main__':
    main()
