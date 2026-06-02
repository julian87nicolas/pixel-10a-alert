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
        print("INFO: last_seen.json no existe")
        return {}

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()

            if not content:
                print("INFO: last_seen.json vacío")
                return {}

            state = json.loads(content)
            print(f"INFO: {len(state)} URLs cargadas")
            return state

    except Exception as e:
        print(f"ERROR cargando estado: {e}")
        return {}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            state,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"INFO: guardadas {len(state)} URLs")


def send_telegram(message):
    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    response = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": message,
            "disable_web_page_preview": False,
        },
        timeout=30,
    )

    print("TELEGRAM STATUS:", response.status_code)
    print("TELEGRAM RESPONSE:", response.text)


def allowed_domain(url):
    hostname = urlparse(url).netloc.lower()

    for domain in ALLOWED_DOMAINS:
        if domain in hostname:
            return True

    return False


def extract_real_url(ddg_url):
    parsed = urlparse(ddg_url)

    qs = parse_qs(parsed.query)

    if "uddg" in qs:
        return unquote(qs["uddg"][0])

    return ddg_url


def search_duckduckgo(query):
    print(f"\n===== BUSCANDO: {query} =====")

    response = requests.post(
        "https://html.duckduckgo.com/html/",
        data={"q": query},
        headers=HEADERS,
        timeout=30,
    )

    print("DDG STATUS:", response.status_code)

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    links = soup.select("a.result__a")

    print(f"RESULTADOS DDG: {len(links)}")

    for link in links:
        href = link.get("href")

        if not href:
            continue

        real_url = extract_real_url(href)

        print("ENCONTRADO:", real_url)

        if not allowed_domain(real_url):
            print("RECHAZADO")
            continue

        print("ACEPTADO")

        title = link.get_text(" ", strip=True)

        print(f"ACEPTADO: {title}")
        print(f"URL: {real_url}")

        results.append({
            "title": title,
            "url": real_url,
        })

    print(f"RESULTADOS FILTRADOS: {len(results)}")

    return results


def main():
    print("===================================")
    print("PIXEL 10A MONITOR")
    print("===================================")

    state = load_state()

    found_new = []

    for term in SEARCH_TERMS:
        try:
            results = search_duckduckgo(term)

            for result in results:
                url = result["url"]

                if url not in state:
                    print("NUEVA URL:", url)

                    state[url] = {
                        "title": result["title"],
                        "first_seen": int(time.time()),
                    }

                    found_new.append(result)

        except Exception as e:
            print("ERROR:", e)

    print(f"\nNUEVOS RESULTADOS: {len(found_new)}")

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
    else:
        print("SIN NOVEDADES")

    save_state(state)


if __name__ == "__main__":
    main()