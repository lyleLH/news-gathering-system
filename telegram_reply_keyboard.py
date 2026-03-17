import os
import sys
import urllib.request
import urllib.parse
import json

# 1. 获取 Bot Token (这里假设用户已经配置了环境变量，或者我们先用一个占位符提示用户)
bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
if not bot_token:
    print("Error: TELEGRAM_BOT_TOKEN environment variable is not set.")
    print("Please set it using: export TELEGRAM_BOT_TOKEN='your_token'")
    sys.exit(1)

# 2. 目标 Chat ID (从上下文中获取)
chat_id = "324968912"

# 3. 构造带有 Reply Keyboard 的消息
url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
data = {
    "chat_id": chat_id,
    "text": "好的，您选择了 **C (多步表单/对话)**。\n\n我已经为您开启了自定义的回复键盘！请看您屏幕下方的输入区域，它现在应该变成了几个快捷选项。\n\n请问您接下来想查看哪个话题的热点？",
    "parse_mode": "Markdown",
    "reply_markup": {
        "keyboard": [
            [{"text": "🚀 OpenCLI 最新动态"}],
            [{"text": "🤖 nanobot 极简 AI 助手"}, {"text": "🏭 DarkVision Technologies"}],
            [{"text": "❌ 关闭快捷键盘"}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }
}

# 4. 发送请求
req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        if result.get("ok"):
            print("Successfully sent message with Reply Keyboard!")
        else:
            print(f"Telegram API Error: {result}")
except Exception as e:
    print(f"HTTP Request Error: {e}")
