# Visual Novel Toolkit

小說轉視覺小說遊戲工具鏈 🎮

## ✨ 功能

將純文字小說轉換為可遊玩的 Monogatari 視覺小說遊戲：

- 📖 **小說轉 Twee** - AI 分析故事，自動生成分支
- ✂️ **段落處理** - 拆分長段落，識別對話和場景
- 🎨 **素材預覽** - 生成概念圖，網頁介面挑選
- 🎮 **遊戲組裝** - 組合文字與圖片，輸出完整遊戲

## 🔄 工作流程

```
小說.txt
    │
    ▼
┌─────────────────┐
│  novel-to-twee  │  AI 分析 + 生成分支
└────────┬────────┘
         ▼
    story.twee (可在 Twine 編輯)
         │
         ▼
┌─────────────────┐
│ twee-processor  │  分析角色場景 + 拆分段落
└────────┬────────┘
         ▼
┌─────────────────┐
│ asset-previewer │  預覽 → 挑選 → 生成素材
└────────┬────────┘
         ▼
┌─────────────────┐
│ game-assembler  │  組合 → 輸出遊戲
└────────┬────────┘
         ▼
    完整遊戲/
```

## 🚀 快速開始

### 安裝

```bash
cd visual-novel-toolkit
pip install -r requirements.txt
```

### 設定 API

編輯 `config.json`，填入 Gemini API 金鑰：

```json
{
  "ai": {
    "gemini": {
      "api_key": "your-api-key"
    }
  }
}
```

### 使用

```bash
# 1. 小說轉 Twee
python novel-to-twee/main.py 小說.txt -o output/

# 2. (可選) 用 Twine 編輯 output/小說/story.twee

# 3. 處理 Twee
python twee-processor/main.py output/小說/story.twee

# 4. 生成素材預覽
python asset-previewer/main.py output/小說/assets-needed.json --preview

# 5. (在網頁中選擇後) 生成正式素材
python asset-previewer/main.py output/小說/assets-needed.json --apply selections.json

# 6. 組裝遊戲
python game-assembler/main.py output/小說/processed.json

# 7. 遊玩
cd output/小說/game
python -m http.server 8080
```

## 📁 專案結構

```
visual-novel-toolkit/
├── shared/              # 共用模組
│   ├── ai_client.py     # AI API
│   ├── image_generator.py
│   └── models/          # 資料模型
├── novel-to-twee/       # 小說→Twee
├── twee-processor/      # Twee 處理
├── asset-previewer/     # 素材預覽
├── game-assembler/      # 遊戲組裝
├── docs/                # 詳細文件
├── config.json          # 設定檔
└── requirements.txt
```

## 📚 文件

詳細文件請參考 [docs/](./docs/) 目錄：

- [總覽](./docs/00-OVERVIEW.md)
- [novel-to-twee 規格](./docs/01-NOVEL-TO-TWEE.md)
- [twee-processor 規格](./docs/02-TWEE-PROCESSOR.md)
- [asset-previewer 規格](./docs/03-ASSET-PREVIEWER.md)
- [game-assembler 規格](./docs/04-GAME-ASSEMBLER.md)
- [資料格式](./docs/05-DATA-FORMATS.md)
- [共用模組](./docs/06-SHARED-MODULES.md)

## ⚙️ 設定

### AI 設定

支援 Gemini 和 OpenAI：

```json
{
  "ai": {
    "provider": "gemini",
    "gemini": {
      "api_key": "...",
      "model": "gemini-1.5-pro"
    }
  }
}
```

### 圖片生成

支援 Stable Diffusion WebUI 和 Gemini Imagen：

```json
{
  "image_generation": {
    "provider": "stable_diffusion",
    "stable_diffusion": {
      "api_url": "http://localhost:7860"
    }
  }
}
```

### 視覺風格

```json
{
  "visual_style": {
    "current": "anime"
  }
}
```

## 📄 授權

MIT License
