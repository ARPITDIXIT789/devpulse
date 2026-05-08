import os
import time

import requests

HEALTH_URL = os.getenv("HEALTH_URL", "http://localhost:5000/health")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "30"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "5"))
ALERT_COOLDOWN_SECONDS = int(os.getenv("ALERT_COOLDOWN_SECONDS", "300"))
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")


def check_health():
    try:
        response = requests.get(HEALTH_URL, timeout=REQUEST_TIMEOUT)
        return response.status_code == 200
    except requests.RequestException:
        return False


def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
        return response.status_code == 200
    except requests.RequestException:
        return False


if __name__ == "__main__":
    unhealthy_since = None
    last_alert_at = 0
    was_healthy = True

    while True:
        now = int(time.time())
        healthy = check_health()
        print(f"Health check [{HEALTH_URL}] => {'OK' if healthy else 'FAIL'}")

        if healthy:
            if not was_healthy:
                downtime_seconds = 0 if unhealthy_since is None else now - unhealthy_since
                send_telegram_message(
                    f"DevPulse recovered. Health endpoint is UP again. Downtime: {downtime_seconds}s"
                )
            unhealthy_since = None
            was_healthy = True
        else:
            if unhealthy_since is None:
                unhealthy_since = now
            if was_healthy or (now - last_alert_at) >= ALERT_COOLDOWN_SECONDS:
                down_for = now - unhealthy_since
                sent = send_telegram_message(
                    f"DevPulse alert. Health endpoint DOWN for {down_for}s. URL: {HEALTH_URL}"
                )
                if sent:
                    last_alert_at = now
            was_healthy = False

        time.sleep(CHECK_INTERVAL)
