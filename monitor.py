from mercadolibre import search_mercadolibre
from price_analyzer import (
    get_deals,
    get_good_prices,
    get_top3_cheapest,
)
from telegram_bot import send_telegram


def main():
    print("===================================")
    print("PIXEL 10A MONITOR")
    print("===================================")

    results = []

    try:
        results.extend(search_mercadolibre())
    except Exception as e:
        print("ERROR MercadoLibre:", e)

    print()
    print(f"TOTAL RESULTADOS: {len(results)}")

    for item in results:
        print(item)

    deals = get_deals(results)
    good_prices = get_good_prices(results)
    cheapest = get_top3_cheapest(results)

    if deals:
        msg = [
            "🚨 PIXEL 10A EN OFERTA",
            ""
        ]

        for item in deals:
            msg.append(
                f"${item['price']:,}".replace(",", ".")
            )
            msg.append(item["store"])
            msg.append(item["url"])
            msg.append("")

        send_telegram("\n".join(msg))

    elif good_prices:
        msg = [
            "🟡 PIXEL 10A A BUEN PRECIO",
            ""
        ]

        for item in good_prices:
            msg.append(
                f"${item['price']:,}".replace(",", ".")
            )
            msg.append(item["store"])
            msg.append(item["url"])
            msg.append("")

        send_telegram("\n".join(msg))

    elif cheapest:
        msg = [
            "📊 ESTADO DEL MONITOREO",
            "",
            "No se encontraron equipos por debajo de $1.000.000",
            "",
            "Top 3 precios:",
            ""
        ]

        for idx, item in enumerate(cheapest, start=1):
            msg.append(
                f"{idx}. ${item['price']:,}".replace(",", ".")
            )
            msg.append(item["store"])
            msg.append(item["url"])
            msg.append("")

        send_telegram("\n".join(msg))

    else:
        print("No se encontraron publicaciones")


if __name__ == "__main__":
    main()