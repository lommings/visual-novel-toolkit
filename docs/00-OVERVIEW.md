# Visual Novel Toolkit - 專案總覽

## 🎯 專案目標

將小說文字轉換為可遊玩的視覺小說遊戲，並在過程中提供：
- AI 自動分析與分支生成
- 人工可介入的預覽與挑選機制
- 模組化設計，方便維護與擴充

---

## 🔄 完整工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                        使用者流程                            │
└─────────────────────────────────────────────────────────────┘

    小說.txt
        │
        ▼
┌───────────────┐
│ novel-to-twee │  AI 分析故事，產生分支選項
└───────┬───────┘
        │ 輸出：story.twee + analysis.json
        ▼
   ┌─────────┐
   │  Twine  │  手動編輯分支、調整劇情
   └────┬────┘
        │ 輸出：edited.twee
        ▼
┌─────────────────┐
│ twee-processor  │  分析角色/場景 + 拆分長段落
└───────┬─────────┘
        │ 輸出：processed.json + assets-needed.json
        ▼
┌─────────────────┐
│ asset-previewer │  生成預覽圖 → 網頁挑選 → 生成正式圖
└───────┬─────────┘
        │ 輸出：characters/ + scenes/ + selections.json
        ▼
   ┌──────────────┐
   │ 手動剪裁調整  │  統一構圖、去除多餘空間
   └──────┬───────┘
          ▼
┌───────────────────────┐
│ character-standardizer │  統一調整角色立繪高度
└───────┬───────────────┘
        │ 輸出：標準化的角色圖片
        ▼
┌─────────────────┐
│ game-assembler  │  組合文字 + 圖片 → Monogatari 遊戲
└───────┬─────────┘
        │
        ▼
    完整遊戲/
```

---

## 📦 工具清單

| 工具名稱 | 功能 | 輸入 | 輸出 |
|----------|------|------|------|
| `novel-to-twee` | 小說→Twee+分支 | .txt/.md | .twee + analysis.json |
| `twee-processor` | 分析+拆分段落 | .twee | processed.json |
| `asset-previewer` | 預覽+挑選圖片 | processed.json | 圖片 + selections.json |
| `character-standardizer` | 標準化角色尺寸 | 角色圖片資料夾 | 統一高度的圖片 |
| `game-assembler` | 組合成遊戲 | processed.json + 圖片 | Monogatari 遊戲 |

---

## 📁 專案結構

```
visual-novel-toolkit/
├── docs/                        # 規劃文件（你正在看的）
│   ├── 00-OVERVIEW.md           # 總覽
│   ├── 01-NOVEL-TO-TWEE.md      # novel-to-twee 規格
│   ├── 02-TWEE-PROCESSOR.md     # twee-processor 規格
│   ├── 03-ASSET-PREVIEWER.md    # asset-previewer 規格
│   ├── 04-CHARACTER-STANDARDIZER.md  # character-standardizer 規格
│   ├── 05-GAME-ASSEMBLER.md     # game-assembler 規格
│   ├── 06-DATA-FORMATS.md       # 資料格式定義
│   └── 07-SHARED-MODULES.md     # 共用模組說明
│
├── shared/                      # 共用模組
│   ├── __init__.py
│   ├── ai_client.py             # AI API 封裝
│   ├── image_generator.py       # 圖片生成封裝
│   ├── config_manager.py        # 設定管理
│   └── models/                  # 資料模型
│       ├── story.py
│       ├── character.py
│       └── scene.py
│
├── novel-to-twee/               # 工具一
│   ├── main.py
│   ├── story_analyzer.py
│   ├── branch_generator.py
│   └── twee_exporter.py
│
├── twee-processor/              # 工具二
│   ├── main.py
│   ├── twee_parser.py
│   ├── content_analyzer.py
│   └── text_splitter.py
│
├── asset-previewer/             # 工具三
│   ├── main.py
│   ├── preview_generator.py
│   ├── web_server.py
│   └── templates/
│       └── preview.html
│
├── game-assembler/              # 工具四
│   ├── main.py
│   ├── script_generator.py
│   └── monogatari_exporter.py
│
├── tools/                       # 輔助工具
│   ├── standardize_characters.py  # 角色立繪標準化
│   └── README.md
│
├── config.json                  # 全域設定
├── requirements.txt             # Python 依賴
└── README.md                    # 使用說明
```

---

## ⚙️ 技術選型

| 項目 | 選擇 | 原因 |
|------|------|------|
| 程式語言 | Python 3.10+ | 生態豐富、AI 整合方便 |
| AI 文字分析 | Gemini API | 支援中文、效果好 |
| AI 圖片生成 | SD WebUI / Gemini Imagen | 本地免費 / 雲端穩定 |
| 遊戲引擎 | Monogatari | 功能完整、網頁即玩 |
| 預覽介面 | HTML + 本地 HTTP Server | 簡單、跨平台 |

---

## 🔗 工具間的資料傳遞

所有工具透過 JSON 檔案傳遞資料，方便：
- 人工檢視與修改
- Debug 時追蹤問題
- 跳過某個步驟重新執行

詳見 [06-DATA-FORMATS.md](./06-DATA-FORMATS.md)

---

## 📅 開發順序

1. `shared/` - 共用模組（AI、圖片生成、設定）
2. `novel-to-twee` - 小說轉 Twee
3. `twee-processor` - Twee 分析與拆分
4. `asset-previewer` - 預覽與挑選
5. `tools/standardize_characters` - 角色立繪標準化
6. `game-assembler` - 組合遊戲

---

## 📝 版本紀錄

| 日期 | 版本 | 說明 |
|------|------|------|
| 2026-02-19 | v0.1 | 初版規劃 |
| 2026-02-21 | v0.2 | 新增角色立繪標準化工具 |
