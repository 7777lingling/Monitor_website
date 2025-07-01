# 🎓 德霖五專續招監控系統

自動監控德霖科技大學五專續招頁面，當發現更新時自動發送Discord通知。

## ✨ 功能特色

- 🌐 **自動監控** - 定期檢查德霖五專續招頁面
- 🔍 **關鍵詞檢測** - 監控"114"年度相關公告
- 📤 **Discord通知** - 發現更新時自動發送通知
- 📝 **日誌記錄** - 詳細記錄所有檢查結果
- 🧹 **自動清理** - 定期清理超過7天的舊日誌
- ⏰ **定時執行** - 適合Windows Task Scheduler

## 🚀 使用方法

### 1. 安裝依賴
```bash
pip install beautifulsoup4 requests
```

### 2. 執行腳本
```bash
python monitor_admissions.py
```

### 3. 設置定時任務（Windows Task Scheduler）
1. 打開"任務計劃程序"
2. 創建基本任務
3. 設置執行頻率（建議每30分鐘）
4. 設置程序路徑：`python`
5. 設置參數：`E:\path\to\monitor_admissions.py`

## ⚙️ 配置說明

### 監控設置
- **目標網址**: 德霖五專續招頁面
- **關鍵詞**: "114"（學年度）
- **檢查間隔**: 可通過Task Scheduler調整

### Discord通知
- 自動發送包含更新內容和連結的通知
- 支持錯誤重試機制

### 日誌管理
- **日誌文件**: `log.txt`
- **保留天數**: 7天
- **自動清理**: 每次執行時自動清理舊日誌

## 📁 文件結構
```
Monitor_website/
├── monitor_admissions.py  # 主程序
├── log.txt               # 日誌文件（自動生成）
└── README.md            # 說明文件
```

## 🔧 自定義設置

### 修改關鍵詞
```python
KEYWORDS = ["114", "續招", "名額"]  # 添加更多關鍵詞
```

### 調整日誌保留天數
```python
LOG_RETENTION_DAYS = 7  # 改為其他天數
```

### 修改Discord Webhook
```python
DISCORD_WEBHOOK_URL = "你的Discord Webhook URL"
```

## 📊 日誌格式
```
[2024-01-15 14:30:00] 📡 正在檢查德霖五專續招頁面...
[2024-01-15 14:30:01] ❌ 尚未更新至 114 年度
```

## 🛠️ 故障排除

### 常見問題
1. **連接超時** - 檢查網絡連接
2. **Discord通知失敗** - 檢查Webhook URL是否正確
3. **編碼錯誤** - 確保系統支持UTF-8編碼

### 錯誤處理
- 所有錯誤都會記錄到日誌文件
- 網絡錯誤會自動重試
- Discord發送失敗不會影響監控功能

## 📈 更新日誌

- **v1.0** - 初始版本，基本監控功能
- **v1.1** - 添加Discord通知功能
- **v1.2** - 添加日誌自動清理功能

## 🤝 貢獻

歡迎提交Issue和Pull Request來改進這個項目！

## 📄 授權

MIT License 