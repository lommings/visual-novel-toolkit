#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧轉換 Twee 到 Monogatari
- 場景在文字提到地點時切換
- 角色在文字提到後才出現
- 根據情緒關鍵字選擇表情

用法:
    python convert_full_story.py --project output/專案名
    python convert_full_story.py --twee story.twee --scene-mapping scene-mapping.json --output js/script.js
"""

import re
import json
import argparse
from pathlib import Path

CHAR_MAPPING = {'和也': 'kazuya', '相葉': 'aiba'}

EMOTION_KEYWORDS = {
    'happy': ['笑', '開心', '高興', '喜', '微笑', '溫暖', '感激', '欣慰', '幸福'],
    'sad': ['難過', '悲傷', '哭', '淚', '痛苦', '絕望', '憂', '沮喪', '低落', '心酸', '無力'],
    'angry': ['怒', '氣', '憤', '惱', '不滿', '冷'],
    'surprised': ['驚', '震', '嚇', '意外', '沒想到', '愕'],
}

SPEAKING_VERBS = ['說', '道', '問', '答', '喊', '叫', '回答', '詢問', '提醒', '告訴', '低聲', '輕聲', '大聲', '回', '應']

# 場景關鍵字對應（更精準的匹配，避免誤判）
SCENE_KEYWORDS = {
    'aiba_apartment_interior': ['到家後', '躺到沙發上'],
    'secluded_alleyway': [],  # 不自動切換到小巷
    'organization_interrogation_room': ['帶到了審訊室'],
    'cold_prison_cell': ['拖回自己的牢房'],
    'busy_commercial_district': ['商業區的人群'],
    'private_hospital_ward': ['將和也安置入院'],
    'secret_medical_lab': ['秘密實驗室中'],
    'rainy_street_lamp': ['天空下著小雨'],
    'final_dark_alley': ['追兵已經逼近'],
}

# 全域變數，由 main() 設定
SCENE_MAPPING = {}

def detect_scene_from_text(text, current_scene):
    """從文字中偵測場景變化"""
    for scene, keywords in SCENE_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                if scene != current_scene:
                    return scene
    return None

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
    current_scene = None
    pending_scene = None  # 待切換的場景
    
    char_positions = {}  # 記錄角色當前位置
    pending_chars = []   # 收集同一段落要顯示的角色
    
    def queue_char(cid, emotion='normal'):
        """將角色加入待顯示列表"""
        pending_chars.append((cid, emotion))
    
    def flush_chars():
        """一次性處理所有待顯示的角色"""
        nonlocal char_positions
        if not pending_chars:
            return
        
        # 找出新角色和更新表情的角色
        new_chars = [(c, e) for c, e in pending_chars if c not in shown]
        update_chars = [(c, e) for c, e in pending_chars if c in shown and shown[c] != e]
        
        # 如果有新角色且已有一個角色，需要重新定位
        if new_chars and len(shown) == 1:
            other = list(shown.keys())[0]
            # 檢查是否有更新這個角色的表情
            updated_emotion = None
            for c, e in update_chars:
                if c == other:
                    updated_emotion = e
                    break
            other_emotion = updated_emotion if updated_emotion else shown[other]
            if char_positions.get(other) != 'left':
                result.append(f"hide character {other}")
                result.append(f"show character {other} {other_emotion} at left")
                char_positions[other] = 'left'
                shown[other] = other_emotion
            # 從更新列表中移除已處理的
            update_chars = [(c, e) for c, e in update_chars if c != other]
        
        # 顯示新角色
        for cid, emotion in new_chars:
            if len(shown) == 0 and len(new_chars) == 1:
                pos = 'center'
            elif len(shown) == 0 and len(new_chars) == 2:
                # 兩個新角色同時出現
                idx = [c for c, e in new_chars].index(cid)
                pos = 'left' if idx == 0 else 'right'
            else:
                pos = 'right'
            result.append(f"show character {cid} {emotion} at {pos} with fadeIn")
            char_positions[cid] = pos
            shown[cid] = emotion
        
        # 更新表情
        for cid, emotion in update_chars:
            pos = char_positions.get(cid, 'center')
            result.append(f"show character {cid} {emotion} at {pos}")
            shown[cid] = emotion
        
        pending_chars.clear()
    
    def change_scene(scene):
        nonlocal current_scene, shown
        if scene != current_scene:
            result.append(f"show scene {scene} with fadeIn")
            current_scene = scene
            shown.clear()  # 場景切換時清除角色
    
    def queue_scene_change(text):
        """檢查文字中是否有場景變化，排入待切換"""
        nonlocal pending_scene
        new_scene = detect_scene_from_text(text, current_scene)
        if new_scene and new_scene != current_scene:
            pending_scene = new_scene
    
    def flush_scene_change():
        """在文字輸出後執行場景切換"""
        nonlocal pending_scene
        if pending_scene:
            change_scene(pending_scene)
            pending_scene = None
    
    # 清理
    clean = re.sub(r'\{\s*/\*.*?\*/\s*\}', '', body).strip()
    clean = re.sub(r'\[\[.+?\]\]', '', clean).strip()
    
    # 初始場景（從 Twee 標記）
    m = re.search(r'\{\s*/\*\s*scene:\s*(\w+)\s*\*/\s*\}', body)
    if m:
        sid = SCENE_MAPPING.get(m.group(1), 'secluded_alleyway')
        change_scene(sid)
    
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
            
            narration = para[last_end:m.start()] + before
            if narration.strip():
                # 檢查場景變化（排入待處理）
                queue_scene_change(narration)
                
                # 輸出文字
                for s in split_text(narration.strip()):
                    result.append(s)
                
                # 文字輸出後切換場景
                flush_scene_change()
                
                # 顯示角色
                chars = detect_chars(narration)
                emotion = detect_emotion(narration)
                for cid in chars:
                    queue_char(cid, emotion)
                flush_chars()
            
            # 對話
            full_before = para[:m.start()] + before
            if is_dialogue(full_before):
                chars = detect_chars(before)
                speaker = chars[-1] if chars else last_speaker
                
                if speaker:
                    last_speaker = speaker
                    emotion = detect_emotion(quote)
                    queue_char(speaker, emotion)
                    flush_chars()
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
                # 檢查場景變化（排入待處理）
                queue_scene_change(remaining)
                
                for s in split_text(remaining):
                    result.append(s)
                
                # 文字輸出後切換場景
                flush_scene_change()
                
                chars = detect_chars(remaining)
                emotion = detect_emotion(remaining)
                for cid in chars:
                    queue_char(cid, emotion)
                flush_chars()
        
        # 沒有引號的段落
        if last_end == 0:
            # 檢查場景變化（排入待處理）
            queue_scene_change(para)
            
            for s in split_text(para):
                result.append(s)
            
            # 文字輸出後切換場景
            flush_scene_change()
            
            chars = detect_chars(para)
            emotion = detect_emotion(para)
            for cid in chars:
                queue_char(cid, emotion)
            flush_chars()
    
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

def load_scene_mapping(path: Path) -> dict:
    """載入場景對應表"""
    global SCENE_MAPPING
    try:
        with open(path, 'r', encoding='utf-8') as f:
            SCENE_MAPPING = json.load(f)
        return SCENE_MAPPING
    except FileNotFoundError:
        print(f"[Error] Scene mapping not found: {path}")
        print("Please provide --scene-mapping or ensure the file exists.")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"[Error] Invalid JSON in {path}: {e}")
        exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='智慧轉換 Twee 到 Monogatari script.js',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
範例:
  # 使用專案目錄（自動找檔案）
  python convert_full_story.py --project output/1140119_Temp

  # 指定個別檔案
  python convert_full_story.py --twee story.twee --scene-mapping scene-mapping.json --output script.js
        '''
    )
    parser.add_argument('--project', '-p', help='專案目錄路徑（會自動尋找 story.twee 等檔案）')
    parser.add_argument('--twee', help='Twee 檔案路徑')
    parser.add_argument('--scene-mapping', help='場景對應 JSON 路徑')
    parser.add_argument('--output', '-o', help='輸出 script.js 路徑')
    
    args = parser.parse_args()
    
    # 決定檔案路徑
    if args.project:
        project_dir = Path(args.project)
        twee_path = project_dir / 'story.twee'
        scene_mapping_path = project_dir / 'game' / 'scene-mapping.json'
        output_path = project_dir / 'monogatari-game' / 'js' / 'script.js'
    else:
        if not args.twee or not args.scene_mapping or not args.output:
            parser.error("請提供 --project 或同時提供 --twee, --scene-mapping, --output")
        twee_path = Path(args.twee)
        scene_mapping_path = Path(args.scene_mapping)
        output_path = Path(args.output)
    
    # 檢查檔案存在
    if not twee_path.exists():
        print(f"[Error] Twee file not found: {twee_path}")
        exit(1)
    
    # 載入場景對應
    load_scene_mapping(scene_mapping_path)
    
    # 轉換
    print("Converting story with scene detection...")
    passages = parse_twee(twee_path)
    print(f"Found {len(passages)} passages")
    
    js = generate_js(passages)
    
    # 確保輸出目錄存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(js, encoding='utf-8')
    print(f"Written to {output_path}")
    print("Done!")


if __name__ == '__main__':
    main()
