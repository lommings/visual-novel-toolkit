#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Twee 格式輸出器"""

import uuid
from pathlib import Path
from typing import List


class TweeExporter:
    """Twee 格式輸出器"""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
    
    def export(self, title: str, passages: list, output_path: str,
               story_format: str = "Harlowe", format_version: str = "3.3.7") -> str:
        """
        輸出 Twee 格式檔案
        
        Args:
            title: 故事標題
            passages: 段落列表
            output_path: 輸出路徑
            story_format: 故事格式（Harlowe, SugarCube, etc.）
            format_version: 格式版本
        
        Returns:
            輸出的檔案路徑
        """
        twee_content = self._generate_header(title, story_format, format_version)
        twee_content += self._generate_passages(passages)
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(twee_content)
        
        return str(output_path)
    
    def _generate_header(self, title: str, story_format: str, 
                         format_version: str) -> str:
        """生成 Twee 檔頭"""
        ifid = str(uuid.uuid4()).upper()
        
        header = f""":: StoryTitle
{title}

:: StoryData
{{
  "ifid": "{ifid}",
  "format": "{story_format}",
  "format-version": "{format_version}",
  "start": "Start",
  "zoom": 1
}}

"""
        return header
    
    def _generate_passages(self, passages: list) -> str:
        """生成所有段落"""
        output = ""
        
        for passage in passages:
            output += self._generate_single_passage(passage)
            output += "\n"
        
        return output
    
    def _generate_single_passage(self, passage: dict) -> str:
        """生成單一段落"""
        name = passage.get('name', 'Unnamed')
        content = passage.get('content', '')
        scene_id = passage.get('scene_id', '')
        choices = passage.get('choices', [])
        next_passage = passage.get('next', '')
        
        # 段落標題
        output = f":: {name}"
        
        # 可選：加入位置標籤
        # output += f" [{position}]"
        
        output += "\n"
        
        # 場景標記（作為註解保留給後續處理）
        if scene_id:
            output += f"{{/* scene: {scene_id} */}}\n"
        
        # 內容
        output += content.strip()
        output += "\n"
        
        # 選項或下一段落
        if choices:
            output += "\n"
            for choice in choices:
                text = choice.get('text', '繼續')
                target = choice.get('target', 'End')
                condition = choice.get('condition', '')
                
                if condition:
                    # 條件選項
                    output += f"[[{text} |? {condition} ->{target}]]\n"
                else:
                    output += f"[[{text}->{target}]]\n"
        elif next_passage:
            output += f"\n[[繼續->{next_passage}]]\n"
        
        return output
    
    def export_with_metadata(self, analysis: dict, passages: list, 
                             output_dir: str) -> dict:
        """
        輸出 Twee 檔案和分析結果
        
        Args:
            analysis: 分析結果
            passages: 段落列表
            output_dir: 輸出目錄
        
        Returns:
            輸出檔案路徑字典
        """
        import json
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        title = analysis.get('title', '未命名故事')
        
        # 輸出 Twee 檔
        twee_path = output_dir / 'story.twee'
        self.export(title, passages, twee_path)
        
        # 輸出分析結果
        analysis_path = output_dir / 'analysis.json'
        with open(analysis_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        
        return {
            'twee': str(twee_path),
            'analysis': str(analysis_path)
        }


def passages_to_twee(passages: list, title: str = "Story") -> str:
    """
    便捷函式：將段落轉換為 Twee 字串
    
    Args:
        passages: 段落列表
        title: 故事標題
    
    Returns:
        Twee 格式字串
    """
    exporter = TweeExporter()
    
    # 生成內容
    header = exporter._generate_header(title, "Harlowe", "3.3.7")
    body = exporter._generate_passages(passages)
    
    return header + body
