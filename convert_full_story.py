#!/usr/bin/env python3
"""
將完整 Twee 故事轉換為 Monogatari script.js
"""

import re
import json
from pathlib import Path

# 角色對應
CHAR_MAPPING = {
    '和也': 'kazuya',
    '相葉': 'aiba',
}

# 讀取場景對應表
with open('C:/Users/lommi/Projects/visual-novel-toolkit/output/1140119_Temp/game/scene-mapping.json', 'r', encoding='utf-8') as f:
    SCENE_MAPPING = json.load(f)

# 預設場景（如果找不到對應）
DEFAULT_SCENE = 'secluded_alleyway'

def detect_characters(text):
    """偵測文字中的角色"""
    chars = set()
    for name, char_id in CHAR_MAPPING.items():
        if name in text:
            chars.add(char_id)
    return chars

def parse_twee(twee_path):
    """解析 Twee 檔案"""
    content = Path(twee_path).read_text(encoding='utf-8')
    
    passages = {}
    
    # 分割段落
    parts = re.split(r'\n:: ', content)
    
    for part in parts[1:]:  # 跳過第一個空白部分
        lines = part.strip().split('\n')
        if not lines:
            continue
        
        # 第一行是段落名稱
        passage_name = lines[0].strip()
        
        # 跳過 metadata
        if passage_name in ['StoryTitle', 'StoryData']:
            continue
        
        # 剩餘是內容
        body = '\n'.join(lines[1:])
        passages[passage_name] = body
    
    return passages

def convert_passage(name, body):
    """轉換單個段落為 Monogatari 格式"""
    result = []
    shown_chars = {}
    
    lines = body.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 場景標記 {/* scene:xxx */}
        scene_match = re.search(r'\{\s*/\*\s*scene:\s*(\w+)\s*\*/\s*\}', line)
        if scene_match:
            scene_code = scene_match.group(1)
            scene_id = SCENE_MAPPING.get(scene_code, DEFAULT_SCENE)
            result.append(f"show scene {scene_id} with fadeIn")
            shown_chars = {}  # 新場景重設角色
            continue
        
        # 選項 [[text->target]]
        choice_match = re.match(r'\[\[(.+?)->(\w+)\]\]', line)
        if choice_match:
            continue  # 選項稍後處理
        
        # 角色對話（中文角色名：對話）
        dialogue_match = re.match(r'^(和也|相葉)[：:]\s*(.+)$', line)
        if dialogue_match:
            char_name = dialogue_match.group(1)
            dialogue = dialogue_match.group(2)
            char_id = CHAR_MAPPING[char_name]
            
            # 確保角色顯示
            if char_id not in shown_chars:
                pos = 'left' if len(shown_chars) == 0 else 'right' if len(shown_chars) == 1 else 'center'
                result.append(f"show character {char_id} normal at {pos} with fadeIn")
                shown_chars[char_id] = pos
            
            result.append(f"{char_id} {dialogue}")
            continue
        
        # 一般旁白 - 分句
        # 檢查是否提到角色
        mentioned = detect_characters(line)
        for char_id in mentioned:
            if char_id not in shown_chars:
                pos = 'left' if len(shown_chars) == 0 else 'right' if len(shown_chars) == 1 else 'center'
                result.append(f"show character {char_id} normal at {pos} with fadeIn")
                shown_chars[char_id] = pos
        
        # 清理特殊標記
        clean_line = re.sub(r'\{\s*/\*.*?\*/\s*\}', '', line).strip()
        clean_line = re.sub(r'\[\[.+?\]\]', '', clean_line).strip()
        
        if clean_line:
            # 分句（用句號、問號、驚嘆號分割）
            sentences = re.split(r'([。！？])', clean_line)
            combined = []
            for i in range(0, len(sentences)-1, 2):
                s = sentences[i] + (sentences[i+1] if i+1 < len(sentences) else '')
                if s.strip():
                    combined.append(s.strip())
            if len(sentences) % 2 == 1 and sentences[-1].strip():
                combined.append(sentences[-1].strip())
            
            # 如果分句後太多，合併成幾段
            if len(combined) > 0:
                # 每 3-4 句合併
                chunks = []
                chunk = []
                for s in combined:
                    chunk.append(s)
                    if len(chunk) >= 3:
                        chunks.append(''.join(chunk))
                        chunk = []
                if chunk:
                    chunks.append(''.join(chunk))
                
                result.extend(chunks)
    
    # 提取選項
    choices = re.findall(r'\[\[(.+?)->(\w+)\]\]', body)
    
    return result, choices

