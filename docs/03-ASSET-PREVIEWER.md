# asset-previewer 規格書

## 📋 功能概述

為角色和場景生成預覽圖，提供網頁介面讓使用者挑選，確定後生成正式素材。

---

## 📥 輸入

| 項目 | 格式 | 說明 |
|------|------|------|
| assets-needed.json | .json | twee-processor 輸出的素材清單 |
| processed.json | .json | (可選) 完整故事資料，用於參考上下文 |

---

## 📤 輸出

### 1. preview/ 資料夾

預覽用的候選圖片：

```
preview/
├── characters/
│   ├── kazuya/
│   │   ├── concept_1.png
│   │   ├── concept_2.png
│   │   ├── concept_3.png
│   │   └── concept_4.png
│   └── aiba/
│       ├── concept_1.png
│       ├── concept_2.png
│       └── ...
└── scenes/
    ├── home_living_room/
    │   ├── concept_1.jpg
    │   ├── concept_2.jpg
    │   └── ...
    └── repair_shop/
        └── ...
```

### 2. preview.html

互動式預覽網頁（詳見下方）

### 3. selections.json

使用者選擇結果：

```json
{
  "selected_at": "2026-02-19T22:00:00Z",
  
  "characters": {
    "kazuya": {
      "selected_concept": "concept_2",
      "notes": "第二張比較符合年輕工程師的感覺"
    },
    "aiba": {
      "selected_concept": "concept_1",
      "notes": ""
    }
  },
  
  "scenes": {
    "home_living_room": {
      "selected_concept": "concept_3",
      "notes": "光線感覺比較自然"
    },
    "repair_shop": {
      "selected_concept": "concept_1",
      "notes": ""
    }
  }
}
```

### 4. assets/ 資料夾

最終生成的正式素材：

```
assets/
├── characters/
│   ├── kazuya/
│   │   ├── normal.png
│   │   ├── sad.png
│   │   ├── surprised.png
│   │   └── ...
│   └── aiba/
│       └── ...
└── scenes/
    ├── home_living_room.jpg
    └── repair_shop.jpg
```

---

## 🌐 預覽網頁 (preview.html)

### 功能需求

1. **顯示所有角色候選圖**
   - 每個角色顯示 N 張概念圖
   - 可點擊放大檢視
   - 單選（只能選一張）

2. **顯示所有場景候選圖**
   - 每個場景顯示 N 張候選
   - 可點擊放大
   - 單選

3. **備註欄位**
   - 每個選項可填寫備註
   - 方便記錄選擇原因

4. **確認按鈕**
   - 點擊後輸出 selections.json
   - 提示未選擇的項目

