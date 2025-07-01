import requests
from bs4 import BeautifulSoup
import time
import sys
import os
from datetime import datetime, timedelta

# 🌐 德霖五專續招頁面
URL = "https://registry.hdut.edu.tw/files/11-1018-443.php?Lang=zh-tw"
KEYWORDS = ["114"]

# ✅ Discord Webhook
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1389509864585170964/zu_LGgoDsVhTCwtdqcngMz6NJ0L505xJX3b4BtNJ0n7YntNvRstwys9YhNBxfIaZ2jtK"

# 📅 日志清理设置
LOG_FILE = "log.txt"
LOG_RETENTION_DAYS = 7  # 保留7天的日志

def send_discord_message(content):
    data = {"content": content}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code in [200, 204]:
            print("📤 Discord 通知成功")
            return True
        else:
            print(f"⚠️ Discord 傳送失敗：{response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"⚠️ 發送過程發生錯誤：{e}")
        return False

def clean_old_logs():
    """清理超过保留天数的旧日志"""
    try:
        if not os.path.exists(LOG_FILE):
            return
        
        # 读取所有日志行
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            return
        
        # 计算截止时间
        cutoff_time = datetime.now() - timedelta(days=LOG_RETENTION_DAYS)
        cutoff_str = cutoff_time.strftime('%Y-%m-%d')
        
        # 过滤保留的日志行
        kept_lines = []
        for line in lines:
            # 检查日志行是否包含时间戳且在保留期内
            if '[' in line and ']' in line:
                timestamp_part = line.split('[')[1].split(']')[0]
                log_date = timestamp_part.split(' ')[0]  # 提取日期部分
                if log_date >= cutoff_str:
                    kept_lines.append(line)
            else:
                # 没有时间戳的行也保留
                kept_lines.append(line)
        
        # 重写日志文件
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.writelines(kept_lines)
        
        cleaned_count = len(lines) - len(kept_lines)
        if cleaned_count > 0:
            print(f"🧹 已清理 {cleaned_count} 条旧日志记录")
            
    except Exception as e:
        print(f"⚠️ 清理日志时发生错误：{e}")

def check_site():
    try:
        response = requests.get(URL, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        paragraphs = soup.find_all('p', align="center")
        for p in paragraphs:
            text = p.get_text(strip=True)
            if any(kw in text for kw in KEYWORDS):
                log = f"✅ 發現段落：{text}\n"
                print(log.strip())

                # 嘗試發送通知
                success = send_discord_message(
                    f"🎓 德霖五專續招更新！\n{text}\n🔗 {URL}"
                )

                # 寫入 log
                with open("log.txt", "a", encoding="utf-8") as f:
                    f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {log}")

                # 成功才退出
                if success:
                    sys.exit(0)
                else:
                    break
        else:
            log = "❌ 尚未更新至 114 年度\n"
    except Exception as e:
        log = f"❌ 發生錯誤：{e}\n"

    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {log}")

# ✅ 單次執行（for Task Scheduler）
print("📡 正在檢查德霖五專續招頁面...")

# 🧹 清理旧日志
clean_old_logs()

# 🔍 检查网站
check_site()
