# 🚀 部署教學：GitHub + Vercel

本教學說明如何將遊戲部署到 GitHub，並透過 Vercel 發布到網路上。

---

## 📋 事前準備

- [GitHub 帳號](https://github.com)
- [Vercel 帳號](https://vercel.com)（可用 GitHub 登入）
- 你的遊戲檔案（至少要有 `index.html`）

---

## 第一部分：上傳到 GitHub

### 1️⃣ 建立 GitHub 倉庫

1. 登入 GitHub
2. 點右上角 **「+」** → **「New repository」**
3. 輸入倉庫名稱（例如：`my-game`）
4. 選擇 **Public**（公開）
5. 點 **「Create repository」**

### 2️⃣ 上傳檔案

**方法 A：網頁上傳（簡單）**
1. 在倉庫頁面點 **「uploading an existing file」**
2. 把遊戲資料夾裡的檔案拖進去
3. 點 **「Commit changes」**

**方法 B：使用 Git（推薦）**
```bash
# 在你的遊戲資料夾執行
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/你的帳號/你的倉庫.git
git push -u origin main
```

### 3️⃣ 確認檔案結構

確保你的倉庫結構類似這樣：
```
/
├── index.html      ← 首頁（必要）
├── style.css
├── game.js
└── assets/
    └── images...
```

如果你的 `index.html` 在子資料夾（例如 `docs/`），之後在 Vercel 需要設定 Root Directory。

---

## 第二部分：連結 Vercel 並部署

### 1️⃣ 註冊 / 登入 Vercel

1. 前往 https://vercel.com
2. 點 **「Sign Up」** 或 **「Log In」**
3. 選擇 **「Continue with GitHub」**
4. 授權 Vercel 存取你的 GitHub

### 2️⃣ 匯入專案

1. 登入後點 **「Add New...」** → **「Project」**
2. 如果看不到倉庫列表：
   - 點 **「+ Add GitHub Account」** 或 **「Install」**
   - 在 GitHub 頁面選擇授權範圍（建議選 All repositories）
   - 點 **「Install & Authorize」**
3. 找到你的倉庫，點 **「Import」**

### 3️⃣ 設定專案（如需要）

如果你的 `index.html` 在子資料夾：

1. 在 Configure Project 頁面找到 **「Root Directory」**
2. 點 **「Edit」**
3. 輸入資料夾名稱（例如：`docs`）

### 4️⃣ 部署

1. 點 **「Deploy」**
2. 等待 1-2 分鐘
3. 完成後會看到 **「Congratulations!」**
4. 點預覽圖片或 **「Visit」** 查看你的網站

---

## 第三部分：取得網址

部署成功後，你會得到一個網址：
```
https://你的專案名.vercel.app
```

例如本專案的網址結構：
- 首頁：`https://visual-novel-toolkit.vercel.app/`
- 遊戲1：`https://visual-novel-toolkit.vercel.app/game1/`
- 遊戲2：`https://visual-novel-toolkit.vercel.app/game2/`

---

## 🔄 更新網站

之後只要把修改 **push 到 GitHub**，Vercel 會**自動重新部署**！

```bash
git add .
git commit -m "更新內容"
git push
```

### 手動重新部署

如果需要手動觸發：
1. 到 Vercel Dashboard
2. 點進你的專案
3. 點 **「Deployments」** 分頁
4. 找到最新的部署，點 **「⋮」** → **「Redeploy」**

---

## ⚙️ 修改 Root Directory（如果搞錯了）

1. 到 Vercel Dashboard → 點進專案
2. 點上方 **「Settings」**
3. 左側選 **「Build and Deployment」**
4. 找到 **「Root Directory」**（根目錄）
5. 輸入正確的資料夾名稱
6. 點 **「Save」**
7. 回到 Deployments 重新部署

---

## 🌏 關於大陸訪問

Vercel 在大陸的連線**不穩定**，有時可以有時不行。

如果需要穩定讓大陸玩家遊玩，可考慮：
- **Gitee Pages**（需實名認證）
- **自己的伺服器** + 國內域名（需 ICP 備案）
- **微信小遊戲 / QQ小遊戲**

---

## ❓ 常見問題

### Q: 部署後顯示 404 NOT_FOUND？
A: 檢查 Root Directory 設定是否正確，確保指向含有 `index.html` 的資料夾。

### Q: 修改後網站沒更新？
A: 確認是否有 push 到 GitHub。也可以手動 Redeploy。

### Q: Vercel 免費嗎？
A: 個人使用（Hobby plan）完全免費，包含：
- 每月 100GB 流量
- 無限制網站數量
- 自動 HTTPS

---

## 🔒 將 GitHub 倉庫設為私人

如果你不想讓別人看到你的原始碼，可以把倉庫改成 Private（私人）。

### 設定步驟

1. 到你的 GitHub 倉庫頁面
2. 點上方的 **「Settings」**（設定）
3. 滑到最下面找到 **「Danger Zone」**（危險區域）
4. 點 **「Change visibility」**
5. 選 **「Make private」**
6. 輸入倉庫名稱確認
7. 點 **「I understand, change repository visibility」**

### 注意事項

改成 Private 後：
- ✅ Vercel 部署**仍然正常**（因為已經授權連結）
- ✅ 你的遊戲網站**還是公開**可以玩
- ✅ 只有程式碼變成私人，別人看不到
- ❌ 別人無法 fork 或查看你的原始碼

---

*最後更新：2026-02-20*
