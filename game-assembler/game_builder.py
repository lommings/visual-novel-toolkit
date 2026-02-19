#!/usr/bin/env python3
"""
遊戲組裝器
將增強版 Twee + 素材組裝成可玩的視覺小說
"""

import re
import json
import shutil
import base64
from pathlib import Path
from typing import Dict, List, Optional


class GameBuilder:
    """組裝視覺小說遊戲"""
    
    # SugarCube 格式的 HTML 模板
    GAME_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            background: #1a1a2e;
            color: #eee;
            font-family: 'Noto Sans TC', 'Microsoft JhengHei', sans-serif;
            min-height: 100vh;
        }}
        
        #game-container {{
            max-width: 1200px;
            margin: 0 auto;
            position: relative;
        }}
        
        #scene-bg {{
            width: 100%;
            height: 70vh;
            background-size: cover;
            background-position: center;
            position: relative;
        }}
        
        #characters {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            display: flex;
            justify-content: center;
            gap: 20px;
            padding: 20px;
        }}
        
        .character {{
            max-height: 60vh;
            filter: drop-shadow(0 5px 15px rgba(0,0,0,0.5));
            transition: all 0.3s ease;
        }}
        
        .character.speaking {{
            transform: scale(1.05);
            filter: drop-shadow(0 5px 20px rgba(255,255,255,0.3));
        }}
        
        #dialogue-box {{
            background: linear-gradient(180deg, rgba(0,0,0,0.8) 0%, rgba(20,20,40,0.95) 100%);
            padding: 30px;
            min-height: 25vh;
            border-top: 2px solid #4a4a6a;
        }}
        
        #speaker-name {{
            color: #7dd3fc;
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 15px;
            text-shadow: 0 0 10px rgba(125, 211, 252, 0.5);
        }}
        
        #dialogue-text {{
            font-size: 1.1em;
            line-height: 1.8;
            margin-bottom: 20px;
        }}
        
        #choices {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        
        .choice-btn {{
            background: linear-gradient(90deg, #2d2d4a 0%, #3d3d5a 100%);
            border: 1px solid #5a5a7a;
            color: #eee;
            padding: 15px 25px;
            font-size: 1em;
            cursor: pointer;
            text-align: left;
            transition: all 0.2s ease;
            border-radius: 5px;
        }}
        
        .choice-btn:hover {{
            background: linear-gradient(90deg, #3d3d5a 0%, #4d4d6a 100%);
            border-color: #7dd3fc;
            transform: translateX(10px);
        }}
        
        #click-to-continue {{
            text-align: center;
            color: #888;
            font-size: 0.9em;
            animation: blink 1.5s infinite;
        }}
        
        @keyframes blink {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.3; }}
        }}
    </style>
