#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monogatari 遊戲輸出器"""

import shutil
from pathlib import Path
from typing import Dict

from script_generator import ScriptGenerator


class MonogatariExporter:
    """Monogatari 遊戲輸出器"""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.script_gen = ScriptGenerator(config)
    
    def export(self, processed_data: Dict, assets_dir: str, 
               output_dir: str, template_dir: str = None) -> str:
        """
        輸出完整的 Monogatari 遊戲
        
        Args:
            processed_data: processed.json 的內容
            assets_dir: 素材目錄（包含 characters/ 和 scenes/）
            output_dir: 輸出目錄
            template_dir: Monogatari 模板目錄
        
        Returns:
            輸出目錄路徑
        """
        output_dir = Path(output_dir)
        assets_dir = Path(assets_dir)
        
        title = processed_data.get('title', '視覺小說')
        characters = processed_data.get('characters', [])
        scenes = processed_data.get('scenes', [])
        passages = processed_data.get('passages', [])
        
        # 建立目錄結構
        (output_dir / 'js').mkdir(parents=True, exist_ok=True)
        (output_dir / 'style').mkdir(exist_ok=True)
        (output_dir / 'assets' / 'characters').mkdir(parents=True, exist_ok=True)
        (output_dir / 'assets' / 'scenes').mkdir(exist_ok=True)
        
        # 複製 Monogatari 引擎
        if template_dir:
            self._copy_engine(template_dir, output_dir)
        
        # 生成 JavaScript 檔案
        self._generate_js_files(output_dir, title, characters, scenes, passages)
        
        # 生成 HTML
        self._generate_html(output_dir, title)
        
        # 生成 CSS
        self._generate_css(output_dir)
        
        # 複製素材
        self._copy_assets(assets_dir, output_dir)
        
        return str(output_dir)
    
    def _copy_engine(self, template_dir: str, output_dir: Path):
        """複製 Monogatari 引擎"""
        template_dir = Path(template_dir)
        dist_src = template_dir / 'dist'
        
        if dist_src.exists():
            dist_dst = output_dir / 'dist'
            if dist_dst.exists():
                shutil.rmtree(dist_dst)
            shutil.copytree(dist_src, dist_dst)
    
    def _generate_js_files(self, output_dir: Path, title: str,
                          characters: list, scenes: list, passages: list):
        """生成所有 JavaScript 檔案"""
        js_dir = output_dir / 'js'
        
        # script.js
        script_content = self.script_gen.generate_script(passages, characters, scenes)
        (js_dir / 'script.js').write_text(script_content, encoding='utf-8')
        
        # characters.js
        chars_content = self.script_gen.generate_characters_js(characters)
        (js_dir / 'characters.js').write_text(chars_content, encoding='utf-8')
        
        # scenes.js
        scenes_content = self.script_gen.generate_scenes_js(scenes)
        (js_dir / 'scenes.js').write_text(scenes_content, encoding='utf-8')
        
        # options.js
        options_content = self.script_gen.generate_options_js(title)
        (js_dir / 'options.js').write_text(options_content, encoding='utf-8')
        
        # main.js
        main_content = self.script_gen.generate_main_js()
        (js_dir / 'main.js').write_text(main_content, encoding='utf-8')
        
        # storage.js
        storage_content = self.script_gen.generate_storage_js()
        (js_dir / 'storage.js').write_text(storage_content, encoding='utf-8')
    
    def _generate_html(self, output_dir: Path, title: str):
        """生成 index.html"""
        html = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
    <title>{title}</title>
    
    <!-- Monogatari CSS -->
    <link rel="stylesheet" href="dist/engine/core/monogatari.css">
    <link rel="stylesheet" href="style/main.css">
</head>
<body>
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
    
    <!-- Monogatari Engine -->
    <script src="dist/engine/core/monogatari.js"></script>
    
    <!-- Game Scripts -->
    <script src="js/options.js"></script>
    <script src="js/storage.js"></script>
    <script src="js/characters.js"></script>
    <script src="js/scenes.js"></script>
    <script src="js/script.js"></script>
    <script src="js/main.js"></script>
</body>
</html>
'''
        (output_dir / 'index.html').write_text(html, encoding='utf-8')
    
    def _generate_css(self, output_dir: Path):
        """生成自訂 CSS"""
        css = '''/* Custom Styles for Visual Novel */

body {
    margin: 0;
    padding: 0;
    overflow: hidden;
    background: #000;
}

#monogatari {
    width: 100vw;
    height: 100vh;
}

/* 對話框樣式 */
.text-box {
    background: rgba(0, 0, 0, 0.85) !important;
    border-top: 2px solid rgba(255, 255, 255, 0.2);
}

/* 角色名稱 */
[data-character] {
    font-weight: bold;
    margin-bottom: 5px;
}

/* 選項樣式 */
.choice-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 20px;
}

.choice-container button {
    background: rgba(0, 0, 0, 0.8);
    border: 2px solid rgba(255, 255, 255, 0.3);
    color: white;
    padding: 15px 30px;
    font-size: 1.1em;
    cursor: pointer;
    transition: all 0.3s ease;
    border-radius: 5px;
}

.choice-container button:hover {
    background: rgba(255, 255, 255, 0.2);
    border-color: white;
    transform: translateX(10px);
}

/* 快速選單 */
quick-menu {
    background: rgba(0, 0, 0, 0.5) !important;
}

/* 載入畫面 */
loading-screen {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}

/* 主選單 */
main-menu {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}
'''
        (output_dir / 'style' / 'main.css').write_text(css, encoding='utf-8')
    
    def _copy_assets(self, assets_dir: Path, output_dir: Path):
        """複製素材"""
        # 複製角色
        chars_src = assets_dir / 'characters'
        chars_dst = output_dir / 'assets' / 'characters'
        if chars_src.exists():
            if chars_dst.exists():
                shutil.rmtree(chars_dst)
            shutil.copytree(chars_src, chars_dst)
        
        # 複製場景
        scenes_src = assets_dir / 'scenes'
        scenes_dst = output_dir / 'assets' / 'scenes'
        if scenes_src.exists():
            if scenes_dst.exists():
                shutil.rmtree(scenes_dst)
            shutil.copytree(scenes_src, scenes_dst)
