#!/usr/bin/env python3
"""
腳本處理器
自動處理角色顯示、位置、對話等
"""

import re
from typing import Dict, List, Set, Tuple, Optional


class ScriptProcessor:
    """處理視覺小說腳本，自動加入角色顯示指令"""
    
    def __init__(self, char_name_mapping: Dict[str, str]):
        """
        Args:
            char_name_mapping: 角色名稱對應表 {'中文名': 'char_id'}
                               例如: {'和也': 'kazuya', '相葉': 'aiba'}
        """
        self.char_name_mapping = char_name_mapping
    
    def detect_characters(self, text: str) -> Set[str]:
        """偵測文字中提到的角色
        
        Args:
            text: 要分析的文字
            
        Returns:
            角色 ID 集合
        """
        chars = set()
        for name, char_id in self.char_name_mapping.items():
            if name in text:
                chars.add(char_id)
        return chars
    
    def parse_dialogue(self, text: str) -> Optional[Tuple[str, str]]:
        """解析對話行，提取角色和對話內容
        
        支援格式:
        - "角色名：對話內容"
        - "角色名: 對話內容"
        
        Args:
            text: 文字行
            
        Returns:
            (char_id, dialogue) 或 None
        """
        # 建立角色名稱的正則
        names = '|'.join(re.escape(name) for name in self.char_name_mapping.keys())
        match = re.match(rf'^({names})[：:]\s*(.+)$', text)
        
        if match:
            char_name = match.group(1)
            dialogue = match.group(2)
            char_id = self.char_name_mapping[char_name]
            return (char_id, dialogue)
        
        return None
    
    def get_position(self, shown_chars: Dict[str, str], new_char: str) -> str:
        """決定角色的顯示位置
        
        規則:
        - 第一個角色: center
        - 第二個角色: 第一個在 left，第二個在 right
        - 更多角色: 輪替 left/right/center
        
        Args:
            shown_chars: 已顯示的角色 {char_id: position}
            new_char: 新角色 ID
            
        Returns:
            位置字串 ('left', 'right', 'center')
        """
        if len(shown_chars) == 0:
            return 'center'
        elif len(shown_chars) == 1:
            # 把第一個角色移到 left，新角色放 right
            return 'right'
        else:
            # 已經有兩個以上，放 center
            return 'center'
    
    def reposition_for_two(self, shown_chars: Dict[str, str]) -> List[str]:
        """當有兩個角色時，重新定位為一左一右
        
        Returns:
            需要執行的 show character 指令列表
        """
        commands = []
        chars = list(shown_chars.keys())
        
        if len(chars) >= 2:
            # 隱藏後重新顯示
            commands.append(f"show character {chars[0]} normal at left")
            commands.append(f"show character {chars[1]} normal at right")
            shown_chars[chars[0]] = 'left'
            shown_chars[chars[1]] = 'right'
        
        return commands
    
    def process_passage(
        self, 
        lines: List[str],
        scene_id: Optional[str] = None
    ) -> List[str]:
        """處理單個段落，加入角色顯示指令
        
        Args:
            lines: 段落的文字行列表
            scene_id: 場景 ID（如果有的話）
            
        Returns:
            處理後的指令列表
        """
        result = []
        shown_chars: Dict[str, str] = {}  # char_id -> position
        
        # 如果有場景，先加入場景指令
        if scene_id:
            result.append(f"show scene {scene_id} with fadeIn")
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 跳過已經是 show 指令的行
            if line.startswith('show ') or line.startswith('hide '):
                if 'show scene' in line:
                    shown_chars = {}  # 新場景重設角色
                result.append(line)
                continue
            
            # 解析對話
            dialogue = self.parse_dialogue(line)
            if dialogue:
                char_id, text = dialogue
                
                # 確保角色顯示
                if char_id not in shown_chars:
                    # 檢查是否需要重新定位
                    if len(shown_chars) == 1:
                        # 變成兩個角色，重新定位
                        other_char = list(shown_chars.keys())[0]
                        result.append(f"show character {other_char} normal at left")
                        shown_chars[other_char] = 'left'
                        result.append(f"show character {char_id} normal at right with fadeIn")
                        shown_chars[char_id] = 'right'
                    else:
                        pos = self.get_position(shown_chars, char_id)
                        result.append(f"show character {char_id} normal at {pos} with fadeIn")
                        shown_chars[char_id] = pos
                
                # 加入對話（使用 Monogatari 格式）
                result.append(f"{char_id} {text}")
                continue
            
            # 一般文字，檢查是否提到角色
            mentioned = self.detect_characters(line)
            new_chars = mentioned - set(shown_chars.keys())
            
            if new_chars:
                # 計算所有角色
                all_chars = set(shown_chars.keys()) | mentioned
                
                if len(all_chars) >= 2 and len(shown_chars) <= 1:
                    # 需要重新定位
                    existing = list(shown_chars.keys())
                    new_list = list(new_chars)
                    
                    if existing:
                        result.append(f"show character {existing[0]} normal at left")
                        shown_chars[existing[0]] = 'left'
                    
                    for i, char_id in enumerate(new_list):
                        if len(shown_chars) == 0:
                            pos = 'left'
                        elif len(shown_chars) == 1:
                            pos = 'right'
                        else:
                            pos = 'center'
                        result.append(f"show character {char_id} normal at {pos} with fadeIn")
                        shown_chars[char_id] = pos
                else:
                    # 單獨顯示新角色
                    for char_id in new_chars:
                        pos = self.get_position(shown_chars, char_id)
                        result.append(f"show character {char_id} normal at {pos} with fadeIn")
                        shown_chars[char_id] = pos
            
            result.append(line)
        
        return result
    
    def process_script(
        self,
        passages: Dict[str, Dict],
        scene_mapping: Optional[Dict[str, str]] = None
    ) -> Dict[str, List]:
        """處理整個腳本
        
        Args:
            passages: 段落資料 {passage_name: {scene, text, choices}}
            scene_mapping: 場景代碼對應表 {scene_code: scene_id}
            
        Returns:
            處理後的腳本 {passage_name: [指令列表]}
        """
        scene_mapping = scene_mapping or {}
        result = {}
        
        for name, data in passages.items():
            # 取得場景
            scene_code = data.get('scene_code') or data.get('scene')
            scene_id = scene_mapping.get(scene_code, scene_code)
            print(f"    Passage '{name}': scene_code={scene_code} -> scene_id={scene_id}")
            
            # 分割文字為行
            text = data.get('text', '')
            lines = self._split_text(text)
            
            # 處理段落
            processed = self.process_passage(lines, scene_id)
            
            # 加入選項
            choices = data.get('choices', [])
            if choices:
                choice_obj = {'Choice': {}}
                for choice in choices:
                    text = choice.get('text', '')
                    target = choice.get('target', '')
                    choice_obj['Choice'][text] = {
                        'Text': text,
                        'Do': f'jump {target}'
                    }
                processed.append(choice_obj)
            elif name.startswith('Ending'):
                # 加入結局標題通知
                ending_title = self._get_ending_title(name)
                processed.append(f'centered ── 結局：{ending_title} ──')
                processed.append('end')
            
            result[name] = processed
        
        return result
    
    def _split_text(self, text: str) -> List[str]:
        """將文字分割成適合顯示的段落
        
        Args:
            text: 原始文字
            
        Returns:
            分割後的文字列表
        """
        if not text:
            return []
        
        # 先用換行分割
        paragraphs = text.split('\n')
        result = []
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # 用句號分割，但保留標點
            sentences = re.split(r'([。！？])', para)
            combined = []
            
            for i in range(0, len(sentences)-1, 2):
                s = sentences[i] + (sentences[i+1] if i+1 < len(sentences) else '')
                if s.strip():
                    combined.append(s.strip())
            
            if len(sentences) % 2 == 1 and sentences[-1].strip():
                combined.append(sentences[-1].strip())
            
            # 每 2-3 句合併成一段
            chunk = []
            for s in combined:
                chunk.append(s)
                if len(chunk) >= 2:
                    result.append(''.join(chunk))
                    chunk = []
            
            if chunk:
                result.append(''.join(chunk))
        
        return result
    
    def _get_ending_title(self, passage_name: str) -> str:
        """將結局段落名稱轉換為可讀標題
        
        Args:
            passage_name: 段落名稱 (例如 "Ending_BreakChains")
            
        Returns:
            可讀的結局標題
        """
        # 結局名稱對應表
        ending_titles = {
            'Ending_BreakChains': '破鏈重生',
            'Ending_LostShadow': '消失的幽影',
            'Ending_SilentEnd': '無聲的終結',
            'Ending_Together': '相守一生',
            'Ending_Sacrifice': '犧牲',
            'Ending_Freedom': '自由',
            'Ending_Hope': '希望',
            'Ending_Farewell': '告別',
        }
        
        if passage_name in ending_titles:
            return ending_titles[passage_name]
        
        # 嘗試從段落名稱生成標題
        # "Ending_BreakChains" -> "Break Chains" -> 直接使用英文
        if passage_name.startswith('Ending_'):
            name_part = passage_name[7:]  # 移除 "Ending_"
            # 將 CamelCase 轉換為空格分隔
            readable = re.sub(r'([a-z])([A-Z])', r'\1 \2', name_part)
            return readable
        
        return passage_name


# 預設角色對應表
DEFAULT_CHAR_MAPPING = {
    '和也': 'kazuya',
    '相葉': 'aiba',
}


def create_processor(char_mapping: Optional[Dict[str, str]] = None) -> ScriptProcessor:
    """建立腳本處理器
    
    Args:
        char_mapping: 角色名稱對應表，None 使用預設
        
    Returns:
        ScriptProcessor 實例
    """
    return ScriptProcessor(char_mapping or DEFAULT_CHAR_MAPPING)
