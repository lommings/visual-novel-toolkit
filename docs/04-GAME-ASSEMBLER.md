# game-assembler 規格書

## 📋 功能概述

將處理好的文字資料與選好的圖片素材組合，輸出完整可遊玩的 Monogatari 視覺小說遊戲。

---

## 📥 輸入

| 項目 | 格式 | 說明 |
|------|------|------|
| processed.json | .json | twee-processor 輸出的故事資料 |
| assets/ | 資料夾 | asset-previewer 生成的圖片素材 |
| selections.json | .json | (可選) 素材選擇記錄，用於追蹤 |

### 輸入結構

```
input/
├── processed.json      # 故事資料（段落、對話、選項）
├── assets/
│   ├── characters/
│   │   ├── kazuya/
│   │   │   ├── normal.png
│   │   │   ├── sad.png
│   │   │   └── ...
│   │   └── aiba/
│   │       └── ...
│   └── scenes/
│       ├── home_living_room.jpg
│       └── repair_shop.jpg
└── selections.json     # (可選)
```

---

## 📤 輸出

完整的 Monogatari 遊戲：

```
output/遊戲名稱/
├── index.html              # 遊戲入口
├── js/
│   ├── script.js           # 遊戲腳本（對話、選項、分支）
│   ├── characters.js       # 角色定義
│   ├── scenes.js           # 場景定義
│   ├── options.js          # 遊戲設定
│   ├── storage.js          # 存檔設定
│   └── main.js             # 初始化
├── style/
│   └── main.css            # 自訂樣式
├── assets/
│   ├── characters/         # 角色立繪（複製過來）
│   └── scenes/             # 場景背景（複製過來）
└── dist/
    └── engine/             # Monogatari 引擎
        └── core/
            ├── monogatari.js
            └── monogatari.css
```

---

## ⚙️ 處理邏輯

### Step 1: 載入資料

```python
def load_inputs(processed_path: str, assets_path: str) -> dict:
    """載入所有輸入資料"""
    with open(processed_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)
    
    # 驗證素材完整性
    validate_assets(story_data, assets_path)
    
    return story_data
```

### Step 2: 生成角色定義 (characters.js)

```python
def generate_characters_js(characters: list) -> str:
    """
    生成 Monogatari 角色定義
    """
    char_dict = {}
    
    for char in characters:
        char_dict[char['id']] = {
            'name': char['name'],
            'color': char.get('color', '#ffffff'),
            'directory': char['id'],
            'sprites': {
                expr: f"{expr}.png" 
                for expr in char['expressions']
            }
        }
    
    return f"monogatari.characters({json.dumps(char_dict, ensure_ascii=False, indent=2)});"
```

輸出範例：
```javascript
monogatari.characters({
  "kazuya": {
    "name": "和也",
    "color": "#4A90D9",
    "directory": "kazuya",
    "sprites": {
      "normal": "normal.png",
      "sad": "sad.png",
      "surprised": "surprised.png"
    }
  },
  "aiba": {
    "name": "相葉",
    "color": "#7CB342",
    "directory": "aiba",
    "sprites": {
      "normal": "normal.png",
      "gentle": "gentle.png"
    }
  }
});
```

### Step 3: 生成場景定義 (scenes.js)

```python
def generate_scenes_js(scenes: list) -> str:
    """生成 Monogatari 場景定義"""
    scene_dict = {
        scene['id']: f"{scene['id']}.jpg"
        for scene in scenes
    }
    
    return f"monogatari.assets('scenes', {json.dumps(scene_dict, ensure_ascii=False, indent=2)});"
```

### Step 4: 生成遊戲腳本 (script.js)

這是最重要的部分，將 processed.json 轉為 Monogatari 腳本。

