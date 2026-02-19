#!/usr/bin/env python3
"""修正 script.js，在角色對話前加入 show character 指令"""

import re

# 讀取檔案
with open('C:/Users/lommi/Projects/visual-novel-toolkit/output/1140119_Temp/monogatari-game/js/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 追蹤當前顯示的角色
shown_chars = set()

lines = content.split('\n')
new_lines = []

for line in lines:
    stripped = line.strip()
    
    # 檢查是否是場景切換
    if "'show scene" in stripped:
        shown_chars = set()  # 新場景，重設角色
    
    # 檢查是否是角色對話（'charId 對話'）
    match = re.match(r"^'(aiba|kazuya)\s+(.+)',?\s*$", stripped)
    
    if match:
        char_id = match.group(1)
        
        # 如果這個角色還沒顯示，先加入 show character
        if char_id not in shown_chars:
            indent = len(line) - len(line.lstrip())
            show_cmd = ' ' * indent + f"'show character {char_id} normal at center with fadeIn',"
            new_lines.append(show_cmd)
            shown_chars.add(char_id)
    
    # 移除已存在的重複 show character 指令（避免重複）
    if "'show character" in stripped and stripped in [l.strip() for l in new_lines[-3:] if "'show character" in l]:
        continue
    
    new_lines.append(line)

# 寫回檔案
with open('C:/Users/lommi/Projects/visual-novel-toolkit/output/1140119_Temp/monogatari-game/js/script.js', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print('Done! Added show character commands.')
