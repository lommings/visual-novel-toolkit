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
