# Visual Novel Toolkit - 完整工作流程

**版本**：2.0 (2026-02-21)  
**專案路徑**：`C:\Users\lommi\Projects\visual-novel-toolkit`

---

## 📋 **完整流程概覽**

```
1. 小說轉 Twee
2. 處理 Twee（生成素材需求）
3. 啟動素材編輯器（生成 prompts）
4. 手動生成圖片（Gemini / SD）
5. 手動剪裁調整構圖 ✂️
6. 標準化角色尺寸 📏
7. 組裝遊戲 🎮
8. 測試遊戲
```

---

## 🚀 **步驟 1：小說轉 Twee**

### 指令

```bash
cd C:\Users\lommi\Projects\visual-novel-toolkit

python novel-to-twee/main.py "C:\Users\lommi\Documents\創作相關\故事資料夾\故事檔名.txt" -o output/
```

### 輸出

- `output/故事名稱/story.twee`
- `output/故事名稱/analysis.json`

---

## 🔧 **步驟 2：處理 Twee**

### 指令

```bash
python twee-processor/main.py "output/故事名稱/story.twee"
```

### 輸出

- `output/故事名稱/story/processed.json`
- `output/故事名稱/story/assets-needed.json`

---

## 🎨 **步驟 3：啟動素材編輯器**

### 清除舊 session（重要！）

```bash
del output\*\*\session.json /s 2>nul
del output\*\*\*\session.json /s 2>nul
```

### 啟動編輯器

```bash
python asset-previewer/prompt_server.py "output/故事名稱/story/assets-needed.json"
```

### 瀏覽器

打開 http://localhost:8080/

**記得按 Ctrl+F5 強制刷新！**

### 💡 提示

編輯器會生成 prompts，但**建議手動用 Gemini 網頁版生圖**（便宜且品質好）

---

## 🖼️ **步驟 4：手動生成圖片**

### 推薦尺寸

#### 角色立繪
- **尺寸**：自由（建議 512x768 或更高）
- **格式**：PNG，透明背景
- **表情**：
  - `normal.png` （必須）
  - `happy.png`
  - `sad.png`
  - `angry.png`
  - `surprised.png`

#### 場景背景
- **尺寸**：1024 x 576
- **格式**：PNG 或 JPG

### 檔案位置

生成的圖片放到：

```
output/故事名稱/story/assets/
├── characters/
│   ├── 角色ID/
│   │   └── normal.png
│   └── ...
└── scenes/
    ├── 場景ID/
    │   └── background.png
    └── ...
```

---

## ✂️ **步驟 5：手動剪裁調整**

### 為什麼需要？

AI 生成的圖片經常有：
- ❌ 人物比例不一致
- ❌ 構圖不統一（有的全身、有的半身）
- ❌ 留白過多或不足

### 操作步驟

用圖片編輯器（Photoshop / GIMP / Paint.NET）打開每個角色的 `normal.png`：

1. **統一構圖風格**：
   - 決定是要**半身像**（頭到胸/腰）還是**全身像**
   - 所有角色採用相同構圖

2. **剪裁調整**：
   - 去除多餘空白
   - 讓人物居中
   - 確保頭部在畫面中的比例相近（如：頭部佔 25-30%）

3. **保存覆蓋原檔案**

---

## 📏 **步驟 6：標準化角色尺寸**

### 為什麼需要？

手動剪裁後，圖片尺寸可能不一致，需要統一高度確保遊戲中人物大小一致。

### 預覽效果

```bash
python tools/standardize_characters.py \
    "output/故事名稱/story/assets/characters" \
    --preview \
    --height 1200
```

### 執行標準化

確認預覽效果無誤後：

```bash
python tools/standardize_characters.py \
    "output/故事名稱/story/assets/characters" \
    --height 1200
```

### 推薦高度

| 立繪類型 | 建議高度 |
|----------|----------|
| 半身像 | 1200px |
| 全身像 | 1800px |

