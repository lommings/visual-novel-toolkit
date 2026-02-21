# 資料格式定義

## 📋 概述

工具鏈中各工具透過 JSON 檔案傳遞資料。本文件定義所有資料格式的規格。

---

## 📄 analysis.json

**產生者**：novel-to-twee  
**使用者**：twee-processor, asset-previewer

```json
{
  "$schema": "analysis-schema.json",
  "version": "1.0",
  "generated_at": "2026-02-19T21:00:00Z",
  "generator": "novel-to-twee v1.0",
  
  "title": "故事標題",
  "summary": "故事簡介...",
  
  "characters": [
    {
      "id": "字串，英文ID，用於程式識別",
      "name": "字串，顯示名稱",
      "description": "字串，角色描述",
      "suggested_expressions": ["normal", "happy", "sad"],
      "appears_in": ["Start", "Chapter1"],
      "notes": "其他備註"
    }
  ],
  
  "scenes": [
    {
      "id": "字串，英文ID",
      "name": "字串，場景名稱",
      "description": "字串，場景描述",
      "location": "字串，地點",
      "time_of_day": "日間 | 夜間 | 黃昏 | 任意",
      "mood": "字串，氛圍描述",
      "appears_in": ["Start", "Chapter1"]
    }
  ],
  
  "branch_points": [
    {
      "passage": "字串，段落名稱",
      "description": "字串，分支描述",
      "choices": [
        {
          "text": "選項文字",
          "target": "目標段落",
          "consequence": "選擇後果描述"
        }
      ]
    }
  ],
  
  "endings": [
    {
      "id": "結局ID",
      "name": "結局名稱",
      "type": "good | bad | neutral",
      "description": "結局描述"
    }
  ]
}
```

### 欄位說明

| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| version | string | ✓ | 格式版本 |
| title | string | ✓ | 故事標題 |
| characters | array | ✓ | 角色列表 |
| characters[].id | string | ✓ | 英文ID，只能含 a-z, 0-9, _ |
| characters[].name | string | ✓ | 顯示名稱 |
| scenes | array | ✓ | 場景列表 |
| branch_points | array | | 分支點列表 |
| endings | array | | 結局列表 |

---

## 📄 processed.json

**產生者**：twee-processor  
**使用者**：asset-previewer, game-assembler

```json
{
  "$schema": "processed-schema.json",
  "version": "1.0",
  "generated_at": "2026-02-19T22:00:00Z",
  "source_file": "story.twee",
  
  "title": "故事標題",
  
  "characters": [
    {
      "id": "kazuya",
      "name": "和也",
      "description": "主角描述",
      "expressions": ["normal", "sad", "happy", "surprised"],
      "color": "#4A90D9"
    }
  ],
  
  "scenes": [
    {
      "id": "home_living_room",
      "name": "家中客廳",
      "description": "場景描述",
      "time_of_day": "日間",
      "mood": "日常"
    }
  ],
  
  "passages": [
    {
      "name": "Start",
      "scene_id": "home_living_room",
      "lines": [
        {
          "type": "narration",
          "text": "旁白文字"
        },
        {
          "type": "dialogue",
          "character": "kazuya",
          "expression": "normal",
          "text": "對話文字"
        },
        {
          "type": "action",
          "action": "show_character | hide_character | change_scene",
          "character": "kazuya",
          "expression": "happy"
        }
      ],
      "choices": [
        {
          "text": "選項文字",
          "target": "目標段落"
        }
      ]
    }
  ]
}
```

### Line 類型

| type | 必要欄位 | 說明 |
|------|---------|------|
| narration | text | 旁白 |
| dialogue | character, text | 對話 |
| action | action | 動作指令 |

### Action 類型

| action | 參數 | 說明 |
|--------|------|------|
| show_character | character, expression | 顯示角色 |
| hide_character | character | 隱藏角色 |
| change_scene | scene_id | 切換場景 |

---

## 📄 assets-needed.json

**產生者**：twee-processor  
**使用者**：asset-previewer

