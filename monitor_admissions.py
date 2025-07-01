import requests
from bs4 import BeautifulSoup
import time
import sys

# 🌐 德霖五專續招頁面
URL = "https://registry.hdut.edu.tw/files/11-1018-443.php?Lang=zh-tw"
KEYWORDS = ["114"]

# ✅ Discord Webhook
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1389509864585170964/zu_LGgoDsVhTCwtdqcngMz6NJ0L505xJX3b4BtNJ0n7YntNvRstwys9YhNBxfIaZ2jtK"

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
check_site()