</head>
<body>
    <div id="game-container">
        <div id="scene-bg">
            <div id="characters"></div>
        </div>
        <div id="dialogue-box">
            <div id="speaker-name"></div>
            <div id="dialogue-text"></div>
            <div id="choices"></div>
            <div id="click-to-continue">▼ 點擊繼續</div>
        </div>
    </div>
    
    <script>
        // 遊戲資料
        const gameData = {game_data};
        const assets = {assets_data};
        
        let currentPassage = 'Start';
        let currentTextIndex = 0;
        let textSegments = [];
        
        // 初始化
        function init() {{
            loadPassage(currentPassage);
            
            document.getElementById('dialogue-box').addEventListener('click', (e) => {{
                if (e.target.classList.contains('choice-btn')) return;
                nextText();
            }});
        }}
        
        // 載入段落
        function loadPassage(passageName) {{
            const passage = gameData.passages[passageName];
            if (!passage) {{
                console.error('Passage not found:', passageName);
                return;
            }}
            
            currentPassage = passageName;
            currentTextIndex = 0;
            
            // 設定場景
            if (passage.scene) {{
                setScene(passage.scene);
            }}
            
            // 設定角色
            if (passage.characters) {{
                setCharacters(passage.characters);
            }}
            
            // 分割文字
            textSegments = splitText(passage.text);
            
            // 儲存選項
            window.currentChoices = passage.choices || [];
            
            // 顯示第一段文字
            showText(0);
        }}
        
        // 設定場景背景
        function setScene(sceneId) {{
            const sceneBg = document.getElementById('scene-bg');
            const scenePath = assets.scenes[sceneId];
            if (scenePath) {{
                sceneBg.style.backgroundImage = `url(${{scenePath}})`;
            }}
        }}
        
        // 設定角色立繪
        function setCharacters(chars) {{
            const container = document.getElementById('characters');
            container.innerHTML = '';
            
            for (const [charId, expr] of Object.entries(chars)) {{
                const charAssets = assets.characters[charId];
                if (charAssets) {{
                    const img = document.createElement('img');
                    img.className = 'character';
                    img.id = `char-${{charId}}`;
                    img.src = charAssets[expr] || charAssets.base;
                    img.alt = charId;
                    container.appendChild(img);
                }}
            }}
        }}
        
        // 分割文字（以句號、問號、驚嘆號分割）
        function splitText(text) {{
            if (!text) return [];
            // 按標點符號分割，但保留標點
            const segments = text.match(/[^。！？\n]+[。！？]?/g) || [text];
            return segments.filter(s => s.trim()).map(s => s.trim());
        }}
        
        // 顯示文字
        function showText(index) {{
            const textEl = document.getElementById('dialogue-text');
            const choicesEl = document.getElementById('choices');
            const continueEl = document.getElementById('click-to-continue');
            
            if (index < textSegments.length) {{
                textEl.textContent = textSegments.slice(0, index + 1).join('');
                choicesEl.innerHTML = '';
                continueEl.style.display = 'block';
            }} else {{
                // 顯示選項
                continueEl.style.display = 'none';
                if (window.currentChoices.length > 0) {{
                    choicesEl.innerHTML = window.currentChoices.map(c => 
                        `<button class="choice-btn" onclick="loadPassage('${{c.target}}')">${{c.text}}</button>`
                    ).join('');
                }} else {{
                    // 沒有選項，遊戲結束
                    textEl.textContent += '\\n\\n【END】';
                }}
            }}
        }}
        
        // 下一段文字
        function nextText() {{
            currentTextIndex++;
            showText(currentTextIndex);
        }}
        
        // 更新角色表情
        function updateCharacterExpression(charId, expression) {{
            const charEl = document.getElementById(`char-${{charId}}`);
            const charAssets = assets.characters[charId];
            if (charEl && charAssets) {{
                charEl.src = charAssets[expression] || charAssets.base;
            }}
        }}
        
        // 啟動遊戲
        init();
    </script>
