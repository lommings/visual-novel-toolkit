#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文字拆分器 - 將長段落拆分為適合視覺小說的短句"""

import re
from typing import List, Dict


class TextSplitter:
    """文字拆分器"""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.max_length = self.config.get('max_line_length', 50)
    
    def split_lines(self, lines: List[Dict]) -> List[Dict]:
        """
        拆分所有行
        
        Args:
            lines: 原始行列表
        
        Returns:
            拆分後的行列表
        """
        result = []
        
        for line in lines:
            if line.get('type') == 'narration':
                # 拆分旁白
                split_narrations = self.split_narration(line.get('text', ''))
                for text in split_narrations:
                    result.append({
                        'type': 'narration',
                        'text': text
                    })
            elif line.get('type') == 'dialogue':
                # 對話通常不需要拆分，但如果太長也要處理
                text = line.get('text', '')
                if len(text) > self.max_length * 2:
                    # 太長的對話拆分
                    split_texts = self.split_text(text)
                    for i, t in enumerate(split_texts):
                        result.append({
                            'type': 'dialogue',
                            'character': line.get('character', ''),
                            'text': t,
                            'expression': line.get('expression', 'normal')
                        })
                else:
                    result.append(line)
            else:
                result.append(line)
        
        return result
    
    def split_narration(self, text: str) -> List[str]:
        """
        拆分旁白文字
        
        Args:
            text: 原始文字
        
        Returns:
            拆分後的句子列表
        """
        if not text:
            return []
        
        # 先按明顯的句子結束符號分割
        sentences = self._split_by_punctuation(text)
        
        # 再檢查是否需要進一步拆分
        result = []
        for sentence in sentences:
            if len(sentence) > self.max_length:
                # 進一步拆分長句
                sub_sentences = self._split_long_sentence(sentence)
                result.extend(sub_sentences)
            else:
                result.append(sentence)
        
        return [s for s in result if s.strip()]
    
    def split_text(self, text: str) -> List[str]:
        """通用文字拆分"""
        return self.split_narration(text)
    
    def _split_by_punctuation(self, text: str) -> List[str]:
        """按標點符號拆分"""
        # 在句號、問號、驚嘆號後拆分
        # 但保留標點符號
        pattern = r'([。！？])'
        parts = re.split(pattern, text)
        
        sentences = []
        current = ''
        
        for part in parts:
            if part in '。！？':
                current += part
                if current.strip():
                    sentences.append(current.strip())
                current = ''
            else:
                current += part
        
        if current.strip():
            sentences.append(current.strip())
        
        return sentences
    
    def _split_long_sentence(self, text: str) -> List[str]:
        """拆分長句"""
        if len(text) <= self.max_length:
            return [text]
        
        # 嘗試在逗號處拆分
        parts = text.split('，')
        
        result = []
        current = ''
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            # 加上逗號（除了最後一部分）
            if current:
                test = current + '，' + part
            else:
                test = part
            
            if len(test) <= self.max_length:
                current = test
            else:
                if current:
                    result.append(current)
                current = part
        
        if current:
            result.append(current)
        
        # 如果還是太長，強制拆分
        final_result = []
        for s in result:
            if len(s) > self.max_length:
                # 強制按字數拆分
                final_result.extend(self._force_split(s))
            else:
                final_result.append(s)
        
        return final_result
    
    def _force_split(self, text: str) -> List[str]:
        """強制按字數拆分"""
        result = []
        
        while len(text) > self.max_length:
            # 找一個合適的拆分點
            split_point = self.max_length
            
            # 嘗試在標點符號處拆分
            for i in range(self.max_length - 1, max(0, self.max_length - 20), -1):
                if text[i] in '，、；：':
                    split_point = i + 1
                    break
            
            result.append(text[:split_point].strip())
            text = text[split_point:].strip()
        
        if text:
            result.append(text)
        
        return result
    
    def process_passage(self, passage: Dict) -> Dict:
        """
        處理單一段落
        
        Args:
            passage: 段落資料
        
        Returns:
            處理後的段落
        """
        lines = passage.get('lines', [])
        split_lines = self.split_lines(lines)
        
        return {
            'name': passage.get('name', ''),
            'scene_id': passage.get('scene_id'),
            'lines': split_lines,
            'choices': passage.get('choices', [])
        }
    
    def process_all_passages(self, passages: List[Dict]) -> List[Dict]:
        """處理所有段落"""
        return [self.process_passage(p) for p in passages]


def split_for_visual_novel(text: str, max_length: int = 50) -> List[str]:
    """
    便捷函式：拆分文字為視覺小說格式
    
    Args:
        text: 原始文字
        max_length: 每行最大長度
    
    Returns:
        拆分後的句子列表
    """
    splitter = TextSplitter({'max_line_length': max_length})
    return splitter.split_narration(text)