def generate_script_js(passages):
    """生成完整 script.js"""
    
    # Header
    output = '''/* global monogatari */

// Define the backgrounds for each scene.
monogatari.assets('scenes', {
	'secluded_alleyway': 'secluded_alleyway/background.png',
	'aiba_apartment_interior': 'aiba_apartment_interior/background.png',
	'organization_interrogation_room': 'organization_interrogation_room/background.png',
	'cold_prison_cell': 'cold_prison_cell/background.png',
	'busy_commercial_district': 'busy_commercial_district/background.png',
	'secret_medical_lab': 'secret_medical_lab/background.png',
	'private_hospital_ward': 'private_hospital_ward/background.png',
	'rainy_street_lamp': 'rainy_street_lamp/background.png',
	'final_dark_alley': 'final_dark_alley/background.png'
});

// Define the Characters
monogatari.characters({
	'kazuya': {
		name: '和也',
		color: '#8b5cf6',
		directory: 'kazuya',
		sprites: {
			normal: 'normal.png',
			happy: 'happy.png',
			sad: 'sad.png',
			angry: 'angry.png',
			surprised: 'surprised.png'
		}
	},
	'aiba': {
		name: '相葉',
		color: '#22c55e',
		directory: 'aiba',
		sprites: {
			normal: 'normal.png',
			happy: 'happy.png',
			sad: 'sad.png',
			angry: 'angry.png',
			surprised: 'surprised.png'
		}
	}
});

monogatari.script({
'''
    
    passage_strs = []
    
    for name, body in passages.items():
        lines, choices = convert_passage(name, body)
        
        # 格式化
        formatted_lines = []
        for line in lines:
            # 跳脫單引號
            escaped = line.replace("'", "\\'")
            formatted_lines.append(f"\t\t'{escaped}'")
        
        # 加入選項
        if choices:
            choice_obj = "\t\t{\n\t\t\t'Choice': {\n"
            for text, target in choices:
                escaped_text = text.replace("'", "\\'")
                choice_obj += f"\t\t\t\t'{escaped_text}': {{\n"
                choice_obj += f"\t\t\t\t\t'Text': '{escaped_text}',\n"
                choice_obj += f"\t\t\t\t\t'Do': 'jump {target}'\n"
                choice_obj += "\t\t\t\t},\n"
            choice_obj += "\t\t\t}\n\t\t}"
            formatted_lines.append(choice_obj)
        elif name.startswith('Ending'):
            formatted_lines.append("\t\t'end'")
        
        passage_str = f"\t'{name}': [\n"
        passage_str += ',\n'.join(formatted_lines)
        passage_str += "\n\t]"
        passage_strs.append(passage_str)
    
    output += ',\n\n'.join(passage_strs)
    output += '\n});\n'
    
    return output

# 主程式
twee_path = 'C:/Users/lommi/Projects/visual-novel-toolkit/output/1140119_Temp/story.twee'
output_path = 'C:/Users/lommi/Projects/visual-novel-toolkit/output/1140119_Temp/monogatari-game/js/script.js'

print("Parsing Twee file...")
passages = parse_twee(twee_path)
print(f"Found {len(passages)} passages")

print("Generating script.js...")
script_content = generate_script_js(passages)

print(f"Writing to {output_path}...")
Path(output_path).write_text(script_content, encoding='utf-8')

print("Done!")
