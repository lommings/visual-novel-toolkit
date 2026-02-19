#!/usr/bin/env python3
"""清理重複的 show character 指令，重新生成正確的腳本"""

import re

# 讀取檔案
with open('C:/Users/lommi/Projects/visual-novel-toolkit/output/1140119_Temp/monogatari-game/js/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
new_lines = []
prev_was_show_char = False
shown_chars = set()

for i, line in enumerate(lines):
    stripped = line.strip()
    
    # 場景切換時重設
    if "'show scene" in stripped:
        shown_chars = set()
        prev_was_show_char = False
        new_lines.append(line)
        continue
    
    # 如果是 show character 指令
    if "'show character" in stripped:
        # 提取角色 ID
        match = re.search(r"show character (\w+)", stripped)
        if match:
            char_id = match.group(1)
            # 如果這個角色已經顯示過，跳過
            if char_id in shown_chars:
                continue
            shown_chars.add(char_id)
        prev_was_show_char = True
        new_lines.append(line)
        continue
    
    # 一般行
    prev_was_show_char = False
    new_lines.append(line)

# 寫回檔案
with open('C:/Users/lommi/Projects/visual-novel-toolkit/output/1140119_Temp/monogatari-game/js/script.js', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print('Done! Cleaned up duplicate show character commands.')