---

## 🎮 **步驟 7：組裝遊戲**

### 指令

```bash
python game-assembler/monogatari_builder.py \
    --twee "output/故事名稱/story.twee" \
    --assets "output/故事名稱/story/assets" \
    --assets-json "output/故事名稱/story/assets-needed.json" \
    --scene-mapping "output/故事名稱/scene-mapping.json" \
    -o "output/故事名稱/game" \
    --no-rembg
```

### 輸出

`output/故事名稱/game/` - 完整的遊戲資料夾

### ⚠️ 重要提醒

**組裝遊戲會覆蓋 `game/` 資料夾中的所有手動修改！**

包括：
- CSS 設定（角色大小、主選單背景等）
- JavaScript 修改
- 所有自定義設定

**建議**：組裝後再做手動調整，或使用 Git 版本控制。

---

## 🧪 **步驟 8：測試遊戲**

### 啟動本地伺服器

```bash
cd output/故事名稱/game
python -m http.server 8080
```

### 瀏覽器

打開 http://localhost:8080/

---

## 🛠️ **後期調整（可選）**

遊戲組裝後，如需細部調整：

### 調整位置

`output/故事名稱/game/`

### 可調整的檔案

| 要調整的內容 | 檔案位置 |
|--------------|----------|
| 角色大小、位置 | `style/main.css` |
| 主選單背景 | `style/main.css` |
| 人物出場、對話 | `js/script.js` |
| 角色定義 | `js/characters.js` |
| 場景定義 | `js/scenes.js` |
| 遊戲設定 | `js/options.js` |
| 角色圖片 | `assets/characters/` |
| 場景圖片 | `assets/scenes/` |

### ⚠️ 注意

手動修改後，**不要重新執行步驟 7（組裝遊戲）**，否則會覆蓋所有修改！

---

## 📦 **懶人一鍵版**

### 步驟 1-3 一鍵執行

```bash
taskkill /F /IM python.exe 2>nul; cd C:\Users\lommi\Projects\visual-novel-toolkit; python novel-to-twee/main.py "C:\Users\lommi\Documents\創作相關\故事資料夾\故事檔名.txt" -o output/; python twee-processor/main.py "output/故事名稱/story.twee"; del output\*\*\session.json /s 2>nul; python asset-previewer/prompt_server.py "output/故事名稱/story/assets-needed.json"
```

**提醒**：記得替換 `故事資料夾` 和 `故事檔名` 和 `故事名稱`！

---

## 🌐 **發布遊戲**

### 方法 1：GitHub Pages（推薦）

```bash
cd output/故事名稱/game

git init
git add -A
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的帳號/遊戲名稱.git
git push -u origin main
```

**設定 GitHub Pages**：
1. Repo → Settings → Pages
2. Source 選 `main branch`
3. 資料夾選 `/` (root)
4. Save

**遊戲網址**：`https://你的帳號.github.io/遊戲名稱/`

### 方法 2：Netlify（拖拉上傳）

1. 到 https://app.netlify.com/drop
2. 把 `game` 資料夾拖進去
3. 自動部署完成

### 方法 3：itch.io（遊戲平台）

1. 註冊 https://itch.io/
2. Dashboard → Create new project
3. 上傳 ZIP（把 `game` 壓縮）
4. Kind of project 選 `HTML`
5. 勾選 `This file will be played in the browser`

### 方法 4：Vercel（自動部署，推薦）** ⭐

**特色**：連接 GitHub 自動部署，推送更新即自動更新網站。

#### **前置準備：將遊戲放到 docs/games/**

⚠️ **重要**：`output/` 資料夾在 `.gitignore` 中，不會推送到 GitHub！

需要將遊戲複製到 `docs/games/` 資料夾：

