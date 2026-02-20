# Monogatari 遊戲轉換說明

## 概述

將 Twee 格式的視覺小說故事轉換為 Monogatari 引擎可執行的遊戲。

## 轉換流程

1. **解析 Twee 檔案** - 讀取 `story.twee`，提取所有段落
2. **場景對應** - 使用 `scene-mapping.json` 將場景代碼對應到背景圖
3. **角色處理** - 偵測文字中的角色名稱，自動顯示立繪
4. **情緒判斷** - 根據關鍵字判斷角色表情
5. **對話格式化** - 將引號對話轉換為角色對話格式

## 轉換腳本

`convert_full_story.py` - 主要轉換腳本

### 角色對應
```python
CHAR_MAPPING = {
    '和也': 'kazuya',
    '相葉': 'aiba'
}
```

### 情緒關鍵字
```python
EMOTION_KEYWORDS = {
    'happy': ['笑', '開心', '高興', '喜', '微笑', '溫暖', '感激', '欣慰'],
    'sad': ['難過', '悲傷', '哭', '淚', '痛苦', '絕望', '憂', '沮喪', '低落'],
    'angry': ['怒', '氣', '憤', '惱', '不滿', '冷'],
    'surprised': ['驚', '震', '嚇', '意外', '沒想到', '愕'],
}
```

### 說話動詞
用於判斷引號內容是否為對話：
```python
SPEAKING_VERBS = ['說', '道', '問', '答', '喊', '叫', '回答', '詢問', '提醒', '告訴', '低聲', '輕聲', '大聲', '回', '應']
```

## 場景對應表

`output/1140119_Temp/game/scene-mapping.json`

| 場景代碼 | 場景名稱 |
|---------|---------|
| S01, S02 | secluded_alleyway |
| S03, S04A-C | aiba_apartment_interior |
| S05A | organization_interrogation_room |
| S06A, S09A | cold_prison_cell |
| S07A, S08A | busy_commercial_district |
| S10A-S12A | private_hospital_ward |
| S13A | final_dark_alley |
| S14A, S15A | rainy_street_lamp |
| S05B-S08C, S13B-C | secret_medical_lab |

## 輸出結構

```
monogatari-game/
├── index.html
├── js/
│   ├── script.js      # 故事腳本（自動生成）
│   ├── main.js
│   ├── options.js
│   └── storage.js
├── style/
│   └── main.css       # 自定義樣式
└── assets/
    ├── scenes/        # 背景圖
    │   ├── secluded_alleyway/
    │   ├── aiba_apartment_interior/
    │   └── ...
    └── characters/    # 角色立繪
        ├── kazuya/
        │   ├── normal.png
        │   ├── happy.png
        │   ├── sad.png
        │   ├── angry.png
        │   └── surprised.png
        └── aiba/
            └── ...
```

## CSS 樣式調整

`style/main.css` 中的重要設定：

```css
/* 角色立繪位置 - 不與對話框重疊 */
[data-character] {
    max-height: 55vh !important;
    bottom: 30vh !important;
}

/* 對話框固定高度 */
[data-component="text-box"] {
    height: 28vh !important;
    background: rgba(0, 0, 0, 0.85) !important;
}

/* 文字放大 */
[data-component="text-box"] p {
    font-size: 1.4rem !important;
}
```

## 待改進項目

- [ ] 角色出場時機更精準（在文字提到後才出現）
- [ ] 文字分段優化（每段約兩行，不以逗號結尾）
- [ ] 場景轉換時機偵測（文字中提到移動時切換場景）
- [ ] 角色退場處理（場景中未提到時隱藏）

## 執行方式

```bash
# 轉換故事
python convert_full_story.py

# 啟動伺服器
cd output/1140119_Temp/monogatari-game
python -m http.server 8888

# 瀏覽器開啟
http://localhost:8888
```