</body>
</html>'''
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def parse_enhanced_twee(self, twee_path: Path) -> Dict:
        """解析增強版 Twee 檔案"""
        content = twee_path.read_text(encoding='utf-8')
        
        # 提取標題
        title_match = re.search(r':: StoryTitle\r?\n(.+?)(?=\r?\n::|\Z)', content, re.DOTALL)
        title = title_match.group(1).strip() if title_match else "Visual Novel"
        
        # 提取段落
        passages = {}
        pattern = r':: (\w+)\r?\n(.*?)(?=\r?\n:: |\Z)'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for name, body in matches:
            if name in ['StoryTitle', 'StoryData']:
                continue
            
            passage_data = self._parse_passage_body(body)
            passages[name] = passage_data
        
        return {
            'title': title,
            'passages': passages
        }
    
    def _parse_passage_body(self, body: str) -> Dict:
        """解析段落內容"""
        result = {
            'scene': None,
            'characters': {},
            'text': '',
            'choices': []
        }
        
        lines = body.strip().split('\n')
        text_lines = []
        
        for line in lines:
            # 場景標記 [scene:xxx]
            scene_match = re.search(r'\[scene:(\w+)\]', line)
            if scene_match:
                result['scene'] = scene_match.group(1)
                continue
            
            # 角色標記 [char:xxx:expression]
            char_match = re.search(r'\[char:(\w+):(\w+)\]', line)
            if char_match:
                result['characters'][char_match.group(1)] = char_match.group(2)
                continue
            
            # 選項 [[text->target]]
            choice_match = re.search(r'\[\[(.+?)->(\w+)\]\]', line)
            if choice_match:
                result['choices'].append({
                    'text': choice_match.group(1),
                    'target': choice_match.group(2)
                })
                continue
            
            # 一般文字
            if line.strip():
                text_lines.append(line.strip())
        
        result['text'] = '\n'.join(text_lines)
        return result
    
    def collect_assets(self, assets_dir: Path) -> Dict:
        """收集素材路徑"""
        assets = {
            'characters': {},
            'scenes': {}
        }
        
        # 收集角色
        chars_dir = assets_dir / 'characters'
        if chars_dir.exists():
            for char_dir in chars_dir.iterdir():
                if char_dir.is_dir():
                    char_id = char_dir.name
                    assets['characters'][char_id] = {}
                    
                    for img in char_dir.glob('*.png'):
                        expr_name = img.stem  # base, normal, happy, etc.
                        # 使用相對路徑
                        assets['characters'][char_id][expr_name] = f'assets/characters/{char_id}/{img.name}'
        
        # 收集場景
        scenes_dir = assets_dir / 'scenes'
        if scenes_dir.exists():
            for scene_item in scenes_dir.iterdir():
                if scene_item.is_dir():
                    scene_id = scene_item.name
                    bg_file = scene_item / 'background.png'
                    if bg_file.exists():
                        assets['scenes'][scene_id] = f'assets/scenes/{scene_id}/background.png'
                elif scene_item.suffix in ['.png', '.jpg']:
                    scene_id = scene_item.stem
                    assets['scenes'][scene_id] = f'assets/scenes/{scene_item.name}'
        
        return assets
    
    def copy_assets(self, src_assets_dir: Path):
        """複製素材到輸出目錄"""
        dst_assets_dir = self.output_dir / 'assets'
        if dst_assets_dir.exists():
            shutil.rmtree(dst_assets_dir)
        shutil.copytree(src_assets_dir, dst_assets_dir)
    
    def build_game(self, twee_path: Path, assets_dir: Path) -> Path:
        """組裝遊戲"""
        # 解析 Twee
        game_data = self.parse_enhanced_twee(twee_path)
        print(f"📖 遊戲標題: {game_data['title']}")
        print(f"   段落數: {len(game_data['passages'])}")
        
        # 收集素材
        assets = self.collect_assets(assets_dir)
        print(f"   角色數: {len(assets['characters'])}")
        print(f"   場景數: {len(assets['scenes'])}")
        
        # 複製素材
        self.copy_assets(assets_dir)
        
        # 生成 HTML
        html = self.GAME_TEMPLATE.format(
            title=game_data['title'],
            game_data=json.dumps(game_data, ensure_ascii=False),
            assets_data=json.dumps(assets, ensure_ascii=False)
        )
        
        output_path = self.output_dir / 'game.html'
        output_path.write_text(html, encoding='utf-8')
        
        print(f"\n✅ 遊戲已組裝完成!")
        print(f"   輸出位置: {output_path}")
        
        return output_path


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='組裝視覺小說遊戲')
    parser.add_argument('twee_path', help='增強版 Twee 檔案')
    parser.add_argument('assets_dir', help='素材目錄')
    parser.add_argument('-o', '--output', help='輸出目錄', required=True)
    
    args = parser.parse_args()
    
    builder = GameBuilder(Path(args.output))
    builder.build_game(Path(args.twee_path), Path(args.assets_dir))


if __name__ == '__main__':
    main()