```bash
cd C:\Users\lommi\Projects\visual-novel-toolkit

# 創建遊戲資料夾
mkdir docs\games\遊戲名稱

# 複製遊戲檔案
xcopy "output\專案資料夾\game\*" "docs\games\遊戲名稱\" /E /I

# 推送到 GitHub
git add docs/games/遊戲名稱
git commit -m "新增遊戲：遊戲名稱"
git push
```

#### **首次設定**

1. **登入 Vercel**
   - 到 https://vercel.com/
   - 用 GitHub 帳號登入

2. **Import Project**
   - 點擊 **Add New... → Project**
   - 選擇 **Import Git Repository**
   - 選擇 `visual-novel-toolkit` repo

3. **設定專案**
   - **Framework Preset**: Other
   - **Root Directory**: `docs` ⭐ 重要！
   - **Build Command**: 留空
   - **Output Directory**: 留空
   - **Install Command**: 留空
   - 點擊 **Deploy**

4. **完成！**
   - 部署完成後會顯示網址
   - 預設：`https://visual-novel-toolkit.vercel.app`

#### **遊戲網址結構**

| 網址 | 內容 |
|------|------|
| `https://visual-novel-toolkit.vercel.app/` | docs/ 根目錄 |
| `https://visual-novel-toolkit.vercel.app/games/` | 遊戲列表首頁 |
| `https://visual-novel-toolkit.vercel.app/games/小花與佳樹/` | 小花與佳樹遊戲 |

#### **更新遊戲**

**方法 A：修改後重新複製推送**

```bash
# 1. 修改遊戲（在 output/專案資料夾/game/）
# 2. 重新複製到 docs/games/
xcopy "output\專案資料夾\game\*" "docs\games\遊戲名稱\" /E /I /Y

# 3. 推送到 GitHub
git add docs/games/遊戲名稱
git commit -m "更新遊戲：修改劇情"
git push

# 4. Vercel 自動重新部署（約 1-2 分鐘）
```

**方法 B：直接修改 docs/games/ 中的檔案**

如果只是小修改（改對話、CSS），可以直接編輯 `docs/games/遊戲名稱/` 中的檔案：

```bash
# 1. 直接修改 docs/games/遊戲名稱/js/script.js
# 2. 推送
git add docs/games/遊戲名稱
git commit -m "修改對話"
git push

# 3. Vercel 自動部署
```

#### **創建遊戲列表首頁**

在 `docs/games/index.html` 創建作品集首頁（已提供範本）。

範本內容：
- 響應式卡片佈局
- 遊戲縮圖和簡介
- 一鍵開始遊戲按鈕
- 可自由添加多個遊戲

#### **Vercel 設定檢查**

如果部署後遊戲無法顯示：

1. **檢查 Root Directory**
   - Vercel Dashboard → 專案 → Settings → General
   - **Root Directory** 應為 `docs`
   - 如果不對，修改後重新部署

2. **強制重新部署**
   - Deployments → 最新部署 → 右上角 ⋯ → Redeploy

3. **檢查檔案路徑**
   - 確認遊戲在 `docs/games/遊戲名稱/index.html`
   - 網址應為 `https://你的專案.vercel.app/games/遊戲名稱/`

#### **優點與缺點**

**優點**：
- ✅ 自動部署（推送 GitHub 即更新）
- ✅ 免費
- ✅ CDN 加速
- ✅ HTTPS 自動配置
- ✅ 可自訂網域

**缺點**：
- ❌ 需要將遊戲從 `output/` 複製到 `docs/games/`
- ❌ 兩份檔案需要同步（開發版和發布版）

---

## 🔧 **常見問題**

### Q1：素材編輯器顯示舊資料？

**解決**：清除 session 快取

```bash
del output\*\*\session.json /s 2>nul
taskkill /F /IM python.exe
python asset-previewer/prompt_server.py "output/故事名稱/story/assets-needed.json"
```

瀏覽器按 **Ctrl+F5** 強制刷新

### Q2：遊戲中角色大小不一致？

**原因**：未執行步驟 6（標準化角色尺寸）

