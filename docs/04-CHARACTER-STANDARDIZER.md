# character-standardizer 規格書

## 📋 功能概述

在手動剪裁角色立繪後，統一調整到相同高度，確保遊戲中人物顯示大小一致。

**工具位置**：`tools/standardize_characters.py`

**使用時機**：在 asset-previewer 生成圖片後、game-assembler 組裝遊戲前

---

## 📥 輸入

| 項目 | 格式 | 說明 |
|------|------|------|
| 角色立繪資料夾 | 目錄路徑 | 包含角色圖片的資料夾 (例如: `story/assets/characters`) |

**資料夾結構**：
```
characters/
├── hanako/
│   └── normal.png  ← 手動剪裁後的圖片
├── yoshiki/
│   └── normal.png
└── daiki/
    └── normal.png
```

---

## 📤 輸出

**覆蓋原圖片**，調整為統一高度（保持原始比例）

---

## 🎯 為什麼需要這個工具？

### 問題背景

AI 生成的角色圖片經常有以下問題：
1. **人物比例不一致**：同樣的 prompt，有些角色畫得大、有些畫得小
2. **構圖差異**：有的是全身、有的是半身、有的是大頭照
3. **空白空間不同**：有的圖片周圍留白多、有的緊湊

直接使用這些圖片會導致**遊戲中角色大小不一致**，影響視覺體驗。

### 解決方案

```
AI 生成圖片 → 手動選擇最佳候選 → 手動剪裁調整構圖 → 自動標準化尺寸
     ↓              ↓                    ↓                   ↓
 4張候選        選1張            統一構圖風格         統一顯示大小
(比例不一)    (人工判斷)      (半身/全身一致)        (頭部大小一致)
```

---

## 🔧 使用方式

### Step 1: 預覽效果

先預覽標準化後的尺寸，不實際修改檔案：

```bash
python tools/standardize_characters.py \
    "output/專案名稱/story/assets/characters" \
    --preview \
    --height 1200
```

**輸出範例**：
```
[*] 找到 3 個角色資料夾
[*] 目標高度: 1200px
[*] 檔案名稱: normal.png
[*] 預覽模式（不會修改檔案）

[o] daiki: 635x600 -> 1270x1200
[o] hanako: 788x1000 -> 945x1200
[o] yoshiki: 525x590 -> 1067x1200

[*] 處理完成: 3 個成功, 0 個跳過

[!] 這是預覽模式，沒有實際修改檔案
    移除 --preview 參數來執行標準化
```

### Step 2: 執行標準化

確認預覽效果無誤後，移除 `--preview` 執行：

```bash
python tools/standardize_characters.py \
    "output/專案名稱/story/assets/characters" \
    --height 1200
```

**執行後**：
```
[*] 找到 3 個角色資料夾
[*] 目標高度: 1200px
[*] 檔案名稱: normal.png

[+] daiki: 635x600 -> 1270x1200
[+] hanako: 788x1000 -> 945x1200
[+] yoshiki: 525x590 -> 1067x1200

[*] 處理完成: 3 個成功, 0 個跳過

[+] 標準化完成！
    所有角色立繪已統一調整為高度 1200px
```

---

## ⚙️ 參數說明

| 參數 | 類型 | 預設值 | 說明 |
|------|------|--------|------|
| `assets_dir` | 字串 | *必填* | 角色素材目錄路徑 |
| `--height` | 整數 | 1200 | 目標高度（像素） |
| `--preview` | 布林 | false | 預覽模式（不修改檔案） |
| `--file` | 字串 | normal.png | 要處理的檔名 |

### 建議的高度設定

| 立繪類型 | 建議高度 | 說明 |
|----------|----------|------|
| 半身像（頭到胸） | 1200px | 適合對話密集的視覺小說 |
| 半身像（頭到腰） | 1500px | 平衡顯示效果和檔案大小 |
| 全身像 | 1800px | 需要展示全身姿勢時使用 |
| 大頭照 | 800-1000px | 強調表情細節 |

---

## 📋 完整工作流程

```
┌────────────────────────────────────────────────┐
│   3. asset-previewer 生成預覽圖                │
│      python asset-previewer/main.py ...        │
│      輸出: preview/characters/                 │
│             └─ hanako/concept_1~4.png          │
└──────────────────┬─────────────────────────────┘
                   ↓
┌────────────────────────────────────────────────┐
│   手動選擇最佳候選圖                            │
│   - 選擇構圖最佳的一張                          │
│   - 複製到 assets/characters/*/normal.png      │
└──────────────────┬─────────────────────────────┘
                   ↓
┌────────────────────────────────────────────────┐
│   手動剪裁調整構圖 ✂️                           │
│   - 用圖片編輯器（PS/GIMP/Paint.NET）打開      │
│   - 統一構圖風格（都是半身 或 都是全身）        │
│   - 去除多餘空白、調整人物位置                  │
│   - 保存覆蓋原檔案                              │
└──────────────────┬─────────────────────────────┘
                   ↓
┌────────────────────────────────────────────────┐
│ ◀◀ 4. character-standardizer 標準化尺寸        │
│    python tools/standardize_characters.py \    │
│        story/assets/characters --height 1200   │
│    輸出: 覆蓋原檔案，統一高度                   │
└──────────────────┬─────────────────────────────┘
                   ↓
┌────────────────────────────────────────────────┐
│   5. game-assembler 組裝遊戲                   │
│      python game-assembler/main.py ...         │
│      輸出: game/                               │
└────────────────────────────────────────────────┘
```

