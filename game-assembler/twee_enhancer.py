#!/usr/bin/env python3
"""
Twee 增強器
根據分析結果，為 Twee 檔案加入場景和角色標記
"""

import re
import json
from pathlib import Path
from typing import Dict, List


class TweeEnhancer:
    """增強 Twee 檔案，加入視覺標記"""
    
    def __init__(self, scene_mapping: Dict[str, str], dialogue_markers: Dict[str, List[Dict]]):
        self.scene_mapping = scene_mapping
        self.dialogue_markers = dialogue_markers
    
    def enhance_twee(self, twee_path: Path, output_path: Path):
        """增強 Twee 檔案"""
        content = twee_path.read_text(encoding='utf-8')
        
        # 分割成段落
        parts = re.split(r'(:: \w+)', content)
        
        enhanced_parts = []
        current_passage = None
        
        for i, part in enumerate(parts):
            if part.startswith(':: '):
                current_passage = part[3:].strip()
                enhanced_parts.append(part)
            elif current_passage and current_passage not in ['StoryTitle', 'StoryData']:
                # 增強段落內容
                enhanced = self._enhance_passage(current_passage, part)
                enhanced_parts.append(enhanced)
            else:
                enhanced_parts.append(part)
        
        # 寫入增強後的檔案
        output_path.write_text(''.join(enhanced_parts), encoding='utf-8')
    
    def _enhance_passage(self, passage_name: str, content: str) -> str:
        """增強單個段落"""
        lines = content.split('\n')
        enhanced_lines = []
        
        for line in lines:
            # 檢查場景標記
            scene_match = re.search(r'\{\s*/\*\s*scene:\s*(\w+)\s*\*/\s*\}', line)
            if scene_match:
                scene_code = scene_match.group(1)
                scene_id = self.scene_mapping.get(scene_code, scene_code)
                # 替換為實際場景 ID
                enhanced_line = re.sub(
                    r'\{\s*/\*\s*scene:\s*\w+\s*\*/\s*\}',
                    f'[scene:{scene_id}]',
                    line
                )
                enhanced_lines.append(enhanced_line)
            else:
                enhanced_lines.append(line)
        
        # 如果有對話標記，插入角色和表情
        if passage_name in self.dialogue_markers:
            return self._insert_dialogue_markers(
                '\n'.join(enhanced_lines),
                self.dialogue_markers[passage_name]
            )
        
        return '\n'.join(enhanced_lines)
    
    def _insert_dialogue_markers(self, content: str, markers: List[Dict]) -> str:
        """插入對話標記"""
        # 簡化版：在段落開頭加入角色標記
        # 完整版應該逐句匹配
        
        result_lines = []
        content_lines = content.split('\n')
        
        # 找到場景標記後的位置
        insert_pos = 0
        for i, line in enumerate(content_lines):
            if '[scene:' in line:
                insert_pos = i + 1
                break
        
        # 收集出現的角色
        speakers = set()
        for marker in markers:
            if marker['speaker'] != 'narrator':
                speakers.add(marker['speaker'])
        
        # 插入角色出場標記
        for i, line in enumerate(content_lines):
            result_lines.append(line)
            if i == insert_pos and speakers:
                for speaker in speakers:
                    # 找到這個角色的第一個表情
                    expr = 'normal'
                    for m in markers:
                        if m['speaker'] == speaker and m.get('expression'):
                            expr = m['expression']
                            break
                    result_lines.append(f'[char:{speaker}:{expr}]')
        
        return '\n'.join(result_lines)


def generate_enhanced_twee(
    twee_path: Path,
    scene_mapping_path: Path,
    dialogue_markers_path: Path,
    output_path: Path
):
    """生成增強版 Twee 檔案"""
    
    # 載入場景對應
    with open(scene_mapping_path, 'r', encoding='utf-8') as f:
        scene_mapping = json.load(f)
    
    # 載入對話標記（可選）
    dialogue_markers = {}
    if dialogue_markers_path.exists():
        with open(dialogue_markers_path, 'r', encoding='utf-8') as f:
            dialogue_markers = json.load(f)
    
    # 增強 Twee
    enhancer = TweeEnhancer(scene_mapping, dialogue_markers)
    enhancer.enhance_twee(twee_path, output_path)
    
    print(f"[Done] Enhanced Twee saved: {output_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='增強 Twee 檔案')
    parser.add_argument('twee_path', help='原始 Twee 檔案')
    parser.add_argument('scene_mapping', help='場景對應 JSON')
    parser.add_argument('-d', '--dialogues', help='對話標記 JSON（可選）')
    parser.add_argument('-o', '--output', help='輸出檔案', required=True)
    
    args = parser.parse_args()
    
    generate_enhanced_twee(
        Path(args.twee_path),
        Path(args.scene_mapping),
        Path(args.dialogues) if args.dialogues else Path('nonexistent'),
        Path(args.output)
    )


if __name__ == '__main__':
    main()
