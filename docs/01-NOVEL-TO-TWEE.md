# novel-to-twee 規格書

## 📋 功能概述

將純文字小說轉換為 Twee 格式，並由 AI 分析產生劇情分支點。

---

## 📥 輸入

| 項目 | 格式 | 說明 |
|------|------|------|
| 小說檔案 | .txt / .md | 純文字或 Markdown 格式的小說 |

### 輸入範例

```text
和也從小就知道，自己的家庭和別人不一樣。

他的母親總是愛發牢騷，而父親相葉卻是個溫柔的人。

十歲那年，和也無意間聽到了一個秘密。

「他不是你的孩子！」母親的聲音從樓下傳來。

和也愣住了。他不敢相信自己聽到的話。

多年後，和也長大了，成為了一名工程師...
```

---

## 📤 輸出

### 1. story.twee

Twee 格式的故事檔，可在 Twine 編輯。

```twee
:: StoryTitle
理智與感情的界線

:: StoryData
{
  "ifid": "自動生成的UUID",
  "format": "Harlowe",
  "format-version": "3.3.7"
}

:: Start
和也從小就知道，自己的家庭和別人不一樣。

他的母親總是愛發牢騷，而父親相葉卻是個溫柔的人。

[[繼續->發現秘密]]

:: 發現秘密
十歲那年，和也無意間聽到了一個秘密。

「他不是你的孩子！」母親的聲音從樓下傳來。

和也愣住了。

[[悄悄離開->逃避真相]]
[[繼續聽下去->面對真相]]

:: 逃避真相
和也選擇假裝沒聽到...
（分支 A 的劇情）

:: 面對真相
和也決定聽清楚...
（分支 B 的劇情）
```

### 2. analysis.json

AI 分析結果，包含角色、場景、分支點資訊。

```json
{
  "title": "理智與感情的界線",
  "summary": "和也與養父相葉之間的情感故事...",
  
  "characters": [
    {
      "id": "kazuya",
      "name": "和也",
      "description": "主角，年輕工程師，內斂溫和",
      "suggested_expressions": ["normal", "sad", "surprised", "determined"]
    },
    {
      "id": "aiba", 
      "name": "相葉",
      "description": "養父，50多歲，溫柔體貼",
      "suggested_expressions": ["normal", "gentle", "sad", "conflicted"]
    }
  ],
  
  "scenes": [
    {
      "id": "home_living_room",
      "name": "和也家客廳",
      "description": "普通的日式客廳，有些陳舊",
      "mood": "日常、略顯壓抑"
    },
    {
      "id": "repair_shop",
      "name": "相葉的修理店", 
      "description": "小型電器修理店，溫馨懷舊",
      "mood": "溫暖、懷舊"
    }
  ],
  
  "branch_points": [
    {
      "passage": "發現秘密",
      "description": "和也發現身世秘密後的選擇",
      "choices": [
        {"text": "悄悄離開", "target": "逃避真相", "consequence": "走向疏離路線"},
        {"text": "繼續聽下去", "target": "面對真相", "consequence": "走向面對路線"}
      ]
    }
  ],
  
  "endings": [
    {"id": "happy_end", "name": "幸福結局", "description": "和也與相葉和解"},
    {"id": "sad_end", "name": "遺憾結局", "description": "兩人錯過彼此"}
  ]
}
```

---

## ⚙️ 處理邏輯

### Step 1: 載入小說

```python
def load_novel(path: str) -> str:
    """載入小說文字"""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()
```

### Step 2: AI 分析

使用 Gemini API 分析：

```python
def analyze_story(text: str) -> dict:
    """
    AI 分析小說，返回：
    - 角色列表
    - 場景列表  
    - 建議的分支點
    - 故事結構
    """
    prompt = f"""
    分析以下小說，請用 JSON 格式回傳：
    1. characters: 角色列表（id, name, description, suggested_expressions）
    2. scenes: 場景列表（id, name, description, mood）
    3. branch_points: 建議的分支點（哪裡適合讓玩家選擇）
    4. story_structure: 故事結構（開頭、發展、高潮、結局）
    
    小說內容：
    {text}
    """
    return call_gemini(prompt)
```

### Step 3: 生成分支

```python
def generate_branches(analysis: dict, text: str) -> dict:
    """
    根據分析結果，生成分支劇情
    - 每個分支點產生 2-3 個選項
    - 每個選項延伸不同劇情走向
    """
    prompt = f"""
    根據以下故事和分支點建議，生成完整的分支劇情。
    每個分支要有不同的發展和結局。
    
    原始故事：{text}
    分支點：{analysis['branch_points']}
    """
    return call_gemini(prompt)
```

### Step 4: 輸出 Twee

```python
def export_twee(story_data: dict, output_path: str):
    """輸出 Twee 格式檔案"""
    twee_content = generate_twee_header(story_data)
    
    for passage in story_data['passages']:
        twee_content += f"\n:: {passage['name']}\n"
        twee_content += passage['content']
        
        if passage.get('choices'):
            for choice in passage['choices']:
                twee_content += f"\n[[{choice['text']}->{choice['target']}]]"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(twee_content)
```

---

## 🖥️ CLI 介面

```bash
# 基本用法
python novel-to-twee/main.py input.txt

# 指定輸出目錄
python novel-to-twee/main.py input.txt -o output/

# 指定分支數量
python novel-to-twee/main.py input.txt --branches 3

# 互動模式（確認每個分支點）
python novel-to-twee/main.py input.txt --interactive
```

---

## 📋 設定選項

在 `config.json` 中：

```json
{
  "novel_to_twee": {
    "default_branches": 2,
    "min_passage_length": 100,
    "max_passage_length": 500,
    "auto_detect_chapters": true,
    "language": "zh-TW"
  }
}
```

---

## ⚠️ 注意事項

1. **分支品質**：AI 生成的分支需要人工在 Twine 中檢查調整
2. **段落切分**：此工具只做粗略切分，詳細拆分由 `twee-processor` 處理
3. **角色辨識**：AI 可能誤判角色，analysis.json 可手動修正
