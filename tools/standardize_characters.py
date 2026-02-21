#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
角色立繪標準化工具

在手動剪裁後，統一調整到相同高度
使用方式：
    # 預覽效果
    python tools/standardize_characters.py story/assets/characters --preview --height 1200
    
    # 執行標準化
    python tools/standardize_characters.py story/assets/characters --height 1200
"""

from PIL import Image
from pathlib import Path
import argparse
import sys


def standardize_character(image_path: Path, target_height: int = 1200, dry_run: bool = False) -> tuple:
    """
    標準化單個角色圖片
    
    Args:
        image_path: 圖片路徑
        target_height: 目標高度
        dry_run: 是否只預覽不實際修改
    
    Returns:
        (原始尺寸, 新尺寸) 元組
    """
    img = Image.open(image_path)
    original_size = img.size
    
    # 計算新尺寸（保持比例）
    ratio = img.size[0] / img.size[1]
    target_width = int(target_height * ratio)
    new_size = (target_width, target_height)
    
    if not dry_run:
        # 縮放
        img_resized = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # 覆蓋原檔案
        img_resized.save(image_path)
    
    return original_size, new_size


def main():
    parser = argparse.ArgumentParser(
        description='標準化角色立繪大小（在手動剪裁後使用）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  # 預覽效果
  python tools/standardize_characters.py story/assets/characters --preview
  
  # 執行標準化（高度 1200px）
  python tools/standardize_characters.py story/assets/characters --height 1200
  
  # 執行標準化（高度 1500px）
  python tools/standardize_characters.py story/assets/characters --height 1500
"""
    )
    
    parser.add_argument('assets_dir', help='角色素材目錄 (例如: story/assets/characters)')
    parser.add_argument('--height', type=int, default=1200, help='目標高度（像素，預設 1200）')
    parser.add_argument('--preview', action='store_true', help='只顯示預覽，不實際修改檔案')
    parser.add_argument('--file', help='只處理特定檔名（預設: normal.png）', default='normal.png')
    
    args = parser.parse_args()
    
    assets_dir = Path(args.assets_dir)
    
    if not assets_dir.exists():
        print(f"❌ 目錄不存在: {assets_dir}")
        sys.exit(1)
    
    # 找出所有角色資料夾
    char_dirs = sorted([d for d in assets_dir.iterdir() if d.is_dir()])
    
    if not char_dirs:
        print(f"❌ 找不到任何角色資料夾")
        sys.exit(1)
    
    print(f"[*] 找到 {len(char_dirs)} 個角色資料夾")
    print(f"[*] 目標高度: {args.height}px")
    print(f"[*] 檔案名稱: {args.file}")
    
    if args.preview:
        print(f"[*] 預覽模式（不會修改檔案）")
    
    print()
    
    processed = 0
    skipped = 0
    
    for char_dir in char_dirs:
        image_file = char_dir / args.file
        
        if not image_file.exists():
            print(f"[!] {char_dir.name}: 找不到 {args.file}")
            skipped += 1
            continue
        
        try:
            original_size, new_size = standardize_character(
                image_file, 
                args.height, 
                dry_run=args.preview
            )
            
            if args.preview:
                print(f"[o] {char_dir.name}: {original_size[0]}x{original_size[1]} -> {new_size[0]}x{new_size[1]}")
            else:
                print(f"[+] {char_dir.name}: {original_size[0]}x{original_size[1]} -> {new_size[0]}x{new_size[1]}")
            
            processed += 1
            
        except Exception as e:
            print(f"[-] {char_dir.name}: 處理失敗 - {e}")
            skipped += 1
    
    print()
    print(f"{'-' * 50}")
    print(f"[*] 處理完成: {processed} 個成功, {skipped} 個跳過")
    
    if args.preview:
        print()
        print(f"[!] 這是預覽模式，沒有實際修改檔案")
        print(f"   移除 --preview 參數來執行標準化：")
        print(f"   python tools/standardize_characters.py {args.assets_dir} --height {args.height}")
    else:
        print()
        print(f"[+] 標準化完成！")
        print(f"    所有角色立繪已統一調整為高度 {args.height}px")


if __name__ == '__main__':
    main()