```json
{
  "$schema": "assets-needed-schema.json",
  "version": "1.0",
  "generated_at": "2026-02-19T22:00:00Z",
  
  "characters": [
    {
      "id": "kazuya",
      "name": "和也",
      "description": "年輕工程師，內斂溫和，25歲左右",
      "expressions_needed": ["normal", "sad", "happy", "surprised", "determined"],
      "visual_notes": "短髮、戴眼鏡、穿著休閒"
    }
  ],
  
  "scenes": [
    {
      "id": "home_living_room",
      "name": "家中客廳",
      "description": "普通的日式客廳，有點陳舊但整潔",
      "time_of_day": "日間",
      "mood": "日常、略顯壓抑",
      "visual_notes": "木質地板、老舊沙發、窗戶透進陽光"
    }
  ]
}
```

---

## 📄 selections.json

**產生者**：asset-previewer (網頁介面)  
**使用者**：asset-previewer (生成正式素材)

```json
{
  "$schema": "selections-schema.json",
  "version": "1.0",
  "selected_at": "2026-02-19T23:00:00Z",
  
  "characters": {
    "kazuya": {
      "selected_concept": "concept_2",
      "concept_file": "preview/characters/kazuya/concept_2.png",
      "notes": "使用者備註"
    },
    "aiba": {
      "selected_concept": "concept_1",
      "concept_file": "preview/characters/aiba/concept_1.png",
      "notes": ""
    }
  },
  
  "scenes": {
    "home_living_room": {
      "selected_concept": "concept_3",
      "concept_file": "preview/scenes/home_living_room/concept_3.jpg",
      "notes": ""
    }
  }
}
```

---

## 📄 config.json

**全域設定檔**

```json
{
  "$schema": "config-schema.json",
  "version": "1.0",
  
  "ai": {
    "provider": "gemini",
    "gemini": {
      "api_key": "your-api-key",
      "model": "gemini-1.5-pro"
    },
    "openai": {
      "api_key": "",
      "model": "gpt-4"
    }
  },
  
  "image_generation": {
    "provider": "stable_diffusion",
    "stable_diffusion": {
      "api_url": "http://localhost:7860",
      "default_model": "animagine-xl",
      "defaults": {
        "steps": 30,
        "cfg_scale": 7.5,
        "width": 512,
        "height": 768
      }
    },
    "gemini_imagen": {
      "model": "imagen-3"
    }
  },
  
  "visual_style": {
    "current": "anime",
    "styles": {
      "anime": {
        "name": "動漫風格",
        "character_prompt_suffix": "anime style, visual novel sprite, detailed",
        "scene_prompt_suffix": "anime style, detailed background, visual novel"
      },
      "semi_realistic": {
        "name": "半寫實",
        "character_prompt_suffix": "semi-realistic, detailed portrait",
        "scene_prompt_suffix": "semi-realistic, cinematic lighting"
      }
    }
  },
  
  "novel_to_twee": {
    "default_branches": 2,
    "min_passage_length": 100,
    "max_passage_length": 500
  },
  
  "twee_processor": {
    "max_line_length": 50,
    "split_on_punctuation": true,
    "detect_dialogue": true
  },
  
  "asset_previewer": {
    "character_concepts_count": 4,
    "scene_concepts_count": 3,
    "preview_port": 8080,
    "auto_open_browser": true
  },
  
  "game_assembler": {
    "engine_template": "templates/monogatari",
    "default_text_speed": 30
  },
  
  "paths": {
    "output_dir": "output",
    "preview_dir": "preview",
    "templates_dir": "templates"
  }
}
```

---

## 📁 目錄結構慣例

### 工作目錄

```
project_name/
├── input/
│   └── novel.txt           # 原始小說
├── twee/
│   ├── story.twee          # 生成的 Twee
│   └── edited.twee         # 編輯後的 Twee
├── data/
│   ├── analysis.json       # 分析結果
│   ├── processed.json      # 處理後資料
│   ├── assets-needed.json  # 素材需求
│   └── selections.json     # 選擇結果
├── preview/
│   ├── characters/         # 角色預覽圖
│   ├── scenes/             # 場景預覽圖
│   └── preview.html        # 預覽網頁
├── assets/
│   ├── characters/         # 正式角色圖
│   └── scenes/             # 正式場景圖
└── output/
    └── game/               # 最終遊戲
```

---

## ✅ 驗證規則

所有 JSON 檔案應符合：

1. **UTF-8 編碼**：必須使用 UTF-8 無 BOM
2. **有效 JSON**：可被標準 JSON 解析器解析
3. **必填欄位**：所有標記為必填的欄位都要存在
4. **ID 格式**：所有 ID 只能包含 `a-z`, `0-9`, `_`
5. **路徑格式**：使用正斜線 `/`，相對路徑
