# Game Assembler 遊戲組裝器

將 Twee 故事檔案 + 素材組裝成可玩的視覺小說 HTML 遊戲。

## 流程

```
story.twee + assets-needed.json + assets/
                    ↓
           [1] twee_analyzer.py
              (AI 分析場景對應 & 對話標記)
                    ↓
           scene-mapping.json
           dialogue-markers.json
                    ↓
           [2] twee_enhancer.py
              (為 Twee 加入標記)
                    ↓
           enhanced-story.twee
                    ↓
           [3] game_builder.py
              (組裝 HTML 遊戲)
                    ↓
           game.html + assets/
```

## 使用方式

### 完整流程（推薦）

```bash
python game-assembler/assemble.py \
    output/project/story.twee \
    output/project/story/assets-needed.json \
    output/project/story/assets/ \
    -o output/project/game/
```

### 只做場景對應（跳過對話分析）

```bash
python game-assembler/assemble.py \
    output/project/story.twee \
    output/project/story/assets-needed.json \
    output/project/story/assets/ \
    -o output/project/game/ \
    --scene-only
```

### 使用已有的分析結果

```bash
python game-assembler/assemble.py \
    output/project/story.twee \
    output/project/story/assets-needed.json \
    output/project/story/assets/ \
    -o output/project/game/ \
    --scene-mapping scene-mapping.json \
    --dialogue-markers dialogue-markers.json
```

## 輸出結構

```
game/
├── game.html              # 主遊戲檔案（用瀏覽器開啟）
├── enhanced-story.twee    # 增強版 Twee（含場景/角色標記）
├── scene-mapping.json     # 場景代碼對應表
├── dialogue-markers.json  # 對話標記（可選）
└── assets/                # 素材副本
    ├── characters/
    │   └── <角色id>/
    │       ├── base.png
    │       ├── normal.png
    │       ├── happy.png
    │       └── ...
    └── scenes/
        └── <場景id>/
            └── background.png
```

## 標記格式

增強版 Twee 使用以下標記：

- `[scene:場景id]` - 切換背景
- `[char:角色id:表情]` - 顯示角色立繪

範例：
```twee
:: Start
[scene:secluded_alleyway]
[char:kazuya:sad]
在黑暗的城市底下，有一個名為「幽影」的秘密組織...

[[繼續->NextPassage]]
```

## 模組說明

### twee_analyzer.py
- 解析 Twee 檔案結構
- 使用 AI 生成場景代碼到場景 ID 的對應
- 使用 AI 分析對話，標記說話者和表情

### twee_enhancer.py
- 將分析結果轉換成標記
- 生成增強版 Twee 檔案

### game_builder.py
- 解析增強版 Twee
- 收集素材
- 生成可玩的 HTML 遊戲

## 遊戲功能

- 場景背景自動切換
- 角色立繪顯示
- 表情變化
- 對話逐句顯示
- 分支選項
