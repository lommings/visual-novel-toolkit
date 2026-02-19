# twee-processor 規格書

## 📋 功能概述

處理 Twee 檔案，執行：
1. 分析並提取角色、場景清單
2. 將長段落拆分為適合視覺小說的短句
3. 標記角色對話、場景切換點

---

## 📥 輸入

| 項目 | 格式 | 說明 |
|------|------|------|
| Twee 檔案 | .twee | 從 Twine 編輯後輸出的檔案 |
| analysis.json | .json | (可選) novel-to-twee 的分析結果 |

### 輸入範例 (story.twee)

```twee
:: Start
和也從小就知道，自己的家庭和別人不一樣。他的母親是個愛發牢騷的女人，總是抱怨這抱怨那。而父親相葉卻完全不同，他是個溫柔體貼的男人，總是用溫暖的目光看著和也。

「和也，吃飯了。」相葉溫柔地喊道。

「來了！」和也從房間跑出來。

[[繼續->童年回憶]]

:: 童年回憶
那是和也十歲的時候，他無意間聽到了改變一切的對話...
```

---

## 📤 輸出

### 1. processed.json

完整處理後的故事資料：

```json
{
  "title": "理智與感情的界線",
  "version": "1.0",
  "generated_at": "2026-02-19T21:00:00Z",
  
  "characters": [
    {
      "id": "kazuya",
      "name": "和也",
      "description": "主角，年輕工程師",
      "expressions": ["normal", "sad", "surprised", "happy", "determined", "crying"],
      "color": "#4A90D9"
    },
    {
      "id": "aiba",
      "name": "相葉", 
      "description": "養父，溫柔的中年男子",
      "expressions": ["normal", "gentle", "sad", "pained", "conflicted"],
      "color": "#7CB342"
    },
    {
      "id": "mother",
      "name": "母親",
      "description": "和也的母親，愛抱怨",
      "expressions": ["normal", "sharp", "concerned"],
      "color": "#E91E63"
    }
  ],
  
  "scenes": [
    {
      "id": "home_living_room",
      "name": "家中客廳",
      "description": "普通的日式客廳，有點陳舊但整潔",
      "time_of_day": "日間",
      "mood": "日常"
    },
    {
      "id": "repair_shop", 
      "name": "修理店",
      "description": "小型電器修理店，堆滿工具和零件",
      "time_of_day": "任意",
      "mood": "溫馨懷舊"
    }
  ],
  
  "passages": [
    {
      "name": "Start",
      "scene_id": "home_living_room",
      "lines": [
        {
          "type": "narration",
          "text": "和也從小就知道，自己的家庭和別人不一樣。"
        },
        {
          "type": "narration",
          "text": "他的母親是個愛發牢騷的女人，總是抱怨這抱怨那。"
        },
        {
          "type": "narration", 
          "text": "而父親相葉卻完全不同，他是個溫柔體貼的男人。"
        },
        {
          "type": "narration",
          "text": "相葉總是用溫暖的目光看著和也。"
        },
        {
          "type": "dialogue",
          "character": "aiba",
          "expression": "gentle",
          "text": "和也，吃飯了。"
        },
        {
          "type": "dialogue",
          "character": "kazuya", 
          "expression": "normal",
          "text": "來了！"
        },
        {
          "type": "action",
          "action": "hide_character",
          "character": "kazuya"
        }
      ],
      "choices": [
        {"text": "繼續", "target": "童年回憶"}
      ]
    }
  ]
}
```

### 2. assets-needed.json

需要生成的素材清單：

```json
{
  "characters": [
    {
      "id": "kazuya",
      "name": "和也",
      "expressions_needed": ["normal", "sad", "surprised", "happy", "determined", "crying"]
    },
    {
      "id": "aiba",
      "name": "相葉",
      "expressions_needed": ["normal", "gentle", "sad", "pained", "conflicted"]
    }
  ],
  
  "scenes": [
    {
      "id": "home_living_room",
      "name": "家中客廳",
      "description": "普通的日式客廳，有點陳舊但整潔，日間光線"
    },
    {
      "id": "repair_shop",
      "name": "修理店", 
      "description": "小型電器修理店，堆滿工具和零件，溫馨懷舊氛圍"
    }
  ]
}
```

---

## ⚙️ 處理邏輯

### Step 1: 解析 Twee

```python
def parse_twee(content: str) -> list:
    """
    解析 Twee 格式，返回 passage 列表
    """
    passages = []
    current = None
    
    for line in content.split('\n'):
        if line.startswith(':: '):
            if current:
                passages.append(current)
            current = {
                'name': line[3:].strip(),
                'content': ''
            }
        elif current:
            current['content'] += line + '\n'
    
    if current:
        passages.append(current)
    
    return passages
```

### Step 2: 分析角色與場景

```python
def analyze_content(passages: list) -> dict:
    """
    使用 AI 分析段落內容，識別：
    - 出現的角色
    - 場景位置
    - 對話與旁白
    """
    prompt = f"""
    分析以下故事段落，識別：
    1. 所有角色（名字、描述、需要的表情）
    2. 所有場景（位置、氛圍）
    3. 每句話是對話還是旁白
    4. 對話的說話者和情緒
    
    段落內容：
    {passages}
    """
    return call_gemini(prompt)
```

### Step 3: 拆分段落

```python
def split_text(text: str, max_length: int = 50) -> list:
    """
    將長段落拆分為短句
    
    規則：
    1. 每句不超過 max_length 字
    2. 優先在標點符號處切分
    3. 對話獨立成句
    4. 保持語意完整
    """
    lines = []
    
    # 先按句號、問號、驚嘆號切分
    sentences = re.split(r'([。！？])', text)
    
    current = ''
    for s in sentences:
        if len(current) + len(s) <= max_length:
            current += s
        else:
            if current:
                lines.append(current.strip())
            current = s
    
    if current:
        lines.append(current.strip())
    
    return lines
```

### Step 4: 識別對話

```python
def identify_dialogue(line: str, characters: list) -> dict:
    """
    識別對話行
    
    模式：
    - 「對話內容」角色說
    - 「對話內容」
    - 角色：「對話內容」
    """
    # 對話模式匹配
    patterns = [
        r'「(.+?)」(.+?)(說|道|喊|問|答)',
        r'(.+?)[:：]「(.+?)」',
        r'「(.+?)」'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, line)
        if match:
            return {
                'type': 'dialogue',
                'text': match.group(1),
                'character': identify_speaker(match, characters)
            }
    
    return {'type': 'narration', 'text': line}
```

---

## 🖥️ CLI 介面

```bash
# 基本用法
python twee-processor/main.py story.twee

# 使用現有分析結果
python twee-processor/main.py story.twee --analysis analysis.json

# 指定輸出目錄
python twee-processor/main.py story.twee -o output/

# 設定最大句子長度
python twee-processor/main.py story.twee --max-length 40
```

---

## 📋 設定選項

```json
{
  "twee_processor": {
    "max_line_length": 50,
    "split_on_punctuation": true,
    "detect_dialogue": true,
    "detect_scenes": true,
    "default_expression": "normal"
  }
}
```

---

## ⚠️ 注意事項

1. **對話識別**：中文對話格式多樣，可能需要手動修正
2. **場景判斷**：AI 可能誤判場景切換點
3. **表情對應**：建議的表情可在 asset-previewer 時調整
