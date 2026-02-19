#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Twee 格式解析器"""

import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class TweePassage:
    """Twee 段落"""
    name: str
    content: str
    tags: List[str] = field(default_factory=list)
    position: Optional[Tuple[int, int]] = None  # x, y 位置
    metadata: Dict = field(default_factory=dict)


@dataclass
class TweeStory:
    """Twee 故事"""
    title: str = ""
    ifid: str = ""
    format: str = "Harlowe"
    format_version: str = "3.3.7"
    start: str = "Start"
    passages: List[TweePassage] = field(default_factory=list)
    
    def get_passage(self, name: str) -> Optional[TweePassage]:
        """取得段落"""
        for p in self.passages:
            if p.name == name:
                return p
        return None


class TweeParser:
    """Twee 格式解析器"""
    
    # 段落標題模式：:: 名稱 [標籤] {位置}
    PASSAGE_PATTERN = re.compile(
        r'^::\s*([^\[\{]+?)\s*'  # 名稱
        r'(?:\[([^\]]*)\])?\s*'  # 標籤（可選）
        r'(?:\{([^\}]*)\})?\s*$'  # 位置（可選）
    )
    
    # 連結模式
    LINK_PATTERN = re.compile(
        r'\[\[([^\]|]+?)(?:\|([^\]]+?))?\s*(?:->\s*([^\]]+?))?\]\]'
    )
    
    def parse(self, content: str) -> TweeStory:
        """
        解析 Twee 內容
        
        Args:
            content: Twee 檔案內容
        
        Returns:
            TweeStory 物件
        """
        story = TweeStory()
        
        # 分割段落
        lines = content.split('\n')
        current_passage = None
        current_content = []
        
        for line in lines:
            # 檢查是否是段落標題
            match = self.PASSAGE_PATTERN.match(line)
            
            if match:
                # 儲存前一個段落
                if current_passage:
                    current_passage.content = '\n'.join(current_content).strip()
                    story.passages.append(current_passage)
                
                # 解析新段落
                name = match.group(1).strip()
                tags = match.group(2).split() if match.group(2) else []
                position = self._parse_position(match.group(3))
                
                # 處理特殊段落
                if name == 'StoryTitle':
                    current_passage = TweePassage(name=name, content='', tags=tags)
                    current_content = []
                elif name == 'StoryData':
                    current_passage = TweePassage(name=name, content='', tags=tags)
                    current_content = []
                else:
                    current_passage = TweePassage(
                        name=name, 
                        content='',
                        tags=tags,
                        position=position
                    )
                    current_content = []
            else:
                # 累積內容
                current_content.append(line)
        
        # 儲存最後一個段落
        if current_passage:
            current_passage.content = '\n'.join(current_content).strip()
            story.passages.append(current_passage)
        
        # 處理特殊段落
        self._process_special_passages(story)
        
        return story
    
    def _parse_position(self, pos_str: str) -> Optional[Tuple[int, int]]:
        """解析位置字串"""
        if not pos_str:
            return None
        
        # 格式: "100,200" 或 "100, 200"
        match = re.match(r'(\d+)\s*,\s*(\d+)', pos_str)
        if match:
            return (int(match.group(1)), int(match.group(2)))
        return None
    
    def _process_special_passages(self, story: TweeStory):
        """處理特殊段落（StoryTitle, StoryData）"""
        passages_to_remove = []
        
        for passage in story.passages:
            if passage.name == 'StoryTitle':
                story.title = passage.content.strip()
                passages_to_remove.append(passage)
            
            elif passage.name == 'StoryData':
                import json
                try:
                    data = json.loads(passage.content)
                    story.ifid = data.get('ifid', '')
                    story.format = data.get('format', 'Harlowe')
                    story.format_version = data.get('format-version', '')
                    story.start = data.get('start', 'Start')
                except json.JSONDecodeError:
                    pass
                passages_to_remove.append(passage)
        
        # 移除特殊段落
        for p in passages_to_remove:
            story.passages.remove(p)
    
    def extract_links(self, content: str) -> List[Dict]:
        """
        從內容中提取連結
        
        Args:
            content: 段落內容
        
        Returns:
            連結列表，每個包含 text, target
        """
        links = []
        
        for match in self.LINK_PATTERN.finditer(content):
            text = match.group(1).strip()
            # 處理各種連結格式
            # [[文字->目標]]
            # [[文字|顯示文字->目標]]
            # [[文字]]
            
            if match.group(3):
                # 有 -> 的情況
                target = match.group(3).strip()
                display = match.group(2).strip() if match.group(2) else text
            elif match.group(2):
                # 有 | 的情況
                target = match.group(2).strip()
                display = text
            else:
                # 只有文字
                target = text
                display = text
            
            # 檢查條件
            condition = None
            if '|?' in display:
                parts = display.split('|?')
                display = parts[0].strip()
                condition = parts[1].strip() if len(parts) > 1 else None
            
            links.append({
                'text': display,
                'target': target,
                'condition': condition
            })
        
        return links
    
    def remove_links(self, content: str) -> str:
        """移除內容中的連結標記，保留文字"""
        def replace_link(match):
            text = match.group(1).strip()
            if '|' in text:
                text = text.split('|')[0].strip()
            return ''
        
        return self.LINK_PATTERN.sub(replace_link, content).strip()
    
    def extract_scene_markers(self, content: str) -> List[str]:
        """
        提取場景標記
        
        支援格式：
        - {/* scene: scene_id */}
        - <!-- scene: scene_id -->
        - [scene: scene_id]
        """
        patterns = [
            r'\{/\*\s*scene:\s*([^\*]+)\s*\*/\}',
            r'<!--\s*scene:\s*([^>]+)\s*-->',
            r'\[scene:\s*([^\]]+)\]'
        ]
        
        scenes = []
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            scenes.extend([m.strip() for m in matches])
        
        return scenes


def parse_twee_file(file_path: str) -> TweeStory:
    """
    便捷函式：解析 Twee 檔案
    
    Args:
        file_path: 檔案路徑
    
    Returns:
        TweeStory 物件
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parser = TweeParser()
    return parser.parse(content)
