import re
import json
import requests

PRICE_LIMIT = 900000

SEARCH_URL = (
    "https://www.google.com/search?q="
    "\"Google+Pixel+10a\"+Argentina"
)

BLACKLIST = [
    "mercadolibre",
    "tiendamia",
    "amazon",
    "ebay",
    "aliexpress"
]

r = requests.get(
    SEARCH_URL,
    headers={
        "User-Agent":
        "Mozilla/5.0"
    }
)

html = r.text

prices = re.findall(
    r'(\d{3,4}\.\d{3})',
    html
)

for p in prices:
    value = int(p.replace(".", ""))

    if value < PRICE_LIMIT:
        print(
            f"ALERTA: Pixel 10a encontrado "
            f"a ${value:,}"
        )