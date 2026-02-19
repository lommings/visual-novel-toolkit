#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Twee Processor - Twee 檔案處理工具

分析 Twee 檔案中的角色、場景，並拆分段落為適合視覺小說的格式。
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.config_manager import ConfigManager
from shared.file_utils import load_json, save_json, ensure_dir, get_timestamp

from twee_parser import TweeParser, parse_twee_file
from content_analyzer import ContentAnalyzer
from text_splitter import TextSplitter


def main():
    """主程式"""
    parser = argparse.ArgumentParser(
        description='處理 Twee 檔案，分析角色場景並拆分段落'
    )
    parser.add_argument('input', help='輸入 Twee 檔案路徑')
    parser.add_argument('-o', '--output', help='輸出目錄', default=None)
    parser.add_argument('-a', '--analysis', help='已有的 analysis.json 路徑', default=None)
    parser.add_argument('-c', '--config', help='設定檔路徑', default=None)
    parser.add_argument('--max-length', type=int, help='每行最大長度', default=50)
    parser.add_argument('--no-split', action='store_true', help='不拆分段落')
    
    args = parser.parse_args()
    
    # 載入設定
    config = ConfigManager.load(args.config)
    
    # 設定最大行長度
    if args.max_length:
        config['twee_processor'] = config.get('twee_processor', {})
        config['twee_processor']['max_line_length'] = args.max_length
    
    # 讀取 Twee 檔案
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ 檔案不存在: {input_path}")
        sys.exit(1)
    
    print(f"📖 讀取 Twee: {input_path.name}")
    
    # 解析 Twee
    twee_parser = TweeParser()
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    story = twee_parser.parse(content)
    print(f"   標題: {story.title or '(無標題)'}")
    print(f"   段落: {len(story.passages)} 個")
    
    # 轉換為字典格式
    passages_raw = []
    for p in story.passages:
        choices = twee_parser.extract_links(p.content)
        passages_raw.append({
            'name': p.name,
            'content': twee_parser.remove_links(p.content),
            'choices': choices
        })
    
    # 載入或進行分析
    existing_analysis = None
    if args.analysis:
        analysis_path = Path(args.analysis)
        if analysis_path.exists():
            print(f"\n📂 載入分析結果: {analysis_path.name}")
            existing_analysis = load_json(analysis_path)
    
    # 分析內容
    print("\n🔍 分析內容...")
    analyzer = ContentAnalyzer(config)
    analysis_result = analyzer.analyze_passages(passages_raw, existing_analysis)
    
    characters = analysis_result.get('characters', [])
    scenes = analysis_result.get('scenes', [])
    analyzed_passages = analysis_result.get('passages', [])
    
    print(f"   角色: {len(characters)} 人")
    for char in characters:
        print(f"      - {char.get('name', '?')}")
    
    print(f"   場景: {len(scenes)} 個")
    for scene in scenes:
        print(f"      - {scene.get('name', '?')}")
    
    # 拆分段落
    if not args.no_split:
        print("\n✂️ 拆分段落...")
        splitter = TextSplitter(config.get('twee_processor', {}))
        processed_passages = splitter.process_all_passages(analyzed_passages)
        
        total_lines = sum(len(p.get('lines', [])) for p in processed_passages)
        print(f"   總行數: {total_lines}")
    else:
        processed_passages = analyzed_passages
    
    # 決定輸出目錄
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = input_path.parent / input_path.stem
    
    ensure_dir(output_dir)
    print(f"\n💾 輸出到: {output_dir}")
    
    # 輸出 processed.json
    processed_data = {
        'version': '1.0',
        'generated_at': get_timestamp(),
        'source_file': str(input_path),
        'title': story.title or input_path.stem,
        'characters': characters,
        'scenes': scenes,
        'passages': processed_passages
    }
    
    processed_path = output_dir / 'processed.json'
    save_json(processed_data, processed_path)
    print(f"   ✓ {processed_path.name}")
    
    # 輸出 assets-needed.json
    assets_needed = {
        'version': '1.0',
        'generated_at': get_timestamp(),
        'characters': [
            {
                'id': c.get('id', ''),
                'name': c.get('name', ''),
                'description': c.get('description', ''),
                'expressions_needed': c.get('expressions', ['normal'])
            }
            for c in characters
        ],
        'scenes': [
            {
                'id': s.get('id', ''),
                'name': s.get('name', ''),
                'description': s.get('description', ''),
                'time_of_day': s.get('time_of_day', '日間'),
                'mood': s.get('mood', '')
            }
            for s in scenes
        ]
    }
    
    assets_path = output_dir / 'assets-needed.json'
    save_json(assets_needed, assets_path)
    print(f"   ✓ {assets_path.name}")
    
    print("\n✅ 完成！")
    print(f"\n下一步:")
    print(f"   使用 asset-previewer 預覽和生成圖片:")
    print(f"   python asset-previewer/main.py {assets_path}")


if __name__ == '__main__':
    main()
