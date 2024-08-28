# PPT 爬蟲程式v0.0.1
---


## 建立虛擬環境
```bash
.\build.ps1
```


## 啟用虛擬環境
```bash
.\activate.ps1
```


## 新增 `.env` 環境變數並登錄Token
```yaml
# .env file
Token=Your_Line_Notify_Token
```


## 執行爬蟲
```bash
python main.py <目標看版> <目標頁數>
```
範例:
```bash
python main.py Tech_Job 1000
```


## Issue
執行結果錯誤請在 Github 發起 Issue。
