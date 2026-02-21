#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prompt Editor Server - 提供 Prompt 編輯與即時生成 API
"""

import sys
import json
import argparse
import webbrowser
import threading
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import io

# 修復 Windows console 編碼問題
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

print("[DEBUG] Starting prompt_server...", flush=True)

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.config_manager import ConfigManager
from shared.file_utils import load_json, save_json, ensure_dir
from shared.visual_prompt_generator import VisualPromptGenerator

from preview_generator import PreviewGenerator


class PromptEditorHandler(SimpleHTTPRequestHandler):
    """處理 Prompt Editor 的 HTTP 請求"""
    
    def __init__(self, *args, preview_dir=None, assets_data=None, config=None, generator=None, visual_gen=None, **kwargs):
        self.preview_dir = preview_dir
        self.assets_data = assets_data
        self.config = config
        self.generator = generator
        self.visual_gen = visual_gen
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """處理 GET 請求"""
        parsed = urlparse(self.path)
        print(f"[DEBUG] GET request: {parsed.path}")
        
        if parsed.path == '/' or parsed.path == '/index.html':
            self.serve_prompt_editor()
        elif parsed.path == '/preview.html':
            self.serve_preview_page()
        elif parsed.path == '/api/load-session':
            self.handle_load_session()
        else:
            # 靜態檔案 - 從 preview_dir 提供
            file_path = self.preview_dir / parsed.path.lstrip('/')
            print(f"[DEBUG] Serving file: {file_path}")
            
            if file_path.exists() and file_path.is_file():
                # 判斷 content type
                suffix = file_path.suffix.lower()
                content_types = {
                    '.png': 'image/png',
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.gif': 'image/gif',
                    '.html': 'text/html',
                    '.css': 'text/css',
                    '.js': 'application/javascript',
                    '.json': 'application/json'
                }
                content_type = content_types.get(suffix, 'application/octet-stream')
                
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', file_path.stat().st_size)
                self.end_headers()
                
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                print(f"[DEBUG] File not found: {file_path}")
                self.send_error(404, f"File not found: {parsed.path}")
    
    def do_POST(self):
        """處理 POST 請求"""
        parsed = urlparse(self.path)
        print(f"[DEBUG] POST request to: {parsed.path}")
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        print(f"[DEBUG] Body: {body[:200] if body else 'empty'}")
        
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self.send_json_response({'success': False, 'error': 'Invalid JSON'}, 400)
            return
        
        if parsed.path == '/api/generate-character':
            self.handle_generate_character(data)
        elif parsed.path == '/api/generate-scene':
            self.handle_generate_scene(data)
        elif parsed.path == '/api/generate-visual-prompt':
            self.handle_generate_visual_prompt(data)
        elif parsed.path == '/api/save-prompts':
            self.handle_save_prompts(data)
        elif parsed.path == '/api/save-selections':
            self.handle_save_selections(data)
        elif parsed.path == '/api/save-session':
            self.handle_save_session(data)
        elif parsed.path == '/api/export-assets':
            self.handle_export_assets(data)
        elif parsed.path == '/api/generate-expressions':
            self.handle_generate_expressions(data)
        else:
            self.send_json_response({'success': False, 'error': 'Not found'}, 404)
    
    def serve_prompt_editor(self):
        """提供 Prompt 編輯頁面"""
        template_path = Path(__file__).parent / 'templates' / 'prompt-editor.html'
        
        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # 注入資料
        html = html.replace('{{ASSETS_DATA}}', json.dumps(self.assets_data, ensure_ascii=False))
        html = html.replace('{{CONFIG_DATA}}', json.dumps(self.config, ensure_ascii=False))
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_preview_page(self):
        """提供預覽選擇頁面"""
        preview_html = self.preview_dir / 'preview.html'
        if preview_html.exists():
            with open(preview_html, 'r', encoding='utf-8') as f:
                html = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_json_response({'error': '尚未生成預覽'}, 404)
    
    def handle_generate_character(self, data):
        """生成角色預覽圖"""
        char_id = data.get('id', '')
        prompt = data.get('prompt', '')
        count = data.get('count', 4)
        
        if not char_id or not prompt:
            self.send_json_response({'success': False, 'error': '缺少必要參數'}, 400)
            return
        
        # 找到角色資料
        char_data = None
        for char in self.assets_data.get('characters', []):
            if char.get('id') == char_id:
                char_data = char.copy()
                break
        
        if not char_data:
            self.send_json_response({'success': False, 'error': '找不到角色'}, 404)
            return
        
        # 使用編輯後的 prompt
        char_data['visual_description'] = prompt
        
        try:
            # 生成預覽
            output_dir = self.preview_dir / 'characters' / char_id
            ensure_dir(output_dir)
            
            paths = self.generator.generate_character_preview(
                char_data, 
                str(output_dir),
                count=count
            )
            
            # 轉換為相對路徑
            rel_paths = [f"characters/{char_id}/{Path(p).name}" for p in paths]
            
            self.send_json_response({
                'success': True,
                'images': rel_paths
            })
            
        except Exception as e:
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, 500)
    
    def handle_generate_scene(self, data):
        """生成場景預覽圖"""
        scene_id = data.get('id', '')
        prompt = data.get('prompt', '')
        model = data.get('model', 'stable_diffusion')
        sd_model = data.get('sd_model', '')  # SD 模型檔名
        style = data.get('style', 'anime')
        count = data.get('count', 3)
        
        print(f"[DEBUG] generate_scene: model={model}, sd_model={sd_model}")
        
        if not scene_id or not prompt:
            self.send_json_response({'success': False, 'error': '缺少必要參數'}, 400)
            return
        
        # 找到場景資料
        scene_data = None
        for scene in self.assets_data.get('scenes', []):
            if scene.get('id') == scene_id:
                scene_data = scene.copy()
                break
        
        if not scene_data:
            self.send_json_response({'success': False, 'error': '找不到場景'}, 404)
            return
        
        # 使用編輯後的 prompt
        scene_data['visual_description'] = prompt
        
        try:
            # 如果使用 SD 且指定了模型，先切換模型
            if model == 'stable_diffusion' and sd_model:
                self._switch_sd_model(sd_model)
            
            # 生成預覽（支援指定模型和風格）
            output_dir = self.preview_dir / 'scenes' / scene_id
            ensure_dir(output_dir)
            
            paths = self.generator.generate_scene_preview(
                scene_data,
                str(output_dir),
                count=count,
                model=model,
                style=style
            )
            
            # 轉換為相對路徑
            rel_paths = [f"scenes/{scene_id}/{Path(p).name}" for p in paths]
            
            self.send_json_response({
                'success': True,
                'images': rel_paths
            })
            
        except Exception as e:
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, 500)
    
    def handle_generate_visual_prompt(self, data):
        """使用 AI 生成視覺描述 Prompt"""
        import sys
        print(f"[DEBUG] generate_visual_prompt called with: {data}")
        sys.stdout.flush()
        item_type = data.get('type', '')  # 'character' or 'scene'
        item_id = data.get('id', '')
        
        if not item_type or not item_id:
            self.send_json_response({'success': False, 'error': '缺少必要參數'}, 400)
            return
        
        try:
            if item_type == 'character':
                # 找到角色資料
                char_data = None
                for char in self.assets_data.get('characters', []):
                    if char.get('id') == item_id:
                        char_data = char
                        break
                
                if not char_data:
                    self.send_json_response({'success': False, 'error': '找不到角色'}, 404)
                    return
                
                # 生成視覺描述
                print(f"[DEBUG] Calling generate_character_visual_prompt for {char_data.get('name')}")
                sys.stdout.flush()
                
                updated = self.visual_gen.generate_character_visual_prompt(char_data)
                
                print(f"[DEBUG] Got result: {updated.get('visual_prompt', '')[:50]}...")
                sys.stdout.flush()
                
                self.send_json_response({
                    'success': True,
                    'visual_prompt': updated.get('visual_prompt', ''),
                    'visual_details': updated.get('visual_details', {})
                })
                
            elif item_type == 'scene':
                # 找到場景資料
                scene_data = None
                for scene in self.assets_data.get('scenes', []):
                    if scene.get('id') == item_id:
                        scene_data = scene
                        break
                
                if not scene_data:
                    self.send_json_response({'success': False, 'error': '找不到場景'}, 404)
                    return
                
                # 生成視覺描述
                updated = self.visual_gen.generate_scene_visual_prompt(scene_data)
                
                self.send_json_response({
                    'success': True,
                    'visual_prompt': updated.get('visual_prompt', ''),
                    'visual_details': updated.get('visual_details', {})
                })
            else:
                self.send_json_response({'success': False, 'error': '不支援的類型'}, 400)
                
        except Exception as e:
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, 500)
    
    def handle_save_prompts(self, data):
        """儲存編輯後的 Prompts"""
        try:
            output_path = self.preview_dir / 'edited-prompts.json'
            save_json(data, output_path)
            
            self.send_json_response({
                'success': True,
                'path': str(output_path)
            })
        except Exception as e:
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, 500)
    
    def _switch_sd_model(self, model_name):
        """切換 SD 模型"""
        import requests
        
        sd_config = self.config.get('image_generation', {}).get('stable_diffusion', {})
        api_url = sd_config.get('api_url', 'http://localhost:7860')
        
        try:
            # 取得當前模型
            response = requests.get(f"{api_url}/sdapi/v1/options", timeout=5)
            if response.status_code == 200:
                current_model = response.json().get('sd_model_checkpoint', '')
                if current_model != model_name:
                    print(f"[DEBUG] 切換 SD 模型: {current_model} -> {model_name}")
                    # 切換模型
                    requests.post(
                        f"{api_url}/sdapi/v1/options",
                        json={"sd_model_checkpoint": model_name},
                        timeout=120  # 切換模型可能需要時間
                    )
        except Exception as e:
            print(f"[WARN] 無法切換 SD 模型: {e}")
    
    def handle_save_selections(self, data):
        """儲存選擇結果"""
        try:
            output_path = self.preview_dir / 'selections.json'
            save_json(data, output_path)
            
            self.send_json_response({
                'success': True,
                'path': str(output_path)
            })
        except Exception as e:
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, 500)
    
    def handle_save_session(self, data):
        """儲存完整工作階段（包含編輯資料和已生成的圖片路徑）"""
        try:
            output_path = self.preview_dir / 'session.json'
            save_json(data, output_path)
            print(f"[DEBUG] Session saved to {output_path}")
            
            self.send_json_response({
                'success': True,
                'path': str(output_path)
            })
        except Exception as e:
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, 500)
    
    def handle_load_session(self):
        """載入工作階段"""
        try:
            session_path = self.preview_dir / 'session.json'
            if session_path.exists():
                session_data = load_json(session_path)
                self.send_json_response({
                    'success': True,
                    'data': session_data
                })
            else:
                self.send_json_response({
                    'success': False,
                    'error': '無儲存的工作階段'
                })
        except Exception as e:
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, 500)
    
    def handle_export_assets(self, data):
        """匯出選定的素材到最終目錄"""
        import shutil
        
        try:
            # 建立輸出目錄
            output_dir = self.preview_dir.parent / 'assets'
            chars_dir = output_dir / 'characters'
            scenes_dir = output_dir / 'scenes'
            
            ensure_dir(chars_dir)
            ensure_dir(scenes_dir)
            
            chars_count = 0
            scenes_count = 0
            
            # 匯出角色
            expressions_count = 0
            for char_id, char_data in data.get('characters', {}).items():
                src_path = self.preview_dir / char_data['selected_image']
                if src_path.exists():
                    # 複製到 assets/characters/角色id/
                    char_dir = chars_dir / char_id
                    ensure_dir(char_dir)
                    dst_path = char_dir / 'base.png'
                    shutil.copy2(src_path, dst_path)
                    
                    # 匯出所有表情
                    exported_expressions = {}
                    expressions = char_data.get('expressions', {})
                    if expressions:
                        for expr_name, expr_path in expressions.items():
                            expr_src = self.preview_dir / expr_path
                            if expr_src.exists():
                                expr_dst = char_dir / f'{expr_name}.png'
                                shutil.copy2(expr_src, expr_dst)
                                exported_expressions[expr_name] = f'{expr_name}.png'
                                expressions_count += 1
                                print(f"[DEBUG] 匯出表情: {char_id}/{expr_name}.png")
                    
                    # 儲存角色資訊
                    info = {
                        'id': char_id,
                        'prompt': char_data.get('prompt', ''),
                        'style': char_data.get('style', 'anime'),
                        'source_image': char_data['selected_image'],
                        'expressions': exported_expressions
                    }
                    save_json(info, char_dir / 'info.json')
                    chars_count += 1
            
            # 匯出場景
            for scene_id, scene_data in data.get('scenes', {}).items():
                src_path = self.preview_dir / scene_data['selected_image']
                if src_path.exists():
                    # 複製到 assets/scenes/場景id/
                    scene_dir = scenes_dir / scene_id
                    ensure_dir(scene_dir)
                    dst_path = scene_dir / 'background.png'
                    shutil.copy2(src_path, dst_path)
                    
                    # 儲存場景資訊
                    info = {
                        'id': scene_id,
                        'prompt': scene_data.get('prompt', ''),
                        'model': scene_data.get('model', ''),
                        'sd_model': scene_data.get('sd_model', ''),
                        'style': scene_data.get('style', 'anime'),
                        'source_image': scene_data['selected_image']
                    }
                    save_json(info, scene_dir / 'info.json')
                    scenes_count += 1
            
            # 儲存匯出摘要
            summary = {
                'exported_at': str(Path.cwd()),
                'characters': list(data.get('characters', {}).keys()),
                'scenes': list(data.get('scenes', {}).keys())
            }
            save_json(summary, output_dir / 'export_summary.json')
            
            self.send_json_response({
                'success': True,
                'output_dir': str(output_dir),
                'characters_count': chars_count,
                'scenes_count': scenes_count,
                'expressions_count': expressions_count
            })
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, 500)
    
    def handle_generate_expressions(self, data):
        """根據選定的參考圖生成角色所有表情"""
        char_id = data.get('id', '')
        reference_path = data.get('reference_path', '')
        prompt = data.get('prompt', '')  # 接收儲存的 prompt
        method = data.get('method', 'sd')  # 'sd' 或 'ai'，預設用 SD
        denoising = data.get('denoising', 0.35)  # SD denoising strength
        
        if not char_id or not reference_path:
            self.send_json_response({'success': False, 'error': '缺少必要參數'}, 400)
            return
        
        # 找到角色資料
        char_data = None
        for char in self.assets_data.get('characters', []):
            if char.get('id') == char_id:
                char_data = char.copy()
                break
        
        if not char_data:
            self.send_json_response({'success': False, 'error': '找不到角色'}, 404)
            return
        
        # 使用傳入的 prompt
        if prompt:
            char_data['visual_description'] = prompt
            char_data['visual_prompt'] = prompt
            print(f"[DEBUG] 使用儲存的 prompt: {prompt[:50]}...")
        
        # 如果參考路徑是相對路徑，轉為絕對路徑
        if not Path(reference_path).is_absolute():
            reference_path = str(self.preview_dir / reference_path)
        
        if not Path(reference_path).exists():
            self.send_json_response({'success': False, 'error': '參考圖不存在'}, 404)
            return
        
        try:
            output_dir = self.preview_dir / 'expressions' / char_id
            ensure_dir(output_dir)
            
            # 取得表情列表
            expressions = char_data.get('expressions_needed', 
                                       char_data.get('expressions', ['normal', 'happy', 'sad', 'angry', 'surprised']))
            
            if method == 'sd':
                # 使用 SD img2img 生成
                from shared.sd_expression_generator import SDExpressionGenerator
                sd_gen = SDExpressionGenerator(self.config)
                
                if not sd_gen.test_connection():
                    self.send_json_response({
                        'success': False, 
                        'error': 'SD WebUI 未運行，請先啟動 SD WebUI (localhost:7860)'
                    }, 503)
                    return
                
                print(f"[SD] Generating expressions with denoising={denoising}")
                results = sd_gen.generate_all_expressions(
                    reference_path=reference_path,
                    expressions=expressions,
                    output_dir=str(output_dir),
                    base_prompt=prompt,
                    denoising_strength=denoising
                )
            else:
                # 使用 AI (Imagen/Gemini) 生成
                results = self.generator.generate_final_character(
                    character=char_data,
                    reference_path=reference_path,
                    output_dir=str(output_dir)
                )
            
            # 轉換為相對路徑
            rel_results = {}
            for expr, path in results.items():
                rel_path = Path(path).relative_to(self.preview_dir)
                rel_results[expr] = str(rel_path).replace('\\', '/')
            
            self.send_json_response({
                'success': True,
                'expressions': rel_results,
                'reference_used': reference_path,
                'method': method
            })
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.send_json_response({
                'success': False,
                'error': str(e)
            }, 500)
    
    def send_json_response(self, data, status=200):
        """發送 JSON 回應"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def log_message(self, format, *args):
        """自訂日誌格式"""
        print(f"   [{self.log_date_time_string()}] {args[0]}")


