#!/usr/bin/env python3
"""
Monogatari 遊戲組裝器
根據規格書生成完整的 Monogatari 視覺小說
"""

import re
import json
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional

# 加入 shared 路徑
sys.path.insert(0, str(Path(__file__).parent.parent))
from shared.image_processor import process_character_sprites, HAS_REMBG
from shared.script_processor import ScriptProcessor, create_processor


class MonogatariBuilder:
    """組裝 Monogatari 視覺小說"""
    
    def __init__(self, output_dir: Path, char_mapping: Optional[Dict[str, str]] = None):
        """
        Args:
            output_dir: 輸出目錄
            char_mapping: 角色名稱對應表 {'中文名': 'char_id'}
        """
        self.output_dir = output_dir
        self.script_processor = create_processor(char_mapping)
        
    def build(
        self, 
        story_data: Dict, 
        assets_dir: Path, 
        title: str = "Visual Novel", 
        remove_bg: bool = True
    ):
        """組裝完整遊戲
        
        Args:
            story_data: 故事資料
            assets_dir: 素材目錄
            title: 遊戲標題
            remove_bg: 是否為角色立繪去背
        """
        print(f"[Build] Starting Monogatari build: {title}")
        
        # 建立目錄結構
        self._create_directories()
        
        # 複製素材（含去背處理）
        self._copy_assets(assets_dir, remove_bg=remove_bg)
        
        # 處理腳本（自動加入角色顯示指令）
        processed_script = self._process_script(story_data)
        
        # 生成 JS 檔案
        self._generate_characters_js(story_data)
        self._generate_scenes_js(story_data)
        self._generate_script_js(processed_script, story_data)
        self._generate_options_js(title)
        self._generate_storage_js()
        self._generate_main_js()
        
        # 生成 HTML
        self._generate_index_html(title)
        
        # 生成 CSS（含角色顯示調整）
        self._generate_main_css()
        
        # 設置引擎
        self._setup_engine()
        
        print(f"[Done] Game built at: {self.output_dir}")
        return self.output_dir
    
    def _process_script(self, story_data: Dict) -> Dict[str, List]:
        """處理腳本，自動加入角色顯示指令
        
        Args:
            story_data: 原始故事資料
            
        Returns:
            處理後的腳本
        """
        passages = story_data.get('passages', {})
        scene_mapping = story_data.get('scene_mapping', {})
        
        print("  Processing script (adding character show commands)...")
        
        processed = self.script_processor.process_script(passages, scene_mapping)
        
        return processed
    
    def _create_directories(self):
        """建立目錄結構"""
        dirs = [
            self.output_dir / 'js',
            self.output_dir / 'style',
            self.output_dir / 'assets' / 'characters',
            self.output_dir / 'assets' / 'scenes',
            self.output_dir / 'engine' / 'core',
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
    
    def _copy_assets(self, assets_dir: Path, remove_bg: bool = True):
        """複製素材並處理圖片"""
        # 複製角色
        src_chars = assets_dir / 'characters'
        dst_chars = self.output_dir / 'assets' / 'characters'
        if src_chars.exists():
            if dst_chars.exists():
                shutil.rmtree(dst_chars)
            shutil.copytree(src_chars, dst_chars)
            file_count = sum(1 for _ in dst_chars.rglob('*.png'))
            print(f"  Copied characters: {file_count} files")
            
            # 去背處理
            if remove_bg and HAS_REMBG:
                print("  Removing backgrounds from character sprites...")
                process_character_sprites(dst_chars, remove_bg=True)
                print("  Background removal complete!")
            elif remove_bg:
                print("  [Warning] rembg not installed, skipping background removal")
        
        # 複製場景
        src_scenes = assets_dir / 'scenes'
        dst_scenes = self.output_dir / 'assets' / 'scenes'
        if src_scenes.exists():
            if dst_scenes.exists():
                shutil.rmtree(dst_scenes)
            shutil.copytree(src_scenes, dst_scenes)
            print(f"  Copied scenes: {sum(1 for _ in dst_scenes.rglob('*.*'))} files")
    
    def _generate_characters_js(self, story_data: Dict):
        """生成 characters.js"""
        characters = {}
        
        for char in story_data.get('characters', []):
            char_id = char['id']
            
            # 收集表情
            sprites = {}
            for expr in char.get('expressions_needed', ['normal', 'happy', 'sad', 'angry', 'surprised']):
                sprites[expr] = f"{expr}.png"
            
            characters[char_id] = {
                'name': char.get('name', char_id),
                'color': self._get_char_color(char_id, char),
                'directory': char_id,
                'sprites': sprites
            }
        
        js_content = f"/* global monogatari */\n\nmonogatari.characters({json.dumps(characters, ensure_ascii=False, indent=2)});"
        
        (self.output_dir / 'js' / 'characters.js').write_text(js_content, encoding='utf-8')
        print(f"  Generated characters.js: {len(characters)} characters")
    
    def _get_char_color(self, char_id: str, char_data: Dict = None) -> str:
        """取得角色顏色"""
        if char_data and 'color' in char_data:
            return char_data['color']
        
        colors = {
            'kazuya': '#8b5cf6',
            'aiba': '#22c55e',
        }
        return colors.get(char_id, '#ffffff')
    
    def _generate_scenes_js(self, story_data: Dict):
        """生成 scenes.js"""
        scenes = {}
        
        for scene in story_data.get('scenes', []):
            scene_id = scene['id']
            scenes[scene_id] = f"{scene_id}/background.png"
        
        js_content = f"/* global monogatari */\n\nmonogatari.assets('scenes', {json.dumps(scenes, ensure_ascii=False, indent=2)});"
        
        (self.output_dir / 'js' / 'scenes.js').write_text(js_content, encoding='utf-8')
        print(f"  Generated scenes.js: {len(scenes)} scenes")
    
    def _generate_script_js(self, processed_script: Dict[str, List], story_data: Dict):
        """生成 script.js"""
        # 收集所有場景
        scenes = {s['id']: f"{s['id']}/background.png" for s in story_data.get('scenes', [])}
        
        # 收集所有角色
        characters = {}
        for char in story_data.get('characters', []):
            char_id = char['id']
            sprites = {}
            for expr in char.get('expressions_needed', ['normal', 'happy', 'sad', 'angry', 'surprised']):
                sprites[expr] = f"{expr}.png"
            characters[char_id] = {
                'name': char.get('name', char_id),
                'color': self._get_char_color(char_id, char),
                'directory': char_id,
                'sprites': sprites
            }
        
        # 建構 JS 內容
        lines = ["'use strict';\n/* global monogatari */\n"]
        
        # 場景
        lines.append(f"monogatari.assets('scenes', {json.dumps(scenes, ensure_ascii=False, indent=2)});\n")
        
        # 角色
        lines.append(f"monogatari.characters({json.dumps(characters, ensure_ascii=False, indent=2)});\n")
        
        # 腳本
        lines.append("monogatari.script({")
        
        passage_strs = []
        for name, commands in processed_script.items():
            formatted = self._format_commands(commands)
            passage_strs.append(f"\t'{name}': [\n{formatted}\n\t]")
        
        lines.append(',\n\n'.join(passage_strs))
        lines.append("\n});")
        
        js_content = '\n'.join(lines)
        (self.output_dir / 'js' / 'script.js').write_text(js_content, encoding='utf-8')
        print(f"  Generated script.js: {len(processed_script)} passages")
    
    def _format_commands(self, commands: List) -> str:
        """格式化指令列表"""
        formatted = []
        for cmd in commands:
            if isinstance(cmd, dict):
                # Choice 物件
                formatted.append(f"\t\t{json.dumps(cmd, ensure_ascii=False, indent=4)}")
            else:
                # 字串指令
                escaped = str(cmd).replace("'", "\\'")
                formatted.append(f"\t\t'{escaped}'")
        return ',\n'.join(formatted)
    
    def _generate_options_js(self, title: str):
        """生成 options.js"""
        options = f''''use strict';
/* global Monogatari */

// 正確取得 monogatari 實例
const {{ Monogatari: monogatari }} = Monogatari;

monogatari.settings({{
    "Name": "{title}",
    "Version": "1.0.0",
    "Label": "Start",
    "Slots": 10,
    "AutoSave": 0,
    "SaveLabel": "存檔",
    "AutoSaveLabel": "自動存檔",
    "SaveScreenshots": true,
    "ShowCredits": false,
    "TextSpeed": 30,
    "AutoPlaySpeed": 5,
    "MultiLanguage": false,
    "ShowMainScreen": true,
    "TypeAnimation": true,
    "NVL": false,
    "Preload": true,
    "AssetsPath": {{
        "root": "assets",
        "characters": "characters",
        "scenes": "scenes"
    }}
}});
'''
        (self.output_dir / 'js' / 'options.js').write_text(options, encoding='utf-8')
    
    def _generate_storage_js(self):
        """生成 storage.js"""
        storage = ''''use strict';
/* global monogatari */

monogatari.storage({
    player: {
        name: ""
    }
});
'''
        (self.output_dir / 'js' / 'storage.js').write_text(storage, encoding='utf-8')
    
    def _generate_main_js(self):
        """生成 main.js"""
        main = ''''use strict';
/* global Monogatari */
/* global monogatari */

const { $_ready } = Monogatari;

$_ready(() => {
    monogatari.init('#monogatari');
});
'''
        (self.output_dir / 'js' / 'main.js').write_text(main, encoding='utf-8')
    
    def _generate_index_html(self, title: str):
        """生成 index.html"""
        html = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no, maximum-scale=1">
    <title>{title}</title>
    
    <!-- Monogatari CSS -->
    <link rel="stylesheet" href="./engine/core/monogatari.css">
    <link rel="stylesheet" href="./style/main.css">
    
    <!-- Monogatari JS -->
    <script src="./engine/core/monogatari.js"></script>
    <script src="./js/options.js"></script>
    <script src="./js/storage.js"></script>
    <script src="./js/script.js"></script>
    <script src="./js/main.js"></script>
</head>
<body>
    <noscript>
        <div class="middle text--center">
            <h2>需要啟用 JavaScript</h2>
            <small>請啟用 JavaScript 或使用其他瀏覽器來遊玩此遊戲。</small>
        </div>
    </noscript>

    <div id="monogatari">
        <visual-novel>
            <loading-screen></loading-screen>
            <main-screen>
                <main-menu></main-menu>
            </main-screen>
            <game-screen>
                <dialog-log></dialog-log>
                <text-box></text-box>
                <quick-menu></quick-menu>
            </game-screen>
            <gallery-screen></gallery-screen>
            <load-screen></load-screen>
            <save-screen></save-screen>
            <settings-screen></settings-screen>
            <help-screen></help-screen>
        </visual-novel>
    </div>
</body>
</html>'''
        (self.output_dir / 'index.html').write_text(html, encoding='utf-8')
        print(f"  Generated index.html")
    
    def _generate_main_css(self):
        """生成 main.css（含角色顯示調整）"""
        css = '''/* Custom styles for visual novel */
body {
    margin: 0;
    padding: 0;
    overflow: hidden;
}

#monogatari {
    width: 100vw;
    height: 100vh;
}

