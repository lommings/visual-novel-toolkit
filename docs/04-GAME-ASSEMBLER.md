# game-assembler 規格書

## 📋 功能概述

將處理好的文字資料與選好的圖片素材組合，輸出完整可遊玩的 Monogatari 視覺小說遊戲。

---

## 🚀 快速開始

```bash
cd C:\Users\lommi\Projects\visual-novel-toolkit

python game-assembler/monogatari_builder.py \
    --twee "output/專案名/story.twee" \
    --assets "output/專案名/story/assets" \
    --scene-mapping "output/專案名/game/scene-mapping.json" \
    --assets-json "output/專案名/story/assets-needed.json" \
    -o "output/專案名/monogatari-game" \
    --title "遊戲標題" \
    --no-rembg
```

### 參數說明

| 參數 | 說明 |
|------|------|
| `--twee` | Twee 故事檔案路徑 |
| `--assets` | 素材資料夾路徑 |
| `--scene-mapping` | 場景對應 JSON 檔案路徑 |
| `--assets-json` | 角色/場景定義 JSON 檔案路徑 |
| `-o`, `--output` | 輸出目錄 |
| `--title` | 遊戲標題 |
| `--no-rembg` | 跳過角色立繪去背處理（加快速度） |

---

## 📥 輸入

| 項目 | 格式 | 說明 |
|------|------|------|
| story.twee | .twee | Twee 格式的故事文字檔 |
| assets/ | 資料夾 | 素材資料夾（含 characters/ 和 scenes/） |
| scene-mapping.json | .json | 場景代碼對應表 |
| assets-needed.json | .json | 角色和場景定義 |

### 輸入結構

```
input/
├── story.twee          # 故事資料（Twee 格式）
├── scene-mapping.json  # 場景代碼對應
├── assets-needed.json  # 角色/場景定義
└── assets/
    ├── characters/
    │   ├── kazuya/
    │   │   ├── normal.png
    │   │   ├── sad.png
    │   │   ├── happy.png
    │   │   ├── angry.png
    │   │   └── surprised.png
    │   └── aiba/
    │       └── ...
    └── scenes/
        ├── secluded_alleyway/
        │   └── background.png
        └── aiba_apartment_interior/
            └── background.png
```

---

## 📤 輸出

完整的 Monogatari 遊戲：

```
monogatari-game/
├── index.html              # 遊戲入口
├── js/
│   ├── script.js           # 遊戲腳本（角色、場景、對話）
│   ├── options.js          # 遊戲設定
│   ├── storage.js          # 存檔設定
│   └── main.js             # 初始化
├── style/
│   └── main.css            # 自訂樣式
├── assets/
│   ├── characters/         # 角色立繪
│   └── scenes/             # 場景背景
└── engine/
    └── core/               # Monogatari 引擎
        ├── monogatari.js
        └── monogatari.css
```

---

## 🖥️ 啟動遊戲伺服器

```bash
cd "output/專案名/monogatari-game"
python -m http.server 8888
```

然後開啟瀏覽器到 `http://localhost:8888`

---

## 🎨 自訂遊戲外觀

所有外觀調整都在 `monogatari-game/style/main.css`

### 角色立繪位置與大小

```css
[data-character] {
    max-height: 85vh !important;    /* 角色最大高度 */
    max-width: 40vw !important;     /* 角色最大寬度 */
    bottom: 5vh !important;         /* 距離底部距離 */
    z-index: 100 !important;        /* 確保角色在對話框之上 */
}
```

**調整 `bottom` 值：**
- `bottom: 0` - 角色腳底貼齊螢幕底部
- `bottom: 5vh` - 角色緊貼對話框上方（推薦）
- `bottom: 20vh` - 角色距離對話框較遠

### 角色位置（左/右/中）

```css
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
```

### 對話框樣式

```css
text-box,
[data-component="text-box"] {
    z-index: 50 !important;         /* 低於角色 z-index */
    background: rgba(0, 0, 0, 0.85) !important;  /* 背景透明度 */
}
```

### 主選單背景圖

```css
[data-screen="main"] {
    background-image: url('../assets/你的圖片.png') !important;
    background-size: cover !important;
    background-position: center !important;
}
```

---

## 💬 Monogatari 對話格式

### script.js 中的格式

```javascript
// 角色說話（會顯示角色名稱）
'aiba 你還好嗎？'
'kazuya 我沒事。'

// 純敘述（不顯示角色名稱）
'夜色低垂，街燈閃爍著微弱的光芒。'

// 顯示角色
'show character kazuya normal at left with fadeIn'
'show character aiba happy at right with fadeIn'

// 隱藏角色
'hide character kazuya'

// 切換場景
'show scene secluded_alleyway with fadeIn'

// 結局畫面
'centered ── 結局：破鏈重生 ──'
'end'
```

### 讓角色說話的原文格式

程式會自動偵測以下格式並轉換：

```
相葉：你還好嗎？
```
↓ 自動轉換為
```javascript
'show character aiba normal at center with fadeIn',
'aiba 你還好嗎？'
```