---

## 🧮 技術實作

### 核心邏輯

```python
from PIL import Image

def standardize_character(image_path, target_height=1200):
    # 1. 載入圖片
    img = Image.open(image_path)
    original_size = img.size
    
    # 2. 計算新尺寸（保持比例）
    ratio = img.size[0] / img.size[1]
    target_width = int(target_height * ratio)
    new_size = (target_width, target_height)
    
    # 3. 縮放（使用高品質演算法）
    img_resized = img.resize(new_size, Image.Resampling.LANCZOS)
    
    # 4. 覆蓋原檔案
    img_resized.save(image_path)
    
    return original_size, new_size
```

### 為什麼只調整高度？

1. **高度決定人物大小**：在視覺小說中，角色通常從畫面底部延伸，高度決定了頭部大小
2. **保持原始比例**：不同角色的體型、姿勢可能不同，強制統一寬度會變形
3. **寬度自動計算**：根據原始比例計算，避免拉伸

### 為什麼使用 LANCZOS？

| 演算法 | 速度 | 品質 | 適用場景 |
|--------|------|------|----------|
| NEAREST | 最快 | 差 | 像素藝術 |
| BILINEAR | 快 | 中 | 縮圖預覽 |
| **LANCZOS** | 慢 | **最佳** | **正式素材** |

LANCZOS 提供最佳的縮放品質，適合角色立繪這種需要細節的圖片。

---

## 💡 最佳實踐

### ✅ 推薦做法

1. **統一構圖風格**
   - 所有角色都是半身 或 都是全身
   - 頭部在畫面中的位置相近（如：眼睛在上 1/3）

2. **預覽後再執行**
   - 先用 `--preview` 檢查效果
   - 確認高度設定合理

3. **Git 版本控制**
   - 執行前先 commit
   - 方便回復如果效果不理想

4. **分批處理**
   - 先處理主要角色測試
   - 確認效果後再批次處理所有角色

### ❌ 避免做法

1. **不要跳過手動剪裁**
   - 直接標準化會保留原始構圖問題
   - 必須先手動統一構圖風格

2. **不要設定過小的高度**
   - 太小會失去細節
   - 最低建議 800px

3. **不要在未備份時執行**
   - 工具會覆蓋原檔案
   - 建議先 Git commit

---

## 🔍 故障排除

### 問題：標準化後頭部大小還是不一致

**原因**：手動剪裁時構圖不統一

**解決方案**：
1. 回到手動剪裁步驟
2. 確保所有角色：
   - 頭部在畫面中的比例相近（如：頭部佔畫面高度 25-30%）
   - 眼睛的垂直位置相近（如：在畫面上 1/3）
   - 肩膀寬度比例相近

### 問題：某些角色變形

**原因**：原始圖片比例極端（過寬或過窄）

**解決方案**：
1. 手動重新剪裁，調整到合理比例
2. 或使用不同的目標高度
3. 或針對該角色單獨處理：
   ```bash
   # 只處理特定角色
   python tools/standardize_characters.py story/assets/characters/yoshiki --height 1500
   ```

### 問題：畫質下降

**原因**：原始圖片太小，放大後失真

**解決方案**：
1. 回到 asset-previewer，用更高解析度重新生成
2. 或接受較低畫質
3. 或使用 AI 放大工具（如 waifu2x）先放大

---

## 📝 範例

### 範例一：標準化半身像

```bash
# 預覽
python tools/standardize_characters.py \
    "output/小花與佳樹/story/assets/characters" \
    --preview \
    --height 1200

# 執行
python tools/standardize_characters.py \
    "output/小花與佳樹/story/assets/characters" \
    --height 1200
```

### 範例二：標準化全身像

```bash
python tools/standardize_characters.py \
    "output/專案名/story/assets/characters" \
    --height 1800
```

### 範例三：只處理特定表情

```bash
# 處理 happy.png
python tools/standardize_characters.py \
    "story/assets/characters" \
    --height 1200 \
    --file happy.png
```

---

## 🎯 與其他工具的關係

| 前置工具 | 本工具 | 後續工具 |
|----------|--------|----------|
| asset-previewer | **character-standardizer** | game-assembler |
| 生成候選圖 | 標準化尺寸 | 組裝遊戲 |
| 自動化 | **人工介入** | 自動化 |

**人工介入的價值**：
- AI 無法保證構圖一致性
- 人工選擇和剪裁能確保最佳視覺效果
- 標準化工具只負責技術性的尺寸統一

---

## 📌 總結

這個工具的設計哲學：
1. ✅ **尊重人工判斷**：不強制自動化所有步驟
2. ✅ **提供彈性**：預覽模式、可調整參數
3. ✅ **專注單一職責**：只處理尺寸標準化
4. ✅ **易於使用**：命令行工具，簡單直接

**適用場景**：任何需要多個角色立繪尺寸一致的視覺小說專案
