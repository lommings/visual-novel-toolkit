#!/usr/bin/env python3
"""
智慧角色顯示處理：
1. 偵測文字中提到的角色
2. 自動在適當位置顯示角色
3. 兩人同時出現時一左一右
"""

import re
import json

# 角色對應表
CHAR_MAPPING = {
    '和也': 'kazuya',
    '相葉': 'aiba',
}

# 讀取檔案
with open('C:/Users/lommi/Projects/visual-novel-toolkit/output/1140119_Temp/monogatari-game/js/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取 script 部分
script_match = re.search(r'monogatari\.script\((\{[\s\S]+)\);?\s*$', content)
if not script_match:
    print("Error: Cannot find monogatari.script")
    exit(1)

# 保留 script 之前的部分
header = content[:script_match.start()]

# 解析 script（用 eval 是不安全的，但這是本地腳本）
script_str = script_match.group(1)

# 處理每個 passage
def detect_characters(text):
    """偵測文字中提到的角色"""
    chars = set()
    for name, char_id in CHAR_MAPPING.items():
        if name in text:
            chars.add(char_id)
    return chars

def process_script():
    """處理整個腳本"""
    lines = content.split('\n')
    new_lines = []
    
    current_shown = {}  # char_id -> position
    in_passage = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # 跳過 header 部分
        if 'monogatari.script' not in ''.join(new_lines) and 'monogatari.script' not in stripped:
            new_lines.append(line)
            continue
        
        # 場景切換時重設角色
        if "'show scene" in stripped:
            current_shown = {}
            new_lines.append(line)
            continue
        
        # 跳過現有的 show character 指令（我們會重新生成）
        if "'show character" in stripped:
            continue
        
        # 跳過 hide character
        if "'hide character" in stripped:
            current_shown = {}
            new_lines.append(line)
            continue
        
        # 檢查是否是文字行
        text_match = re.match(r"^\s*'([^']+)',?\s*$", line)
        if text_match:
            text = text_match.group(1)
            indent = len(line) - len(line.lstrip())
            
            # 偵測文字中的角色
            mentioned = detect_characters(text)
            
            # 檢查是否是角色對話（'charId 對話'）
            dialogue_match = re.match(r'^(aiba|kazuya)\s+', text)
            if dialogue_match:
                mentioned.add(dialogue_match.group(1))
            
            # 需要顯示的新角色
            to_show = mentioned - set(current_shown.keys())
            
            if to_show:
                # 決定位置
                all_chars = set(current_shown.keys()) | mentioned
                
                if len(all_chars) == 1:
                    # 只有一個角色，放中間
                    for char in to_show:
                        show_cmd = ' ' * indent + f"'show character {char} normal at center with fadeIn',"
                        new_lines.append(show_cmd)
                        current_shown[char] = 'center'
                elif len(all_chars) >= 2:
                    # 兩個角色，一左一右
                    positions = ['left', 'right']
                    pos_idx = 0
                    
                    # 先安排已顯示的角色位置
                    for char in current_shown:
                        if pos_idx < len(positions):
                            current_shown[char] = positions[pos_idx]
                            pos_idx += 1
                    
                    # 新角色
                    for char in to_show:
                        if pos_idx < len(positions):
                            pos = positions[pos_idx]
                            pos_idx += 1
                        else:
                            pos = 'center'
                        
                        show_cmd = ' ' * indent + f"'show character {char} normal at {pos} with fadeIn',"
                        new_lines.append(show_cmd)
                        current_shown[char] = pos
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

result = process_script()

# 寫回檔案
with open('C:/Users/lommi/Projects/visual-novel-toolkit/output/1140119_Temp/monogatari-game/js/script.js', 'w', encoding='utf-8') as f:
    f.write(result)

print('Done! Added smart character display commands.')