**注意：** 如果原文是「焦急地詢問：『你還好嗎？』」這種格式，程式無法自動偵測，需要手動修改 `script.js`。

---

## 📋 檔案修改參考

### 直接修改生成的遊戲（不需重新生成）

| 要修改的內容 | 檔案位置 |
|-------------|---------|
| 人物出場、對話、場景切換 | `monogatari-game/js/script.js` |
| 角色定義（名字、顏色） | `monogatari-game/js/script.js` 開頭 |
| 遊戲設定（標題、速度） | `monogatari-game/js/options.js` |
| 畫面樣式（大小、位置、背景） | `monogatari-game/style/main.css` |
| 角色立繪圖片 | `monogatari-game/assets/characters/` |
| 場景背景圖片 | `monogatari-game/assets/scenes/` |

### 修改原始檔再重新生成

| 要修改的內容 | 檔案位置 |
|-------------|---------|
| 故事內容、對話 | `story.twee` |
| 場景對應 | `scene-mapping.json` |
| 角色偵測規則 | `shared/script_processor.py` |
| 遊戲生成模板 | `game-assembler/monogatari_builder.py` |

---

## ⚙️ 主要程式說明

### monogatari_builder.py

主要建構器，負責：
- 建立目錄結構
- 複製素材（含去背處理）
- 生成 JS 檔案（options.js, storage.js, script.js, main.js）
- 生成 index.html
- 生成 main.css
- 複製 Monogatari 引擎

### 重要函式

```python
class MonogatariBuilder:
    def build(self, story_data, assets_dir, title, remove_bg=True):
        """組裝完整遊戲"""
        self._create_directories()
        self._copy_assets(assets_dir, remove_bg)
        processed_script = self._process_script(story_data)
        self._generate_characters_js(story_data)
        self._generate_scenes_js(story_data)
        self._generate_script_js(processed_script, story_data)
        self._generate_options_js(title)
        self._generate_storage_js()
        self._generate_main_js()
        self._generate_index_html(title)
        self._generate_main_css()
        self._setup_engine()
```

### 生成的 JS 格式

**options.js** - 必須使用正確的 Monogatari 初始化：
```javascript
'use strict';
/* global Monogatari */

const { Monogatari: monogatari } = Monogatari;

monogatari.settings({
    "Name": "遊戲標題",
    "Version": "1.0.0",
    "Label": "Start",
    // ...
});
```

**main.js** - 使用 $_ready 等待 DOM：
```javascript
'use strict';
/* global Monogatari */
/* global monogatari */

const { $_ready } = Monogatari;

$_ready(() => {
    monogatari.init('#monogatari');
});
```

---

## 🏷️ 結局標註

結局段落會自動加上標題通知。

### 自動偵測規則

段落名稱以 `Ending_` 開頭會被視為結局：
- `Ending_BreakChains` → 顯示「── 結局：破鏈重生 ──」
- `Ending_LostShadow` → 顯示「── 結局：消失的幽影 ──」
- `Ending_SilentEnd` → 顯示「── 結局：無聲的終結 ──」

### 自訂結局名稱

編輯 `shared/script_processor.py` 中的 `_get_ending_title` 方法：

```python
ending_titles = {
    'Ending_BreakChains': '破鏈重生',
    'Ending_LostShadow': '消失的幽影',
    'Ending_SilentEnd': '無聲的終結',
    # 新增自訂結局...
    'Ending_NewEnding': '新結局名稱',
}
```

---

## ❓ 常見問題排解

### 遊戲卡住不動

**可能原因：** JavaScript 錯誤

**解決方法：**
1. 按 F12 開啟開發者工具
2. 查看 Console 頁籤的錯誤訊息
3. 常見錯誤：
   - `monogatari is not defined` → options.js 格式錯誤
   - `Cannot read properties of undefined` → 角色或場景 ID 不存在

### 角色被對話框蓋住

**解決方法：** 調整 CSS z-index

```css
[data-character] {
    z-index: 100 !important;  /* 角色層級要高於對話框 */
}

text-box {
    z-index: 50 !important;   /* 對話框層級較低 */
}
```

### 角色和對話框距離太遠

**解決方法：** 調整 CSS bottom 值

```css
[data-character] {
    bottom: 5vh !important;   /* 數值越小，角色越靠近底部 */
}
```

### 主選單沒有背景圖

**解決方法：** 在 main.css 加入

```css
[data-screen="main"] {
    background-image: url('../assets/your-image.png') !important;
    background-size: cover !important;
}
```

---

## 📊 AI 使用情況

| 元件 | 用途 | 是否使用 AI |
|------|------|------------|
| `monogatari_builder.py` | 組裝遊戲 | ❌ 否 |
| `twee_analyzer.py` | 分析場景對應 | ✅ 是 |
| `script_processor.py` | 處理角色顯示 | ❌ 否（規則判斷） |
| 角色/場景圖片生成 | 產生素材 | ✅ 是 |

**如果已有完整素材和對應表，可完全不依賴 AI 生成遊戲。**

---

## 📝 版本紀錄

- **2026-02-20** - 修正 Monogatari JS 初始化格式，修正角色 z-index 問題，新增結局標註功能