/* 角色立繪大小和位置 */
[data-character] {
    max-height: 113vh !important;
    max-width: 53vw !important;
    bottom: 5vh !important;
    object-fit: contain !important;
    z-index: 100 !important;
    pointer-events: none !important;
}

/* 角色位置 */
[data-character][data-position="left"] {
    left: 5% !important;
}

[data-character][data-position="right"] {
    right: 5% !important;
}

[data-character][data-position="center"] {
    left: 50% !important;
    transform: translateX(-50%) !important;
}

/* 對話框背景 */
[data-component="text-box"] {
    background: rgba(0, 0, 0, 0.85) !important;
}
'''
        (self.output_dir / 'style' / 'main.css').write_text(css, encoding='utf-8')
        print(f"  Generated main.css (with character positioning)")
    
    def _setup_engine(self):
        """設置 Monogatari 引擎"""
        # 複製本地引擎檔案或使用 CDN
        template_dir = Path(__file__).parent.parent / 'templates' / 'monogatari'
        engine_src = template_dir / 'engine' / 'core'
        engine_dst = self.output_dir / 'engine' / 'core'
        
        if engine_src.exists():
            # 使用本地引擎
            if engine_dst.exists():
                shutil.rmtree(engine_dst)
            shutil.copytree(engine_src, engine_dst)
            print("  Copied Monogatari engine from templates")
        else:
            # 檢查是否已有引擎
            if not (engine_dst / 'monogatari.js').exists():
                print("  [Warning] Monogatari engine not found. Please copy engine files to:")
                print(f"    {engine_dst}")


def build_from_twee(
    twee_path: Path,
    assets_dir: Path,
    scene_mapping: Dict[str, str],
    output_dir: Path,
    title: str = "Visual Novel",
    char_mapping: Optional[Dict[str, str]] = None,
    assets_data: Optional[Dict] = None
):
    """從 Twee 檔案建構遊戲"""
    
    # 自動從 assets_data 建立角色對應表
    if char_mapping is None and assets_data:
        char_mapping = {}
        for char in assets_data.get('characters', []):
            char_name = char.get('name', '')
            char_id = char.get('id', '')
            if char_name and char_id:
                char_mapping[char_name] = char_id
        print(f"  Auto-generated character mapping: {char_mapping}")
    
    twee_content = twee_path.read_text(encoding='utf-8')
    
    # 提取標題
    title_match = re.search(r':: StoryTitle\r?\n(.+?)(?=\r?\n::|\Z)', twee_content, re.DOTALL)
    if title_match:
        title = title_match.group(1).strip()
    
    # 解析段落
    passages = {}
    parts = re.split(r'\n:: ', twee_content)
    
    for part in parts[1:]:
        lines = part.strip().split('\n')
        if not lines:
            continue
        
        name = lines[0].strip()
        if name in ['StoryTitle', 'StoryData']:
            continue
        
        body = '\n'.join(lines[1:])
        
        # 提取場景
        scene_match = re.search(r'\{\s*/\*\s*scene:\s*(\w+)\s*\*/\s*\}', body)
        scene_code = scene_match.group(1) if scene_match else None
        
        # 清理文字
        clean_body = re.sub(r'\{\s*/\*.*?\*/\s*\}', '', body).strip()
        
        # 提取選項
        choices = []
        for choice_text, target in re.findall(r'\[\[(.+?)->(\w+)\]\]', clean_body):
            choices.append({'text': choice_text, 'target': target})
        
        # 移除選項標記
        text = re.sub(r'\[\[.+?->\w+\]\]', '', clean_body).strip()
        
        passages[name] = {
            'scene_code': scene_code,
            'text': text,
            'choices': choices
        }
    
    # 建構故事資料
    story_data = {
        'characters': assets_data.get('characters', []) if assets_data else [],
        'scenes': assets_data.get('scenes', []) if assets_data else [],
        'passages': passages,
        'scene_mapping': scene_mapping
    }
    
    # 建構遊戲
    builder = MonogatariBuilder(output_dir, char_mapping)
    return builder.build(story_data, assets_dir, title)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Build Monogatari visual novel')
    parser.add_argument('--twee', required=True, help='Twee file path')
    parser.add_argument('--assets', required=True, help='Assets directory')
    parser.add_argument('--assets-json', help='assets-needed.json path')
    parser.add_argument('--scene-mapping', help='Scene mapping JSON')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    parser.add_argument('--title', default='Visual Novel', help='Game title')
    parser.add_argument('--no-rembg', action='store_true', help='Skip background removal')
    
    args = parser.parse_args()
    
    # 載入場景對應
    scene_mapping = {}
    if args.scene_mapping:
        with open(args.scene_mapping, 'r', encoding='utf-8') as f:
            scene_mapping = json.load(f)
    
    # 載入素材資料
    assets_data = {}
    if args.assets_json:
        with open(args.assets_json, 'r', encoding='utf-8') as f:
            assets_data = json.load(f)
    
    build_from_twee(
        Path(args.twee),
        Path(args.assets),
        scene_mapping,
        Path(args.output),
        args.title,
        assets_data=assets_data
    )


if __name__ == '__main__':
    main()
