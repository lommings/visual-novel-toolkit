# Monogatari Builder 使用指南

本文件詳細說明如何使用 `monogatari_builder.py` 生成視覺小說遊戲，以及如何自訂遊戲外觀。

---

## 目錄

1. [快速開始](#快速開始)
2. [輸入檔案說明](#輸入檔案說明)
3. [生成遊戲指令](#生成遊戲指令)
4. [啟動遊戲伺服器](#啟動遊戲伺服器)
5. [自訂遊戲外觀](#自訂遊戲外觀)
6. [角色與對話設定](#角色與對話設定)
7. [場景切換機制](#場景切換機制)
8. [結局標註](#結局標註)
9. [常見問題排解](#常見問題排解)
10. [檔案修改參考](#檔案修改參考)

---

## 快速開始

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

---

## 輸入檔案說明

| 檔案 | 說明 | 必要性 |
|------|------|--------|
| `story.twee` | Twee 格式的故事文字檔，包含所有段落和對話 | 必要 |
| `assets/` | 素材資料夾，含 `characters/` 和 `scenes/` 子目錄 | 必要 |
| `scene-mapping.json` | 場景代碼對應表，將段落名對應到場景 ID | 必要 |
| `assets-needed.json` | 角色和場景的定義檔（名稱、表情等） | 必要 |

### 素材資料夾結構

```
assets/
├── characters/
│   ├── kazuya/           # 角色 ID
│   │   ├── normal.png    # 表情
│   │   ├── happy.png
│   │   ├── sad.png
│   │   ├── angry.png
│   │   └── surprised.png
│   └── aiba/
│       └── ...
└── scenes/
    ├── secluded_alleyway/      # 場景 ID
    │   └── background.png
    ├── aiba_apartment_interior/
    │   └── background.png
    └── ...
```

---

## 生成遊戲指令

### 完整指令

```bash
python game-assembler/monogatari_builder.py \
    --twee "story.twee" \
    --assets "assets/" \
    --scene-mapping "scene-mapping.json" \
    --assets-json "assets-needed.json" \
    -o "output/game/" \
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

### 輸出結構

```
monogatari-game/
├── index.html          # 遊戲入口
├── js/
│   ├── options.js      # 遊戲設定
│   ├── storage.js      # 存檔設定
│   ├── script.js       # 遊戲腳本（角色、場景、對話）
│   └── main.js         # 初始化
├── style/
│   └── main.css        # 自訂樣式
├── assets/
│   ├── characters/     # 角色立繪
│   └── scenes/         # 場景背景
└── engine/
    └── core/           # Monogatari 引擎
```

---

## 啟動遊戲伺服器

```bash
cd "output/專案名/monogatari-game"
python -m http.server 8888
```

然後開啟瀏覽器到 `http://localhost:8888`

---

## 自訂遊戲外觀

所有外觀調整都在 `monogatari-game/style/main.css`

### 角色立繪位置與大小

```css
[data-character] {
    max-height: 85vh !important;    /* 角色最大高度 */
    max-width: 40vw !important;     /* 角色最大寬度 */
    bottom: 5vh !important;         /* 距離底部距離（調整此值控制與對話框的距離） */
    z-index: 100 !important;        /* 確保角色在對話框之上 */
}
```

**調整 `bottom` 值：**
- `bottom: 0` - 角色腳底貼齊螢幕底部
- `bottom: 5vh` - 角色稍微往上，緊貼對話框
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

## 角色與對話設定

### Monogatari 對話格式

```javascript
// script.js 中的格式

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
```

### 角色 ID 對應

在 `script.js` 開頭的 `monogatari.characters()` 定義：

```javascript
monogatari.characters({
    'kazuya': {
        name: '和也',           // 顯示名稱
        color: '#8b5cf6',       // 名稱顏色
        directory: 'kazuya',    // 素材資料夾名
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
        sprites: { ... }
    }
});
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

## 場景切換機制

### Twee 檔案中的場景標記

```twee
:: S01
{/* scene: S01 */}
在黑暗的城市底下，有一個名為「幽影」的秘密組織...

:: S02
{/* scene: S02 */}
相葉把和也帶回自己的公寓...
```

### 場景對應表 (scene-mapping.json)

```json
{
  "S01": "secluded_alleyway",
  "S02": "aiba_apartment_interior",
  "S03": "organization_interrogation_room"
}
```

### 對應表來源

1. **手動編寫** - 自己定義每個段落使用哪個背景
2. **AI 分析** - 使用 `twee_analyzer.py` 自動分析故事內容並生成對應

---

## 結局標註

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

## 常見問題排解

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

## 檔案修改參考

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

## 相關元件 AI 使用情況

| 元件 | 用途 | 是否使用 AI |
|------|------|------------|
| `monogatari_builder.py` | 組裝遊戲 | ❌ 否 |
| `twee_analyzer.py` | 分析場景對應 | ✅ 是 |
| `script_processor.py` | 處理角色顯示 | ❌ 否（規則判斷） |
| 角色/場景圖片生成 | 產生素材 | ✅ 是 |

**如果已有完整素材和對應表，可完全不依賴 AI 生成遊戲。**

---

## 版本紀錄

- **2026-02-20** - 修正 Monogatari JS 初始化格式，修正角色 z-index 問題，新增結局標註功能
