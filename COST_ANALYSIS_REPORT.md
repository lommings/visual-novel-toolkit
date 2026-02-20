# Visual Novel Toolkit - API 成本分析報告

**分析日期:** 2026-02-20
**問題:** 一天花了 $62 USD

---

## 📊 專案配置

```json
{
  "文字模型": "gemini-2.0-flash",
  "角色圖片": "gemini_imagen (imagen-4.0-generate-001)",
  "場景圖片": "stable_diffusion (免費)"
}
```

---

## 💰 API 價格表

### 圖片生成（最貴！）

| 模型 | 單價 | 說明 |
|------|------|------|
| `imagen-4.0-generate-001` | $0.05/張 | 角色立繪、表情 fallback |
| `gemini-3-pro-image-preview` | $0.03/張 | 表情變化生成 |
| Stable Diffusion | $0/張 | 本地運行，完全免費 |

### 文字生成（便宜）

| 模型 | 價格 | 說明 |
|------|------|------|
| `gemini-2.0-flash` | ~$0.001/次 | 故事分析、角色識別 |

---

## 🔍 成本來源分析

### 1. 角色概念圖生成

**位置:** `asset-previewer/preview_generator.py`

- 每個角色生成 **4 張概念圖**
- 使用 Imagen 4（$0.05/張）
- 2 個角色 × 4 張 = 8 張 = **$0.40**

### 2. 表情生成（主要成本！）

**位置:** `shared/expression_generator.py`

**流程:**
1. 先嘗試 Gemini 3 Pro Image Preview（$0.03/張）
2. 如果失敗，fallback 到 Imagen 4（$0.05/張）
3. 如果還失敗，複製原圖

**成本計算（2 角色 × 5 表情）:**
- 最佳情況（Gemini 成功）: 8 張 × $0.03 = **$0.24**
- 最差情況（全部 fallback）: 8 張 × $0.05 = **$0.40**
- 混合情況: 約 **$0.32**

### 3. 預覽/測試調用

**位置:** `asset-previewer/prompt_server.py`（Web API）

如果頻繁：
- 刷新預覽頁面
- 重複生成概念圖
- 測試不同風格

每次都會消耗 API！

---

## 🧮 反推 $62/天 的使用量

### 假設全是 Imagen 4

```
$62 ÷ $0.05 = 1,240 張圖片/天
```

### 假設全是 Gemini 3 Pro

```
$62 ÷ $0.03 = 2,067 張圖片/天
```

### 混合情況

假設 70% Imagen + 30% Gemini Pro:
- Imagen: 868 張 × $0.05 = $43.40
- Gemini: 620 張 × $0.03 = $18.60
- 總計: $62

---

## 🎯 可能的原因

### 原因 1: 頻繁重複生成

- 每次運行腳本都重新生成所有圖片
- 沒有檢查圖片是否已存在
- 沒有快取機制

### 原因 2: 測試導致大量調用

- 預覽 API 伺服器頻繁被調用
- 測試不同風格/模型
- 每次測試都生成新圖

### 原因 3: 表情 Fallback 頻繁發生

- Gemini 3 Pro 經常失敗
- 每次失敗都 fallback 到 Imagen 4
- 成本加倍

### 原因 4: 腳本重複執行

- 自動化腳本多次運行
- 沒有跳過已完成的任務

---

## 💡 優化建議

### 立即優化（省 50-80%）

#### 1. 改用 Stable Diffusion 生成角色

**修改 `config.json`:**
```json
{
  "image_generation": {
    "character_provider": "stable_diffusion",  // 改這裡
    "scene_provider": "stable_diffusion"
  }
}
```

**效果:** 角色和場景圖片完全免費！

#### 2. 減少概念圖數量

**修改 `config.json`:**
```json
{
  "asset_previewer": {
    "character_concepts_count": 2,  // 原本 4
    "scene_concepts_count": 2       // 原本 3
  }
}
```

**效果:** 減少 50% 圖片生成

#### 3. 減少表情數量

只生成必要的表情：
```python
expressions = ['normal', 'happy', 'sad']  # 只要 3 種
```

**效果:** 減少 40% 表情生成

### 中期優化

#### 4. 加入圖片快取機制

在生成前檢查圖片是否已存在：
```python
if output_path.exists():
    print(f"[SKIP] 圖片已存在: {output_path}")
    return True
```

#### 5. 移除表情 Fallback

如果 Gemini 3 Pro 失敗，直接複製原圖，不要 fallback 到 Imagen：
```python
# expression_generator.py
# 註解掉 fallback 到 Imagen 的程式碼
```

---

## 📊 優化後的成本估算

### 優化前（當前）

| 項目 | 數量 | 單價 | 成本 |
|------|------|------|------|
| 角色概念圖 | 8 張 | $0.05 | $0.40 |
| 表情生成 | 8 張 | $0.04 | $0.32 |
| 場景 | 免費 | $0 | $0 |
| **單次總計** | | | **$0.72** |
| **每天 100 次** | | | **$72** |

### 優化後（改用 SD + 減少數量）

| 項目 | 數量 | 單價 | 成本 |
|------|------|------|------|
| 角色概念圖 | 4 張 | $0 (SD) | $0 |
| 表情生成 | 4 張 | $0 (SD) | $0 |
| 場景 | 免費 | $0 | $0 |
| **單次總計** | | | **$0** |
| **每天 100 次** | | | **$0** |

**節省: 100%** 🎉

---

## 🔧 立即執行

### 步驟 1: 修改 config.json

```json
{
  "image_generation": {
    "character_provider": "stable_diffusion",
    "scene_provider": "stable_diffusion",
    ...
  },
  "asset_previewer": {
    "character_concepts_count": 2,
    "scene_concepts_count": 2,
    ...
  }
}
```

### 步驟 2: 加入快取檢查（可選）

在 `image_generator.py` 中加入：
```python
def generate(self, prompt, output_path, **kwargs):
    if Path(output_path).exists():
        print(f"[SKIP] Image exists: {output_path}")
        return True
    # ... 原本的生成邏輯
```

### 步驟 3: 停止不必要的測試

避免頻繁執行生成腳本，除非真的需要新圖片。

---

## 📞 需要更多幫助？

1. **追蹤 API 調用** - 執行 `python cost_tracker.py --breakdown`
2. **分析使用模式** - 檢查何時/為何調用 API
3. **進一步優化** - 根據實際使用情況調整

---

## ✅ 總結

**問題:** $62/天 主要來自 Imagen 4 圖片生成

**解決方案:**
1. 改用 Stable Diffusion（免費）
2. 減少生成數量
3. 加入快取機制

**預期效果:** 成本降至 $0-5/天（節省 90-100%）
