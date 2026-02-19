#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""檔案操作工具模組"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Union


def ensure_dir(path: Union[str, Path]) -> Path:
    """
    確保目錄存在，不存在則建立
    
    Args:
        path: 目錄路徑
    
    Returns:
        Path 物件
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_json(path: Union[str, Path]) -> dict:
    """
    載入 JSON 檔案
    
    Args:
        path: JSON 檔案路徑
    
    Returns:
        解析後的字典
    
    Raises:
        FileNotFoundError: 檔案不存在
        json.JSONDecodeError: JSON 格式錯誤
    """
    path = Path(path)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: dict, path: Union[str, Path], indent: int = 2) -> None:
    """
    儲存 JSON 檔案
    
    Args:
        data: 要儲存的資料
        path: 輸出路徑
        indent: 縮排空格數
    """
    path = Path(path)
    ensure_dir(path.parent)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)


def copy_file(src: Union[str, Path], dst: Union[str, Path]) -> None:
    """
    複製檔案
    
    Args:
        src: 來源路徑
        dst: 目標路徑
    """
    src, dst = Path(src), Path(dst)
    ensure_dir(dst.parent)
    shutil.copy2(src, dst)


def copy_directory(src: Union[str, Path], dst: Union[str, Path], 
                   overwrite: bool = True) -> None:
    """
    複製整個目錄
    
    Args:
        src: 來源目錄
        dst: 目標目錄
        overwrite: 是否覆蓋現有目錄
    """
    src, dst = Path(src), Path(dst)
    
    if dst.exists() and overwrite:
        shutil.rmtree(dst)
    
    shutil.copytree(src, dst)


def get_timestamp() -> str:
    """
    取得 ISO 格式時間戳
    
    Returns:
        ISO 格式時間字串
    """
    return datetime.now().isoformat()


def read_text(path: Union[str, Path]) -> str:
    """
    讀取文字檔
    
    Args:
        path: 檔案路徑
    
    Returns:
        檔案內容
    """
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write_text(content: str, path: Union[str, Path]) -> None:
    """
    寫入文字檔
    
    Args:
        content: 檔案內容
        path: 輸出路徑
    """
    path = Path(path)
    ensure_dir(path.parent)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def list_files(directory: Union[str, Path], pattern: str = "*") -> list:
    """
    列出目錄中的檔案
    
    Args:
        directory: 目錄路徑
        pattern: 過濾模式，如 "*.json"
    
    Returns:
        檔案路徑列表
    """
    directory = Path(directory)
    return list(directory.glob(pattern))


def get_relative_path(path: Union[str, Path], base: Union[str, Path]) -> str:
    """
    取得相對路徑
    
    Args:
        path: 完整路徑
        base: 基礎路徑
    
    Returns:
        相對路徑字串（使用正斜線）
    """
    path, base = Path(path), Path(base)
    try:
        rel = path.relative_to(base)
        return str(rel).replace('\\', '/')
    except ValueError:
        return str(path).replace('\\', '/')
