import json
import os
import time
from urllib.parse import urlparse, parse_qs, unquote

import requests
from bs4 import BeautifulSoup

SEARCH_TERMS = [
    "Google Pixel 10a",
    "Pixel 10a",
    "Google Pixel 10 A",
]

ALLOWED_DOMAINS = [
    "fravega.com",
    "megatone.net",
    "garbarino.com",
    "musimundo.com",
    "oncity.com",
    "naldo.com.ar",
    "celularesindustriales.com.ar",
    "heyshop.com.ar",
    "undertec.store",
    "start.com.ar",
    "diggit.com.ar",
    "spacegadget.com.ar",
    "compugarden.com.ar",
    "mercadolibre.com.ar",
]

STATE_FILE = "last_seen.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}


def load_state():
    if not os.path.exists(STATE_FILE):
        return {}

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()

            if not content:
                return {}

            return json.loads(content)

    except Exception:
        return {}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def send_telegram(message):
    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": message,
            "disable_web_page_preview": False,
        },
        timeout=30,
    )


def allowed_domain(url):
    hostname = urlparse(url).netloc.lower()

    for domain in ALLOWED_DOMAINS:
        if domain in hostname:
            return True

    return False


def extract_real_url(ddg_url):
    """
    Convierte:
    https://duckduckgo.com/l/?uddg=https%3A...
    en
    https://...
    """

    parsed = urlparse(ddg_url)

    qs = parse_qs(parsed.query)

    if "uddg" in qs:
        return unquote(qs["uddg"][0])

    return ddg_url


def search_duckduckgo(query):
    url = "https://html.duckduckgo.com/html/"

    response = requests.post(
        url,
        data={"q": query},
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    for link in soup.select("a.result__a"):
        href = link.get("href")

        if not href:
            continue

        real_url = extract_real_url(href)

        if not allowed_domain(real_url):
            continue

        title = link.get_text(" ", strip=True)

        results.append(
            {
                "title": title,
                "url": real_url,
            }
        )

    return results


def is_new_result(url, state):
    return url not in state


def main():
    state = load_state()

    found_new = []

    for term in SEARCH_TERMS:
        print(f"Searching: {term}")

        try:
            results = search_duckduckgo(term)

            for result in results:
                url = result["url"]

                if is_new_result(url, state):
                    state[url] = {
                        "title": result["title"],
                        "first_seen": int(time.time()),
                    }

                    found_new.append(result)

        except Exception as e:
            print(f"ERROR: {e}")

    if found_new:
        msg = [
            "📱 NUEVAS COINCIDENCIAS PARA GOOGLE PIXEL 10A",
            "",
        ]

        for item in found_new:
            msg.append(f"• {item['title']}")
            msg.append(item["url"])
            msg.append("")

        send_telegram("\n".join(msg))

    save_state(state)


if __name__ == "__main__":
    main()