**解決**：

```bash
python tools/standardize_characters.py \
    "output/故事名稱/story/assets/characters" \
    --height 1200
```

### Q3：重新組裝遊戲後，手動修改消失了？

**原因**：`game-assembler` 會覆蓋所有手動修改

**解決方案**：
1. **不要重新組裝**，只更新圖片
2. **使用 Git**，組裝前先 commit
3. **記錄修改**，重新組裝後再手動調整

### Q4：只想更新圖片，不重新組裝？

**解決**：

```bash
# 標準化圖片
python tools/standardize_characters.py \
    "output/故事名稱/story/assets/characters" \
    --height 1200

# 複製到遊戲資料夾
xcopy "output\故事名稱\story\assets\characters" "output\故事名稱\game\assets\characters" /E /Y
```

### Q5：如何添加角色的不同表情？

遊戲組裝後，可以手動添加表情圖片並在對話中使用。

#### **步驟 1：準備表情圖片**

將表情圖片放到角色資料夾：

```
game/assets/characters/hanako/
├── normal.png      ← 普通表情（已有）
├── happy.png       ← 開心
├── sad.png         ← 悲傷
├── angry.png       ← 生氣
└── surprised.png   ← 驚訝
```

**建議**：
- 所有表情圖片**尺寸要一致**（例如都是 945 x 1200）
- 使用 PNG 格式，透明背景
- 可用標準化工具處理：

```bash
python tools/standardize_characters.py "game/assets/characters" --height 1200 --file happy.png
python tools/standardize_characters.py "game/assets/characters" --height 1200 --file sad.png
# ... 其他表情
```

#### **步驟 2：修改 script.js**

打開 `game/js/script.js`，找到要改的對話段落。

**範例：添加表情變化**

```javascript
'Route_Library': [
    'show scene old_library_corner with fadeIn',
    
    // 1. 傷心地進入圖書館
    'show character hanako sad at center with fadeIn',
    '花子選擇了逃跑，她一路穿過長廊，躲進了校園最偏僻的圖書館角落。',
    
    // 2. 驚訝地發現書在動
    'show character hanako surprised',
    '就在這時，她面前的一本書竟無風自鼓，頁面快速翻動。',
    
    // 3. 見到佳樹後恢復正常
    'show character hanako normal at left',
    'show character yoshiki normal at right with fadeIn',
    '他是佳樹，這座圖書館的幽靈。',
]
```

#### **Monogatari 表情指令格式**

| 情況 | 指令格式 | 範例 |
|------|----------|------|
| 顯示角色（首次出場） | `show character 角色ID 表情 at 位置 with fadeIn` | `show character hanako happy at center with fadeIn` |
| 切換表情（已在場上） | `show character 角色ID 表情` | `show character hanako sad` |

#### **可用的表情名稱**

根據你準備的圖片檔名：

| 圖片檔名 | 表情名稱 | 用法 |
|----------|----------|------|
| `normal.png` | `normal` | `show character hanako normal` |
| `happy.png` | `happy` | `show character hanako happy` |
| `sad.png` | `sad` | `show character hanako sad` |
| `angry.png` | `angry` | `show character hanako angry` |
| `surprised.png` | `surprised` | `show character hanako surprised` |

#### **步驟 3：保存並測試**

1. 保存 `script.js`
2. 瀏覽器按 **Ctrl+F5** 強制刷新
3. 測試對話，確認表情變化

#### **快速測試範例**

在 `Start` 段落添加測試代碼：

```javascript
'Start': [
    'show scene aoba_academy_gate with fadeIn',
    
    'show character hanako normal at center with fadeIn',
    '這是普通表情',
    
    'show character hanako happy',
    '這是開心表情',
    
    'show character hanako sad',
    '這是悲傷表情',
    
    'show character hanako angry',
    '這是生氣表情',
    
    'show character hanako surprised',
    '這是驚訝表情',
]
```