def create_handler(preview_dir, assets_data, config, generator, visual_gen):
    """建立帶有資料的 Handler 類別"""
    class CustomHandler(PromptEditorHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(
                *args,
                preview_dir=preview_dir,
                assets_data=assets_data,
                config=config,
                generator=generator,
                visual_gen=visual_gen,
                **kwargs
            )
    return CustomHandler


def main():
    """主程式"""
    parser = argparse.ArgumentParser(
        description='啟動 Prompt 編輯器伺服器'
    )
    parser.add_argument('input', help='assets-needed.json 路徑')
    parser.add_argument('-o', '--output', help='輸出目錄', default=None)
    parser.add_argument('-c', '--config', help='設定檔路徑', default=None)
    parser.add_argument('-p', '--port', type=int, default=8080, help='伺服器端口')
    parser.add_argument('--no-browser', action='store_true', help='不自動開啟瀏覽器')
    
    args = parser.parse_args()
    
    # 載入設定
    config = ConfigManager.load(args.config)
    
    # 讀取素材需求
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ 檔案不存在: {input_path}")
        sys.exit(1)
    
    assets_data = load_json(input_path)
    
    print(f"📖 讀取素材需求: {input_path.name}")
    print(f"   角色: {len(assets_data.get('characters', []))} 人")
    print(f"   場景: {len(assets_data.get('scenes', []))} 個")
    
    # 決定輸出目錄
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = input_path.parent
    
    preview_dir = (output_dir / 'preview').resolve()  # 使用絕對路徑
    ensure_dir(preview_dir)
    
    # 初始化生成器
    generator = PreviewGenerator(config)
    visual_gen = VisualPromptGenerator(config)
    
    print(f"   預覽目錄: {preview_dir}")
    
    # 建立伺服器
    handler = create_handler(preview_dir, assets_data, config, generator, visual_gen)
    server = HTTPServer(('localhost', args.port), handler)
    
    url = f"http://localhost:{args.port}/"
    print(f"\n🌐 Prompt 編輯器已啟動: {url}")
    print("   按 Ctrl+C 停止伺服器")
    
    # 自動開啟瀏覽器
    if not args.no_browser:
        webbrowser.open(url)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n伺服器已停止")


if __name__ == '__main__':
    main()
