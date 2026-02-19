#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Asset Previewer - 素材預覽工具

生成預覽圖，提供網頁介面選擇，然後生成正式素材。
"""

import sys
import json
import argparse
import webbrowser
import http.server
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.config_manager import ConfigManager
from shared.file_utils import load_json, save_json, ensure_dir, get_timestamp, read_text

from preview_generator import PreviewGenerator


def progress_callback(current, total, message):
    """進度顯示"""
    percent = (current / total) * 100
    bar_len = 30
    filled = int(bar_len * current / total)
    bar = '█' * filled + '░' * (bar_len - filled)
    print(f"\r   [{bar}] {percent:.0f}% {message[:40]:<40}", end='', flush=True)
    if current == total:
        print()


def generate_preview_html(preview_dir: Path, assets_data: dict, 
                          char_results: dict, scene_results: dict) -> str:
    """生成預覽 HTML"""
    # 準備資料
    preview_data = {
        'characters': [],
        'scenes': []
    }
    
    for char in assets_data.get('characters', []):
        char_id = char.get('id', '')
        paths = char_results.get(char_id, [])
        # 轉換為相對路徑
        rel_paths = [str(Path(p).relative_to(preview_dir)).replace('\\', '/') for p in paths]
        preview_data['characters'].append({
            'id': char_id,
            'name': char.get('name', char_id),
            'description': char.get('description', ''),
            'concepts': rel_paths
        })
    
    for scene in assets_data.get('scenes', []):
        scene_id = scene.get('id', '')
        paths = scene_results.get(scene_id, [])
        rel_paths = [str(Path(p).relative_to(preview_dir)).replace('\\', '/') for p in paths]
        preview_data['scenes'].append({
            'id': scene_id,
            'name': scene.get('name', scene_id),
            'description': scene.get('description', ''),
            'time_of_day': scene.get('time_of_day', ''),
            'concepts': rel_paths
        })
    
    # 讀取模板
    template_path = Path(__file__).parent / 'templates' / 'preview.html'
    template = read_text(template_path)
    
    # 替換資料
    html = template.replace('{{PREVIEW_DATA}}', json.dumps(preview_data, ensure_ascii=False))
    
    # 寫入
    output_path = preview_dir / 'preview.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return str(output_path)


def start_preview_server(preview_dir: str, port: int = 8080):
    """啟動預覽伺服器"""
    import os
    os.chdir(preview_dir)
    
    handler = http.server.SimpleHTTPRequestHandler
    server = http.server.HTTPServer(('localhost', port), handler)
    
    print(f"\n🌐 預覽伺服器已啟動: http://localhost:{port}/preview.html")
    print("   按 Ctrl+C 停止伺服器")
    
    # 自動開啟瀏覽器
    webbrowser.open(f"http://localhost:{port}/preview.html")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n伺服器已停止")


def apply_selections(selections_path: str, assets_data: dict, 
                    preview_dir: str, output_dir: str, config: dict):
    """根據選擇生成正式素材"""
    selections = load_json(selections_path)
    generator = PreviewGenerator(config)
    
    output_dir = Path(output_dir)
    preview_dir = Path(preview_dir)
    
    # 生成角色
    print("\n👤 生成角色立繪...")
    char_selections = selections.get('characters', {})
    
    for char in assets_data.get('characters', []):
        char_id = char.get('id', '')
        if char_id not in char_selections:
            print(f"   ⚠️ 未選擇: {char.get('name', char_id)}")
            continue
        
        selection = char_selections[char_id]
        reference_path = selection.get('concept_file', '')
        
        # 如果是相對路徑，轉為絕對路徑
        if not Path(reference_path).is_absolute():
            reference_path = str(preview_dir / reference_path)
        
        print(f"   生成 {char.get('name', char_id)}...")
        generator.generate_final_character(
            character=char,
            reference_path=reference_path,
            output_dir=str(output_dir),
            callback=lambda c, t, m: print(f"      {m}")
        )
    
    # 生成場景
    print("\n🖼️ 生成場景...")
    scene_selections = selections.get('scenes', {})
    
    for scene in assets_data.get('scenes', []):
        scene_id = scene.get('id', '')
        if scene_id not in scene_selections:
            print(f"   ⚠️ 未選擇: {scene.get('name', scene_id)}")
            continue
        
        selection = scene_selections[scene_id]
        reference_path = selection.get('concept_file', '')
        
        if not Path(reference_path).is_absolute():
            reference_path = str(preview_dir / reference_path)
        
        print(f"   複製 {scene.get('name', scene_id)}...")
        generator.generate_final_scene(
            scene=scene,
            reference_path=reference_path,
            output_dir=str(output_dir)
        )
    
    print("\n✅ 素材生成完成！")


def main():
    """主程式"""
    parser = argparse.ArgumentParser(
        description='生成素材預覽，選擇後生成正式素材'
    )
    parser.add_argument('input', help='assets-needed.json 路徑')
    parser.add_argument('-o', '--output', help='輸出目錄', default=None)
    parser.add_argument('-c', '--config', help='設定檔路徑', default=None)
    parser.add_argument('--generate-only', action='store_true', 
                       help='只生成預覽，不啟動伺服器')
    parser.add_argument('--preview', action='store_true',
                       help='生成預覽並開啟網頁')
    parser.add_argument('--apply', help='套用選擇結果（selections.json 路徑）')
    parser.add_argument('--concepts', type=int, help='每項生成幾張概念圖')
    parser.add_argument('--port', type=int, default=8080, help='預覽伺服器端口')
    
    args = parser.parse_args()
    
    # 載入設定
    config = ConfigManager.load(args.config)
    
    # 更新概念圖數量
    if args.concepts:
        config['asset_previewer'] = config.get('asset_previewer', {})
        config['asset_previewer']['character_concepts_count'] = args.concepts
        config['asset_previewer']['scene_concepts_count'] = args.concepts
    
    # 讀取素材需求
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ 檔案不存在: {input_path}")
        sys.exit(1)
    
    assets_data = load_json(input_path)
    
    # 決定輸出目錄
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = input_path.parent
    
    preview_dir = output_dir / 'preview'
    assets_dir = output_dir / 'assets'
    
    # 如果是套用選擇
    if args.apply:
        print(f"📂 套用選擇: {args.apply}")
        apply_selections(args.apply, assets_data, str(preview_dir), 
                        str(assets_dir), config)
        return
    
    # 生成預覽
    print(f"📖 讀取素材需求: {input_path.name}")
    print(f"   角色: {len(assets_data.get('characters', []))} 人")
    print(f"   場景: {len(assets_data.get('scenes', []))} 個")
    
    ensure_dir(preview_dir)
    generator = PreviewGenerator(config)
    
    # 生成角色預覽
    print("\n👤 生成角色概念圖...")
    char_results = generator.generate_character_previews(
        assets_data.get('characters', []),
        str(preview_dir),
        callback=progress_callback
    )
    
    # 生成場景預覽  
    print("\n🖼️ 生成場景概念圖...")
    scene_results = generator.generate_scene_previews(
        assets_data.get('scenes', []),
        str(preview_dir),
        callback=progress_callback
    )
    
    # 生成預覽 HTML
    print("\n📄 生成預覽頁面...")
    html_path = generate_preview_html(preview_dir, assets_data, 
                                      char_results, scene_results)
    print(f"   ✓ {html_path}")
    
    if args.generate_only:
        print("\n✅ 預覽生成完成！")
        print(f"   開啟 {html_path} 查看並選擇")
        return
    
    if args.preview:
        # 啟動預覽伺服器
        start_preview_server(str(preview_dir), args.port)
    else:
        print("\n✅ 預覽生成完成！")
        print(f"\n下一步:")
        print(f"   1. 開啟預覽: python asset-previewer/main.py {input_path} --preview")
        print(f"   2. 或直接開啟: {html_path}")
        print(f"   3. 選擇後下載 selections.json")
        print(f"   4. 生成素材: python asset-previewer/main.py {input_path} --apply selections.json")


if __name__ == '__main__':
    main()