#### **注意事項**

- ⚠️ 表情圖片檔名必須對應指令中的表情名稱
- ⚠️ 所有表情圖片尺寸應一致，避免切換時大小突變
- ⚠️ 修改後記得強制刷新瀏覽器 (Ctrl+F5)

### Q6：如何修改故事路線和劇情？

有兩種方法，推薦使用方法 B 以保持原始檔案和最終遊戲同步。

#### **方法 A：直接修改 script.js（小修改）**

**位置**：`output/故事名稱/game/js/script.js`

**適用於**：
- 修改少量對話
- 調整選項文字
- 微調劇情

**優點**：
- ✅ 快速立即生效
- ✅ 不影響其他手動修改

**缺點**：
- ❌ 重新組裝會消失
- ❌ 原始檔案不同步

#### **方法 B：修改 Twee 重新組裝（推薦）** ⭐

適用於任何劇情修改，保持檔案同步。

##### **步驟 1：備份手動修改**

⚠️ **重要**：重新組裝會覆蓋所有手動修改！

備份這些檔案：

```bash
# 備份 CSS（如果有自定義修改）
copy "output\故事名稱\game\style\main.css" "output\故事名稱\main.css.backup"

# 備份主選單背景（如果有添加）
copy "output\故事名稱\game\assets\scenes\main-menu-bg.png" "output\故事名稱\main-menu-bg.backup.png"

# 或使用 Git
cd output/故事名稱/game
git add -A
git commit -m "重新組裝前備份"
```

##### **步驟 2：修改 Twee 檔案**

**位置**：`output/故事名稱/story.twee`

**Twee 格式範例**：

```twee
:: Start
{/* scene: S01 */}
東京的春天帶著一種喧囂的冷漠。花子拖著沉重的行李箱站在私立青葉學園的門口。

她握緊拳頭，對自己說：「我一定不能給爸爸媽媽添麻煩。」

[[躲進圖書館哭泣->Route_Library]]
[[試圖向老師告狀->Route_Teacher]]
[[在教室大聲質問是誰做的->Route_Confront]]

:: Route_Library
{/* scene: S02 */}
花子選擇了逃跑，她一路穿過長廊，躲進了校園最偏僻的圖書館角落。

這裡空氣中瀰漫著古舊書卷的氣息，讓她的恐懼稍微平復。

[[繼續->Meet_Yoshiki]]
```

**修改技巧**：

| 要修改的內容 | Twee 語法 |
|--------------|-----------|
| 對話內容 | 直接寫在段落中 |
| 場景切換 | `{/* scene: 場景代碼 */}` |
| 選項 | `[[選項文字->目標段落名稱]]` |
| 新增段落 | `:: 段落名稱` |
| 結局 | 段落名稱以 `Ending_` 開頭 |

##### **步驟 3：重新組裝遊戲**

```bash
cd C:\Users\lommi\Projects\visual-novel-toolkit

python game-assembler/monogatari_builder.py \
    --twee "output/故事名稱/story.twee" \
    --assets "output/故事名稱/story/assets" \
    --assets-json "output/故事名稱/story/assets-needed.json" \
    --scene-mapping "output/故事名稱/scene-mapping.json" \
    -o "output/故事名稱/game" \
    --no-rembg
```

##### **步驟 4：重新應用手動修改**

組裝後需要重新做這些調整：

**1. 恢復主選單背景**

如果有自定義主選單背景，在 `game/style/main.css` 最後添加：

```css
/* 主選單背景 */
[data-screen="main"],
#main-screen {
    background-image: url('../assets/scenes/main-menu-bg.png') !important;
    background-size: cover !important;
    background-position: center !important;
    background-repeat: no-repeat !important;
}
```

然後複製背景圖：

```bash
copy "output\故事名稱\main-menu-bg.backup.png" "output\故事名稱\game\assets\scenes\main-menu-bg.png"
```

**2. 恢復角色大小設定**

