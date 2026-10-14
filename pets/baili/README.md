# 白璃 Baili

銀白長髮、紫眼、龍角、白紫裙裝、翅膀與龍尾的 Q 版桌面夥伴，掌心帶著藍色小精靈。

![待機](previews/idle.gif) ![注視方向](previews/look.gif)

[全部動作影片](previews/all-states.mp4) · [透明圖集](spritesheet.png)

## 安裝

在 repository 根目錄執行 `python3 tools/install_pet.py baili`，依桌面 App 的安裝畫面完成，再到 Settings → Pets 選用。這是開啟官方安裝流程，不是跳過 App 確認的自動安裝；桌面安裝尚未實機確認。

## 製作與驗證

2026-10-14 由 imagegen 製作。v2 圖集有九種動作與十六個注視方向，73 個有效格。已依回饋修正轉頭時脖子過長的問題。

圖集結構、透明度、跳躍落地、方向辨識與 Pets 上傳預檢已通過。部分中間方向差異較細微；雲端 Pets 建立／選用確認不代表桌面浮窗已測試。CI 工具只檢查結構與 metadata，未聲稱完整視覺品質驗證。

## 素材來源與授權

由使用者提供角色參考圖後生成；參考圖原作者尚未記錄。角色素材授權目前為 `unspecified`，不適用根目錄程式碼的 MIT 授權。投稿更多角色時應各自附上清楚來源與素材授權。