```python
def generate_script_js(passages: list) -> str:
    """
    將故事段落轉換為 Monogatari 腳本格式
    """
    script = {}
    
    for passage in passages:
        lines = []
        current_scene = None
        shown_character = None
        
        # 場景切換
        if passage.get('scene_id') and passage['scene_id'] != current_scene:
            lines.append(f"show scene {passage['scene_id']} with fadeIn")
            current_scene = passage['scene_id']
        
        # 處理每一行
        for line in passage['lines']:
            if line['type'] == 'narration':
                # 旁白前先隱藏角色
                if shown_character:
                    lines.append(f"hide character {shown_character}")
                    shown_character = None
                lines.append(line['text'])
                
            elif line['type'] == 'dialogue':
                char_id = line['character']
                expr = line.get('expression', 'normal')
                
                # 切換角色
                if shown_character != char_id:
                    if shown_character:
                        lines.append(f"hide character {shown_character}")
                    lines.append(f"show character {char_id} {expr} at center with fadeIn")
                    shown_character = char_id
                
                # 對話
                lines.append(f"{char_id} {line['text']}")
                
            elif line['type'] == 'action':
                if line['action'] == 'hide_character':
                    lines.append(f"hide character {line['character']}")
                    if shown_character == line['character']:
                        shown_character = None
        
        # 處理選項
        if passage.get('choices'):
            if shown_character:
                lines.append(f"hide character {shown_character}")
            
            choice_obj = {'Choice': {}}
            for i, choice in enumerate(passage['choices']):
                choice_obj['Choice'][f'Option{i+1}'] = {
                    'Text': choice['text'],
                    'Do': f"jump {choice['target']}"
                }
            lines.append(choice_obj)
        
        script[passage['name']] = lines
    
    # 輸出 JavaScript
    return f"'use strict';\nmonogatari.script({json.dumps(script, ensure_ascii=False, indent=2)});"
```

輸出範例：
```javascript
'use strict';
monogatari.script({
  "Start": [
    "show scene home_living_room with fadeIn",
    "和也從小就知道，自己的家庭和別人不一樣。",
    "他的母親是個愛發牢騷的女人。",
    "show character aiba gentle at center with fadeIn",
    "aiba 和也，吃飯了。",
    "hide character aiba",
    "show character kazuya normal at center with fadeIn",
    "kazuya 來了！",
    "hide character kazuya",
    {"Choice": {"Option1": {"Text": "繼續", "Do": "jump 童年回憶"}}}
  ],
  "童年回憶": [
    "show scene home_living_room with fadeIn",
    "那是和也十歲的時候...",
    {"Choice": {
      "Option1": {"Text": "悄悄離開", "Do": "jump 逃避真相"},
      "Option2": {"Text": "繼續聽", "Do": "jump 面對真相"}
    }}
  ]
});
```

### Step 5: 複製素材與引擎

```python
def copy_assets_and_engine(assets_path: str, output_path: str, template_path: str):
    """
    複製素材和 Monogatari 引擎到輸出目錄
    """
    # 複製角色圖片
    shutil.copytree(
        f"{assets_path}/characters",
        f"{output_path}/assets/characters"
    )
    
    # 複製場景圖片
    shutil.copytree(
        f"{assets_path}/scenes",
        f"{output_path}/assets/scenes"
    )
    
    # 複製 Monogatari 引擎
    shutil.copytree(
        f"{template_path}/dist",
        f"{output_path}/dist"
    )
```

### Step 6: 生成 HTML 入口

```python
def generate_index_html(title: str) -> str:
    """生成遊戲入口 HTML"""
    return f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
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
        </visual-novel>
    </div>
    
    <script src="dist/engine/core/monogatari.js"></script>
    <script src="js/options.js"></script>
    <script src="js/characters.js"></script>
    <script src="js/scenes.js"></script>
    <script src="js/script.js"></script>
    <script src="js/main.js"></script>
</body>
</html>'''
```

---

## 🖥️ CLI 介面

```bash
# 基本用法
python game-assembler/main.py processed.json --assets assets/

# 指定輸出目錄
python game-assembler/main.py processed.json --assets assets/ -o output/my_game

# 指定遊戲標題
python game-assembler/main.py processed.json --assets assets/ --title "我的視覺小說"

# 打包成單一 HTML（嵌入所有資源）
python game-assembler/main.py processed.json --assets assets/ --bundle
```

---

## 📋 設定選項

```json
{
  "game_assembler": {
    "engine_template": "templates/monogatari",
    "default_text_speed": 30,
    "auto_save_interval": 10000,
    "enable_gallery": false,
    "custom_css": "style/custom.css"
  }
}
```

---

## ⚠️ 注意事項

1. **素材驗證**：組裝前會檢查所有需要的素材是否存在
2. **編碼問題**：所有輸出檔案使用 UTF-8 編碼
3. **路徑處理**：Windows/Mac/Linux 路徑相容處理
4. **引擎版本**：使用 Monogatari v2.0+ 版本
