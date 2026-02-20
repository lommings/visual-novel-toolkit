#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧轉換 Twee 到 Monogatari
- 角色在文字提到後才出現
- 根據情緒關鍵字選擇表情
"""

import re
import json
from pathlib import Path

CHAR_MAPPING = {'和也': 'kazuya', '相葉': 'aiba'}

EMOTION_KEYWORDS = {
    'happy': ['笑', '開心', '高興', '喜', '微笑', '溫暖', '感激', '欣慰'],
    'sad': ['難過', '悲傷', '哭', '淚', '痛苦', '絕望', '憂', '沮喪', '低落'],
    'angry': ['怒', '氣', '憤', '惱', '不滿', '冷'],
    'surprised': ['驚', '震', '嚇', '意外', '沒想到', '愕'],
}

SPEAKING_VERBS = ['說', '道', '問', '答', '喊', '叫', '回答', '詢問', '提醒', '告訴', '低聲', '輕聲', '大聲', '回', '應']

with open('C:/Users/lommi/Projects/visual-novel-toolkit/output/1140119_Temp/game/scene-mapping.json', 'r', encoding='utf-8') as f:
    SCENE_MAPPING = json.load(f)

def detect_chars(text):
    """偵測文字中的角色"""
    chars = []
    for name, cid in CHAR_MAPPING.items():
        pos = text.find(name)
        if pos >= 0:
            chars.append((cid, pos))
    chars.sort(key=lambda x: x[1])
    return [c[0] for c in chars]

def detect_emotion(text):
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return emotion
    return 'normal'

def is_dialogue(before):
    for v in SPEAKING_VERBS:
        if v in before[-8:]:
            return True
    return before.rstrip().endswith('：') or before.rstrip().endswith(':')

def split_text(text, max_len=50):
    """分割文字，每段約兩行，不以逗號結尾"""
    if not text.strip():
        return []
    
    text = text.strip()
    if len(text) <= max_len:
        return [text]
    
    # 用句號分割
    parts = re.split(r'([。！？])', text)
    sentences = []
    
    i = 0
    while i < len(parts):
        s = parts[i]
        if i + 1 < len(parts) and parts[i+1] in '。！？':
            s += parts[i+1]
            i += 2
        else:
            i += 1
        if s.strip():
            sentences.append(s.strip())
    
    result = []
    current = ''
    
    for s in sentences:
        if len(current) + len(s) <= max_len:
            current += s
        else:
            if current:
                if current.endswith('，'):
                    current = current[:-1]
                result.append(current)
            current = s
    
    if current:
        if current.endswith('，'):
            current = current[:-1]
        result.append(current)
    
    return result if result else [text]

def parse_twee(path):
    content = Path(path).read_text(encoding='utf-8')
    passages = {}
    for part in re.split(r'\n:: ', content)[1:]:
        lines = part.strip().split('\n')
        if not lines:
            continue
        name = lines[0].strip()
        if name not in ['StoryTitle', 'StoryData']:
            passages[name] = '\n'.join(lines[1:])
    return passages

def convert_passage(name, body):
    result = []
    shown = {}
    
    def show_char(cid, emotion='normal'):
        """顯示角色（在文字後）"""
        if cid in shown and shown[cid] == emotion:
            return
        
        # 計算位置
        if cid not in shown:
            if len(shown) == 0:
                pos = 'center'
            elif len(shown) == 1:
                # 移動第一個角色到左邊
                other = list(shown.keys())[0]
                other_emotion = shown[other]
                result.append(f"show character {other} {other_emotion} at left")
                pos = 'right'
            else:
                pos = 'right'
            result.append(f"show character {cid} {emotion} at {pos} with fadeIn")
        else:
            # 只更新表情
            keys = list(shown.keys())
            idx = keys.index(cid)
            pos = 'center' if len(keys) == 1 else ('left' if idx == 0 else 'right')
            result.append(f"show character {cid} {emotion} at {pos}")
        
        shown[cid] = emotion
    
    # 清理
    clean = re.sub(r'\{\s*/\*.*?\*/\s*\}', '', body).strip()
    clean = re.sub(r'\[\[.+?\]\]', '', clean).strip()
    
    # 場景
    m = re.search(r'\{\s*/\*\s*scene:\s*(\w+)\s*\*/\s*\}', body)
    if m:
        sid = SCENE_MAPPING.get(m.group(1), 'secluded_alleyway')
        result.append(f"show scene {sid} with fadeIn")
    
    last_speaker = None
    
    for para in clean.split('\n'):
        para = para.strip()
        if not para:
            continue
        
        # 處理引號對話
        last_end = 0
        
        for m in re.finditer(r'([^「」]*?)[「『]([^」』]+)[」』]', para):
            before = m.group(1)
            quote = m.group(2)
            
            # 引號前的旁白
            narration = para[last_end:m.start()] + before
            if narration.strip():
                # 先輸出文字
                for s in split_text(narration.strip()):
                    result.append(s)
                
                # 再顯示角色
                chars = detect_chars(narration)
                emotion = detect_emotion(narration)
                for cid in chars:
                    show_char(cid, emotion)
            
            # 判斷是否是對話
            full_before = para[:m.start()] + before
            if is_dialogue(full_before):
                chars = detect_chars(before)
                speaker = chars[-1] if chars else last_speaker
                
                if speaker:
                    last_speaker = speaker
                    emotion = detect_emotion(quote)
                    show_char(speaker, emotion)
                    result.append(f"{speaker} {quote}")
                else:
                    result.append(f"「{quote}」")
            else:
                result.append(f"「{quote}」")
            
            last_end = m.end()
        
        # 剩餘文字
        if last_end < len(para):
            remaining = para[last_end:].strip()
            if remaining:
                for s in split_text(remaining):
                    result.append(s)
                chars = detect_chars(remaining)
                emotion = detect_emotion(remaining)
                for cid in chars:
                    show_char(cid, emotion)
        
        # 沒有引號的段落
        if last_end == 0:
            for s in split_text(para):
                result.append(s)
            chars = detect_chars(para)
            emotion = detect_emotion(para)
            for cid in chars:
                show_char(cid, emotion)
    
    choices = re.findall(r'\[\[(.+?)->(\w+)\]\]', body)
    return result, choices

def generate_js(passages):
    scenes = list(set(SCENE_MAPPING.values()))
    
    out = '''/* global monogatari */

monogatari.assets('scenes', ''' + json.dumps({s: f"{s}/background.png" for s in scenes}, ensure_ascii=False, indent=2) + ''');

monogatari.characters({
    'kazuya': {
        name: '和也',
        color: '#8b5cf6',
        directory: 'kazuya',
        sprites: { normal: 'normal.png', happy: 'happy.png', sad: 'sad.png', angry: 'angry.png', surprised: 'surprised.png' }
    },
    'aiba': {
        name: '相葉',
        color: '#22c55e',
        directory: 'aiba',
        sprites: { normal: 'normal.png', happy: 'happy.png', sad: 'sad.png', angry: 'angry.png', surprised: 'surprised.png' }
    }
});

monogatari.script({
'''
    
    pstrs = []
    for pname, body in passages.items():
        lines, choices = convert_passage(pname, body)
        
        flines = []
        for ln in lines:
            esc = ln.replace("\\", "\\\\").replace("'", "\\'")
            flines.append(f"\t\t'{esc}'")
        
        if choices:
            cobj = "\t\t{\n\t\t\t'Choice': {\n"
            for txt, tgt in choices:
                etxt = txt.replace("'", "\\'")
                cobj += f"\t\t\t\t'{etxt}': {{ 'Text': '{etxt}', 'Do': 'jump {tgt}' }},\n"
            cobj += "\t\t\t}\n\t\t}"
            flines.append(cobj)
        elif pname.startswith('Ending'):
            flines.append("\t\t'end'")
        
        pstrs.append(f"\t'{pname}': [\n" + ',\n'.join(flines) + "\n\t]")
    
    out += ',\n\n'.join(pstrs) + '\n});\n'
    return out

# Main
print("Converting story...")
passages = parse_twee('C:/Users/lommi/Projects/visual-novel-toolkit/output/1140119_Temp/story.twee')
print(f"Found {len(passages)} passages")

js = generate_js(passages)
output_path = Path('C:/Users/lommi/Projects/visual-novel-toolkit/output/1140119_Temp/monogatari-game/js/script.js')
output_path.write_text(js, encoding='utf-8')
print(f"Written to {output_path}")
print("Done!")
