# 遊戲發布工作流程

本文檔說明如何將視覺小說遊戲發布到線上平台。

## 目錄
- [GitHub Pages 發布](#github-pages-發布)
- [Vercel 發布](#vercel-發布)
- [更新主頁](#更新主頁)

---

## GitHub Pages 發布

GitHub Pages 是免費的靜態網站託管服務，適合發布遊戲。

### 前置要求
- Repository 必須是**公開的**（GitHub Pages 免費版限制）
- 遊戲檔案放在 `docs/games/` 資料夾下

### 設定步驟

#### 1. 確保 Repository 是公開的
如果是私有 repository，需要改成公開：
1. 前往 https://github.com/你的用戶名/visual-novel-toolkit
2. 點右上角 **Settings**
3. 拉到最下面的 **Danger Zone**
4. 找到 **Change repository visibility**
5. 點 **Change visibility** → 選 **Make public**
6. 輸入 repository 名稱確認

#### 2. 啟用 GitHub Pages
1. 前往 repository 的 **Settings** → **Pages**
2. 設定：
   - **Source**: Deploy from a branch
   - **Branch**: `main`
   - **Folder**: `/docs` ⚠️ **重要！選 /docs 不是 / (root)**
3. 點 **Save**
4. 等待 1-3 分鐘讓 GitHub 部署

#### 3. 確認部署成功
部署完成後，Settings → Pages 頁面上方會顯示：
```
✅ Your site is live at https://你的用戶名.github.io/visual-novel-toolkit/
```

### 訪問網址
- **主頁**: https://你的用戶名.github.io/visual-novel-toolkit/
- **遊戲**: https://你的用戶名.github.io/visual-novel-toolkit/games/遊戲名稱/

### 發布新遊戲的流程
1. 將遊戲資料夾放到 `docs/games/遊戲名稱/`
2. 更新 `docs/index.html`（見下方「更新主頁」）
3. Git commit & push：
   ```bash
   cd C:\Users\lommi\Projects\visual-novel-toolkit
   git add docs/games/遊戲名稱 docs/index.html
   git commit -m "新增遊戲：遊戲名稱"
   git push
   ```
4. 等待 1-3 分鐘，GitHub Pages 自動更新

---

## Vercel 發布

Vercel 提供更快的部署速度和更多功能，支援私有 repository。

### 前置要求
- GitHub 帳號
- Vercel 帳號（可用 GitHub 登入）

### 設定步驟

#### 1. 連接 Vercel
1. 前往 https://vercel.com/
2. 用 GitHub 帳號登入
3. 點 **Add New** → **Project**
4. 選擇 `visual-novel-toolkit` repository
5. 點 **Import**

#### 2. 設定專案
- **Framework Preset**: Other（或留空）
- **Root Directory**: 選擇 `docs`（點 Edit，然後選 docs 資料夾）
- **Build Command**: 留空（靜態網站不需要）
- **Output Directory**: `.`（當前目錄）

#### 3. 部署
1. 點 **Deploy**
2. 等待部署完成（約 30 秒）
3. 部署成功後會顯示網址：`https://你的專案名稱.vercel.app`

### 訪問網址
- **主頁**: https://你的專案名稱.vercel.app/
- **遊戲**: https://你的專案名稱.vercel.app/games/遊戲名稱/

### 自動部署
設定完成後，每次 push 到 GitHub，Vercel 會自動重新部署：
```bash
git add .
git commit -m "更新遊戲"
git push
```
→ Vercel 自動偵測並部署（約 30 秒）

### 自訂網域（可選）
1. Vercel 專案 → Settings → Domains
2. 輸入你的網域名稱
3. 按照指示設定 DNS

---

## 更新主頁

每次新增遊戲後，需要更新 `docs/index.html` 加入新遊戲卡片。

### 編輯位置
在 `docs/index.html` 找到 `<div class="games-grid">` 區塊。

### 新增遊戲卡片
複製以下模板，修改內容：

```html
<!-- 遊戲名稱 -->
<div class="game-card">
    <a href="./games/遊戲資料夾名稱/">
        <div class="game-cover">🎮</div> <!-- 改成適合的 emoji -->
        <div class="game-info">
            <h2 class="game-title">遊戲完整名稱</h2>
            <p class="game-desc">遊戲簡介，吸引玩家的一兩句話...</p>
            <span class="play-btn">開始遊玩 →</span>
        </div>
    </a>
</div>
```

### 範例
```html
<!-- 圖書館的幽靈 -->
<div class="game-card">
    <a href="./games/小花與佳樹/">
        <div class="game-cover">📚👻</div>
        <div class="game-info">
            <h2 class="game-title">圖書館的幽靈：少女的校園反擊課</h2>
            <p class="game-desc">小花在圖書館遇見了神秘的幽靈佳樹，一段關於復仇與救贖的校園故事就此展開...</p>
            <span class="play-btn">開始遊玩 →</span>
        </div>
    </a>
</div>
```

### Commit 變更
```bash
cd C:\Users\lommi\Projects\visual-novel-toolkit
git add docs/index.html
git commit -m "更新主頁：加入新遊戲"
git push
```

---

## 比較：GitHub Pages vs Vercel

| 特性 | GitHub Pages | Vercel |
|------|--------------|---------|
| **費用** | 完全免費 | 免費（有用量限制） |
| **私有 Repo** | ❌ 需公開 | ✅ 支援 |
| **部署速度** | 1-3 分鐘 | ~30 秒 |
| **自訂網域** | ✅ 支援 | ✅ 支援 |
| **自動部署** | ✅ Push 後自動 | ✅ Push 後自動 |
| **設定難度** | 簡單 | 簡單 |

**建議：**
- 如果不介意公開 repository → 用 **GitHub Pages**（完全免費）
- 如果想保持私有或需要更快部署 → 用 **Vercel**

---

## 疑難排解

### GitHub Pages 顯示 404
1. 確認 Pages 設定的 Folder 是 `/docs` 不是 `/`
2. 確認 repository 是公開的
3. 等待 1-3 分鐘讓部署完成
4. 確認檔案路徑正確（中文路徑需 URL encode）

### Vercel 部署失敗
1. 確認 Root Directory 設定為 `docs`
2. 檢查 Build Command 是否留空
3. 查看 Vercel 部署日誌找錯誤訊息

### 遊戲無法載入資源
1. 檢查遊戲內的路徑是否正確（相對路徑）
2. 確認所有圖片/音檔都已 commit 並 push
3. 查看瀏覽器 Console 的錯誤訊息

---

最後更新：2026-02-21