如果有自定義角色大小，修改 `game/style/main.css`：

```css
/* 半身立繪優化設定 - 適合三人同框 */
[data-character] {
    max-height: 65vh !important;
    max-width: 35vw !important;
    bottom: 18vh !important;
    object-fit: contain !important;
    z-index: 50 !important;
    pointer-events: none !important;
}

/* 佳樹（幽靈）單獨設定 */
[data-character="yoshiki"] {
    max-height: 70vh !important;
    max-width: 40vw !important;
}

/* 大樹（哥哥）單獨設定 */
[data-character="daiki"] {
    max-height: 70vh !important;
    max-width: 42vw !important;
}
```

**3. 檢查場景名稱**

如果之前有修正場景名稱（如 `SCENE_07_REVENGE_B` → `hostile_classroom`），檢查 `game/js/script.js` 是否需要重新修正。

##### **步驟 5：測試遊戲**

```bash
cd output/故事名稱/game
python -m http.server 8080
```

打開 http://localhost:8080/ 測試所有修改。

##### **最佳實踐**

**使用 Git 追蹤修改**：

```bash
# 初次組裝後
cd output/故事名稱/game
git init
git add -A
git commit -m "初次組裝"

# 手動調整後
git add -A
git commit -m "手動調整：主選單背景、角色大小"

# 修改 Twee 重新組裝後
# Git 會顯示差異，方便重新應用修改
git diff
```

**創建修改檢查表**：

在 `output/故事名稱/` 創建 `CUSTOMIZATIONS.md`：

```markdown
# 手動修改記錄

## CSS 修改
- [ ] 主選單背景
- [ ] 角色大小設定（花子 65vh、佳樹 70vh、大樹 70vh）

## 場景修正
- [ ] SCENE_07_REVENGE_B → hostile_classroom
- [ ] SCENE_08_DAIKI → library_strategy_room
- [ ] ...

## 其他
- [ ] 主選單背景圖 (main-menu-bg.png)
```

每次重新組裝後，對照檢查表重新應用修改。

##### **總結流程**

```
1. 備份手動修改 → Git commit 或複製檔案
2. 修改 story.twee → 編輯對話、選項、分支
3. 重新組裝遊戲 → 執行 monogatari_builder.py
4. 重新應用修改 → 對照檢查表逐一恢復
5. 測試遊戲 → 確認所有修改生效
```

---

## 📝 **工作流程檢查表**

新遊戲生成流程：

- [ ] 步驟 1：小說轉 Twee
- [ ] 步驟 2：處理 Twee
- [ ] 步驟 3：啟動素材編輯器
- [ ] 步驟 4：手動生成圖片
- [ ] 步驟 5：手動剪裁調整
- [ ] 步驟 6：標準化角色尺寸
- [ ] 步驟 7：組裝遊戲
- [ ] 步驟 8：測試遊戲
- [ ] （可選）後期調整
- [ ] （可選）發布遊戲

---

## 🎯 **重點提醒**

### ✅ 推薦做法

1. **版本控制**：用 Git 追蹤所有修改
2. **分批處理**：先處理主要角色，確認效果
3. **預覽確認**：標準化前先用 `--preview` 預覽
4. **測試驗證**：組裝後先測試再調整

### ❌ 避免做法

1. **不要跳過步驟 5 和 6**：直接組裝會導致角色大小不一致
2. **不要在有手動修改時重新組裝**：會覆蓋所有修改
3. **不要刪除 `preview/` 資料夾**：方便日後重新選擇

---

## 📚 **相關文檔**

- [00-OVERVIEW.md](./00-OVERVIEW.md) - 專案總覽
- [04-CHARACTER-STANDARDIZER.md](./04-CHARACTER-STANDARDIZER.md) - 角色標準化工具詳細說明
- [tools/README.md](../tools/README.md) - 工具使用說明

---

**最後更新**：2026-02-21  
**維護者**：Pearl
