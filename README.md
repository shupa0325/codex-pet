# Codex Pet

可持續擴充的 Codex 桌面寵物素材集。每隻寵物有自己的圖集、動畫預覽、版本與作者資訊；先收錄「白璃」，歡迎以 Pull Request 投稿更多角色。

這是社群素材 repository，與 OpenAI 無官方關係。第一版提供素材、安裝流程入口與結構驗證工具；桌面安裝流程尚未實機驗證，不把可開啟安裝視窗宣稱為自動完成安裝。

## 寵物目錄

| 角色 | 預覽 | 格式 | 下載 |
| --- | --- | --- | --- |
| [白璃 Baili](pets/baili/README.md) | ![白璃](pets/baili/previews/idle.gif) | v2，九種動作及十六個注視方向 | [透明 PNG](https://raw.githubusercontent.com/shupa0325/codex-pet/main/pets/baili/spritesheet.png) |

## 其他用戶如何使用

### 開啟桌面安裝流程

安裝支援 Pets 的 Codex／ChatGPT 桌面版本後，下載此 repository，執行：

```sh
python3 tools/install_pet.py baili
```

工具使用 Python 標準函式庫，不需要 API key。它開啟官方的 `codex://pets/install` 連結，由桌面 App 下載公開圖集並處理安裝。第一次可能需要瀏覽器或作業系統確認開啟 App；請依 App 畫面完成，再到 Settings → Pets 選擇角色，使用 `/pet` 或 Show pet 顯示。

不想自動開啟 App，可以列印網址後貼到瀏覽器網址列：

```sh
python3 tools/install_pet.py baili --print-url
```

這個入口需要 App 啟用 Pets 安裝功能。App 對公開 URL 的下載與實際安裝仍需實機確認。v2 圖集必須帶 `spriteVersionNumber=2`；省略參數會使用 v1。

### 只下載素材

直接下載上表 PNG，或在 GitHub 使用 Code → Download ZIP。下載 PNG 本身不會自動安裝。網頁版、桌面版與 CLI 的寵物支援有不同限制，桌面自製寵物也不會自動同步到網頁版。

官方說明：[Pets](https://learn.chatgpt.com/docs/pets) · [安裝 deep link](https://learn.chatgpt.com/docs/reference/commands#pets)。

## 製作與投稿

1. 依 [投稿指南](CONTRIBUTING.md) 建立 `pets/<id>/`。
2. 提供透明圖集、動畫預覽與 `pet.json`；metadata 範本在 `templates/pet.json`。
3. 登記作者與素材授權，更新 `catalog.json`。
4. 執行結構檢查，再開 Pull Request。CI 會重跑檢查；人工作動畫及方向 review。

```sh
python3 -m pip install -r requirements.txt
python3 tools/validate_pets.py
```

檢查工具驗證 metadata、路徑、雜湊、尺寸、透明度、必要格與空格，不取代造型、脖子比例、動作或方向的視覺檢查。

## 結構與授權

```text
catalog.json
pets/<id>/pet.json
pets/<id>/spritesheet.png
pets/<id>/previews/
tools/
templates/
```

程式碼與文件採 [MIT](LICENSE)；有權授權的原創投稿素材預設採 **CC BY 4.0**，詳見 [素材授權政策](LICENSE-ASSETS.md)。各角色實際授權以 `pet.json` 與角色資料夾為準，不能把程式碼 MIT 視為所有角色素材的授權。白璃的參考角色來源尚未確認，素材暫記 `unspecified`；本專案不宣稱持有未知參考角色的原始權利。

未來方向：更多角色、可視化圖庫、安裝流程實機驗證、創作者製作工具，以及跨版本相容性。這些尚未完成。
