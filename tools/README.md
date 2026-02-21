# Tools - 工具集

這個資料夾包含輔助工具，用於處理視覺小說素材。

---

## 📏 standardize_characters.py

**功能**：標準化角色立繪大小

**使用場景**：在手動剪裁角色圖片後，統一調整到相同高度，確保遊戲中人物大小一致。

### 使用方式

#### 1. 預覽效果（不修改檔案）

```bash
python tools/standardize_characters.py "output/20260220_小花與佳樹/story/assets/characters" --preview --height 1200
```

輸出範例：
```
[*] 找到 3 個角色資料夾
[*] 目標高度: 1200px
[*] 檔案名稱: normal.png
[*] 預覽模式（不會修改檔案）

[o] daiki: 635x600 -> 1270x1200
[o] hanako: 788x1000 -> 945x1200
[o] yoshiki: 525x590 -> 1067x1200

[*] 處理完成: 3 個成功, 0 個跳過
```

#### 2. 執行標準化（實際修改檔案）

確認預覽效果無誤後，移除 `--preview` 參數：

```bash
python tools/standardize_characters.py "output/20260220_小花與佳樹/story/assets/characters" --height 1200
```

### 參數說明

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `assets_dir` | 角色素材目錄 | 必填 |
| `--height` | 目標高度（像素） | 1200 |
| `--preview` | 只預覽，不修改 | false |
| `--file` | 要處理的檔名 | normal.png |

### 工作流程建議

```
1. asset-previewer 生成圖片
        ↓
2. 手動選擇最佳候選圖
        ↓
3. 手動剪裁（調整構圖、去除多餘空間）
   工具：Photoshop / GIMP / Paint.NET
        ↓
4. 執行 standardize_characters.py
   （統一調整到相同高度）
        ↓
5. game-assembler 組裝遊戲
```

### 範例

#### 處理特定高度

```bash
# 半身像（1200px）
python tools/standardize_characters.py story/assets/characters --height 1200

# 全身像（1800px）
python tools/standardize_characters.py story/assets/characters --height 1800
```

#### 處理不同表情

預設只處理 `normal.png`，如果要處理其他表情：

```bash
python tools/standardize_characters.py story/assets/characters --height 1200 --file happy.png
```

---

## 注意事項

⚠️ **執行前建議**：
1. 先使用 `--preview` 預覽效果
2. 確認高度設定合理
3. 建議先提交 Git，方便回復

✅ **建議設定**：
- 半身像：`--height 1200`
- 全身像：`--height 1800`
- 保持寬度自動調整（維持原始比例）

💡 **提示**：
- 工具會保持原始圖片的長寬比
- 只調整高度，寬度自動計算
- 覆蓋原檔案，建議先備份
