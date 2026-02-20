# Changelog

## [2026-02-20] - 修正圖片生成模型配置

### 修正
- 角色立繪改用 `gemini-3-pro-image-preview`（原本誤用 Imagen 4）
- 表情變化改用 Stable Diffusion img2img（原本誤用 Gemini）
- 新增 `GeminiProImageProvider` 支援 Gemini 3 Pro Image Preview

### 設定變更
`config.json` 圖片生成設定：
```json
{
  "image_generation": {
    "character_provider": "gemini_pro_image",  // 角色用 Gemini 3 Pro
    "scene_provider": "stable_diffusion",       // 場景用 SD
    "expression_provider": "stable_diffusion"   // 表情用 SD img2img
  }
}
```

### 成本影響
| 項目 | 原模型 | 新模型 | 成本變化 |
|------|--------|--------|----------|
| 角色立繪 | Imagen 4 ($0.04-0.08/張) | Gemini 3 Pro ($0.02-0.04/張) | ⬇️ 降低 |
| 表情變化 | Gemini ($0.02-0.04/張) | SD (免費) | ⬇️ 免費 |

---

## [2026-02-20] - Context Caching 支援

### 新增功能

#### Gemini Context Caching
- 新增 Context Caching 支援，可大幅降低重複 API 請求的成本
- 快取輸入成本降低 75%（$0.075 → $0.01875 / 1M tokens）
- 預設 System Prompts 自動快取：
  - `story_analyzer` - 故事分析
  - `scene_detector` - 場景偵測
  - `character_analyzer` - 角色分析
  - `dialogue_parser` - 對話解析

#### 快取管理工具
新增 `manage_cache.py`：
```bash
python manage_cache.py list    # 列出所有快取
python manage_cache.py clear   # 清除所有快取
python manage_cache.py init    # 初始化預設快取
python manage_cache.py status  # 顯示狀態和成本估算
```

### 設定
`config.json` 新增快取設定：
```json
{
  "ai": {
    "cache": {
      "enabled": true,
      "ttl_minutes": 60
    }
  }
}
```

---

## [2026-02-20] - 程式碼清理與改進

### 改進
- `convert_full_story.py` 現在支援命令列參數，不再使用寫死路徑
  - `--project` 指定專案目錄（自動尋找檔案）
  - `--twee`, `--scene-mapping`, `--output` 指定個別檔案
- 新增錯誤處理：場景對應檔案不存在時顯示清楚錯誤訊息

### 移除
- 移除 `fix_script.py`, `fix_script2.py`, `fix_script3.py`（功能已整合到 `shared/script_processor.py`）

### 文件
- 更新 `04-GAME-ASSEMBLER.md` 常見問題排解章節

---

## [2026-02-20] - 表情匯出與 Session 恢復

### 新功能

#### 表情匯出
- 匯出素材時自動包含所有已生成的表情圖片
- 每個角色資料夾會包含：`base.png` + 5 種表情 (`normal.png`, `happy.png`, `sad.png`, `angry.png`, `surprised.png`)
- 匯出確認對話框顯示表情數量
- `info.json` 記錄表情檔案對應

#### Session 恢復改進
- 新增 `restoreExpressionPreviews()` 函數
- 載入 session 時自動恢復已生成的表情預覽
- 表情預覽包含「清除重生」按鈕

### 修復
- 修正匯出只有 `base.png` 沒有表情的問題
- 修正 session.json UTF-8 BOM 導致 Python 無法解析的問題

---

## [2026-02-20] - SD 表情生成功能

### 新增功能

#### SD img2img 表情生成
- 新增 `shared/sd_expression_generator.py` - 使用 Stable Diffusion img2img 生成角色表情變化
- 支援可調整的 **去噪強度 (denoising strength)**：
  - 0.2-0.3：非常像原圖，表情變化小
  - 0.35-0.45：適中（推薦）
  - 0.5-0.6：變化大，可能不像原角色
- 表情 prompt 使用權重語法 `(expression:1.3)` 強調表情特徵
- 自動排除衝突表情（如生成 happy 時排除 crying, tears）

#### UI 改進
- 選定角色圖片後，圖片右上角顯示紅色 ✕ 取消按鈕
- 表情預覽區新增「🗑️ 清除重生」按鈕，方便重新生成
- 去噪強度滑桿控制（0.1 - 0.6）
- 表情生成完成後顯示 denoising 參數

### 修復

- 修正 `saveSession is not defined` JavaScript 錯誤
- 修正表情圖片路徑重複問題
- 修正表情 prompt 導致所有表情都像在哭的問題
- 表情 prompt 現在放在最前面優先處理

### 技術細節

#### SD 表情 Prompt 設計
```python
EXPRESSION_PROMPTS = {
    'happy': '(smiling:1.3), (happy expression:1.2), bright eyes, cheerful',
    'sad': '(sad expression:1.3), (melancholic:1.2), downcast eyes, frowning',
    'angry': '(angry expression:1.3), (furrowed brows:1.2), intense glare',
    # ...
}

EXPRESSION_NEGATIVE = {
    'happy': 'sad, crying, tears, angry, neutral, frown, melancholic',
    'sad': 'happy, smiling, laughing, cheerful, tears, crying',
    # ...
}
```

#### API 端點更新
`POST /api/generate-expressions` 新增參數：
- `method`: `'sd'` 或 `'ai'`（預設 `'sd'`）
- `denoising`: 去噪強度（預設 `0.35`）

### 已知限制

- AI 表情生成（Imagen/Gemini）無法保持角色一致性，建議使用 SD
- SD 需要本地運行 WebUI (`localhost:7860`)
- 建議安裝 ControlNet 以獲得更好的一致性（目前未整合）

---

## [2026-02-19] - Prompt Editor 初版

### 新增功能
- Prompt Editor 網頁介面
- 角色/場景概念圖生成與預覽
- 多模型支援（Gemini Imagen / Stable Diffusion）
- 風格選擇器
- Session 自動儲存/載入
