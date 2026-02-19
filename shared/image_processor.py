#!/usr/bin/env python3
"""
圖片處理工具
提供去背、縮放等功能
"""

from pathlib import Path
from typing import Optional, Tuple
from PIL import Image

try:
    from rembg import remove
    HAS_REMBG = True
except ImportError:
    HAS_REMBG = False
    print("[Warning] rembg not installed. Background removal will be skipped.")


def remove_background(
    input_path: Path,
    output_path: Optional[Path] = None,
    resize: Optional[Tuple[int, int]] = None
) -> Path:
    """
    移除圖片背景
    
    Args:
        input_path: 輸入圖片路徑
        output_path: 輸出路徑（預設覆蓋原檔）
        resize: 縮放尺寸 (width, height)，None 不縮放
    
    Returns:
        輸出檔案路徑
    """
    if output_path is None:
        output_path = input_path
    
    img = Image.open(input_path)
    
    # 去背
    if HAS_REMBG:
        img = remove(img)
    
    # 縮放
    if resize:
        img = img.resize(resize, Image.Resampling.LANCZOS)
    
    # 確保是 RGBA
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # 儲存
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, 'PNG')
    
    return output_path


def process_character_sprites(
    chars_dir: Path,
    output_dir: Optional[Path] = None,
    remove_bg: bool = True,
    resize: Optional[Tuple[int, int]] = None
) -> int:
    """
    批次處理角色立繪
    
    Args:
        chars_dir: 角色素材目錄（包含各角色子資料夾）
        output_dir: 輸出目錄（預設覆蓋原檔）
        remove_bg: 是否去背
        resize: 縮放尺寸
    
    Returns:
        處理的檔案數量
    """
    if not HAS_REMBG and remove_bg:
        print("[Warning] rembg not available, skipping background removal")
        remove_bg = False
    
    count = 0
    
    for char_dir in chars_dir.iterdir():
        if not char_dir.is_dir():
            continue
        
        char_id = char_dir.name
        print(f"  Processing character: {char_id}")
        
        for img_path in char_dir.glob('*.png'):
            if output_dir:
                out_path = output_dir / char_id / img_path.name
            else:
                out_path = img_path
            
            if remove_bg:
                print(f"    {img_path.name} -> removing background...")
                remove_background(img_path, out_path, resize)
            elif resize:
                print(f"    {img_path.name} -> resizing...")
                img = Image.open(img_path)
                img = img.resize(resize, Image.Resampling.LANCZOS)
                out_path.parent.mkdir(parents=True, exist_ok=True)
                img.save(out_path, 'PNG')
            
            count += 1
    
    return count


def main():
    """命令列介面"""
    import argparse
    
    parser = argparse.ArgumentParser(description='處理角色立繪圖片')
    parser.add_argument('input_dir', help='輸入目錄（角色素材）')
    parser.add_argument('-o', '--output', help='輸出目錄（預設覆蓋原檔）')
    parser.add_argument('--no-rembg', action='store_true', help='不去背')
    parser.add_argument('--resize', help='縮放尺寸，格式: WxH (如 512x1024)')
    
    args = parser.parse_args()
    
    resize = None
    if args.resize:
        w, h = args.resize.lower().split('x')
        resize = (int(w), int(h))
    
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output) if args.output else None
    
    print(f"Processing characters in: {input_dir}")
    count = process_character_sprites(
        input_dir,
        output_dir,
        remove_bg=not args.no_rembg,
        resize=resize
    )
    print(f"Done! Processed {count} images.")


if __name__ == '__main__':
    main()
