import os
import requests

def send_telegram(message):
    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    print(f"TOKEN existe: {bool(token)}")
    print(f"CHAT_ID: {chat_id}")

    response = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": message
        },
        timeout=30
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:")
    print(response.text)

def main():
    send_telegram("✅ Test desde GitHub Actions")

if __name__ == "__main__":
    main()