### 網頁設計

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>素材預覽 - Visual Novel Toolkit</title>
    <style>
        /* 樣式 */
        .character-section, .scene-section {
            margin: 20px 0;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
        }
        
        .concept-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
        }
        
        .concept-item {
            border: 3px solid transparent;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .concept-item.selected {
            border-color: #4CAF50;
            box-shadow: 0 0 10px rgba(76, 175, 80, 0.5);
        }
        
        .concept-item img {
            width: 100%;
            border-radius: 5px;
        }
        
        .confirm-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 15px 30px;
            font-size: 18px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>🎨 素材預覽</h1>
    
    <h2>👤 角色</h2>
    <div id="characters-container">
        <!-- 動態生成 -->
    </div>
    
    <h2>🖼️ 場景</h2>
    <div id="scenes-container">
        <!-- 動態生成 -->
    </div>
    
    <button class="confirm-btn" onclick="saveSelections()">
        ✓ 確認選擇
    </button>
    
    <script>
        // 載入素材資料
        const assetsData = /* 從 JSON 載入 */;
        
        // 渲染角色選項
        function renderCharacters() { /* ... */ }
        
        // 渲染場景選項
        function renderScenes() { /* ... */ }
        
        // 儲存選擇
        function saveSelections() {
            const selections = collectSelections();
            
            // 下載 JSON
            const blob = new Blob([JSON.stringify(selections, null, 2)], 
                                  {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'selections.json';
            a.click();
        }
    </script>
</body>
</html>
```

---

## ⚙️ 處理邏輯

### Step 1: 生成角色概念圖

```python
def generate_character_concepts(character: dict, count: int = 4) -> list:
    """
    為角色生成多張概念圖供挑選
    
    使用不同的 seed 或略微不同的 prompt 產生變化
    """
    concepts = []
    
    base_prompt = f"""
    視覺小說角色立繪，{character['name']}，
    {character['description']}，
    正面半身像，透明背景，動漫風格
    """
    
    for i in range(count):
        # 每張用不同 seed
        image = generate_image(
            prompt=base_prompt,
            seed=random.randint(0, 999999)
        )
        concepts.append(image)
    
    return concepts
```

### Step 2: 生成場景概念圖

```python
def generate_scene_concepts(scene: dict, count: int = 3) -> list:
    """
    為場景生成多張候選圖
    """
    concepts = []
    
    base_prompt = f"""
    視覺小說背景，{scene['name']}，
    {scene['description']}，
    {scene.get('time_of_day', '日間')}，
    {scene.get('mood', '')}氛圍，
    動漫風格，高品質背景
    """
    
    for i in range(count):
        image = generate_image(
            prompt=base_prompt,
            seed=random.randint(0, 999999)
        )
        concepts.append(image)
    
    return concepts
```

### Step 3: 啟動預覽伺服器

```python
def start_preview_server(preview_dir: str, port: int = 8080):
    """
    啟動本地 HTTP 伺服器供預覽
    """
    import http.server
    import webbrowser
    
    os.chdir(preview_dir)
    
    handler = http.server.SimpleHTTPRequestHandler
    server = http.server.HTTPServer(('localhost', port), handler)
    
    print(f"預覽網頁已開啟: http://localhost:{port}/preview.html")
    webbrowser.open(f"http://localhost:{port}/preview.html")
    
    server.serve_forever()
```

### Step 4: 根據選擇生成正式素材

```python
def generate_final_assets(selections: dict, assets_needed: dict):
    """
    根據使用者選擇的概念圖，生成所有正式素材
    """
    for char_id, selection in selections['characters'].items():
        # 取得選中的概念圖作為參考
        reference = load_concept_image(char_id, selection['selected_concept'])
        
        # 生成所有表情
        for expression in assets_needed[char_id]['expressions_needed']:
            generate_expression(
                character=char_id,
                expression=expression,
                reference=reference,  # 使用參考圖確保一致性
                output_path=f"assets/characters/{char_id}/{expression}.png"
            )
    
    for scene_id, selection in selections['scenes'].items():
        # 直接使用選中的概念圖作為正式場景
        copy_as_final(
            source=f"preview/scenes/{scene_id}/{selection['selected_concept']}.jpg",
            dest=f"assets/scenes/{scene_id}.jpg"
        )
```

---

## 🖥️ CLI 介面

```bash
# 生成預覽（不啟動伺服器）
python asset-previewer/main.py assets-needed.json --generate-only

# 生成預覽並開啟網頁
python asset-previewer/main.py assets-needed.json --preview

# 指定每個項目生成幾張候選
python asset-previewer/main.py assets-needed.json --concepts 5

# 讀取選擇結果，生成正式素材
python asset-previewer/main.py assets-needed.json --apply selections.json

# 完整流程（生成預覽 → 等待選擇 → 生成正式素材）
python asset-previewer/main.py assets-needed.json --interactive
```

---

## 📋 設定選項

```json
{
  "asset_previewer": {
    "character_concepts_count": 4,
    "scene_concepts_count": 3,
    "preview_port": 8080,
    "auto_open_browser": true,
    "image_provider": "stable_diffusion",
    "visual_style": "anime"
  }
}
```

---

## ⚠️ 注意事項

1. **一致性**：使用選中的概念圖作為參考，確保同一角色的不同表情風格一致
2. **預覽品質**：預覽圖可用較低品質加快生成，正式圖再用高品質
3. **網頁相容**：preview.html 需支援主流瀏覽器（Chrome, Firefox, Edge）
