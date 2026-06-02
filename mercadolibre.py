import re
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}


def parse_price(text):
    digits = re.sub(r"[^\d]", "", text)

    if not digits:
        return None

    return int(digits)


def search_mercadolibre():
    url = (
        "https://listado.mercadolibre.com.ar/"
        "celulares-telefonos/celulares-smartphones/google/google-pixel-10a_OrderId_PRICE_NoIndex_True_SHIPPING*ORIGIN_10215068#unapplied_filter_id%3Dinstallments%26unapplied_filter_name%3DCuotas%26unapplied_value_id%3Dgood_financing%26unapplied_value_name%3DMejor+precio+en+cuotas%26unapplied_autoselect%3Dfalse"
    )

    print("Consultando MercadoLibre")

    r = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )

    print("STATUS:", r.status_code)

    soup = BeautifulSoup(
        r.text,
        "html.parser"
    )

    results = []

    cards = soup.select(
        "li.ui-search-layout__item"
    )

    print(
        "PUBLICACIONES:",
        len(cards)  
    )

    for card in cards[:20]:

        title_el = card.select_one(
            ".poly-component__title"
        )

        price_el = card.select_one(
            ".andes-money-amount__fraction"
        )

        link_el = card.select_one(
            "a"
        )

        if (
            not title_el
            or not price_el
            or not link_el
        ):
            continue

        title = title_el.get_text(
            " ",
            strip=True
        )

        price = parse_price(
            price_el.get_text(
                " ",
                strip=True
            )
        )

        url = link_el.get("href")

        title_lower = title.lower()

        if any(
            word in title_lower
            for word in [
                "importado",
                "internacional",
                "usa",
                "us version",
            ]
        ):
            continue

        results.append(
            {
                "store": "MercadoLibre",
                "title": title,
                "price": price,
                "url": url,
            }
        )

    return results