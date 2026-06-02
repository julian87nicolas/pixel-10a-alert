PRICE_LIMIT = 900000
GOOD_PRICE = 1000000


def get_deals(results):
    """
    Precio menor a 900k
    """

    return [
        item
        for item in results
        if item.get("price")
        and item["price"] < PRICE_LIMIT
    ]


def get_good_prices(results):
    """
    Precio menor a 1M
    """

    return [
        item
        for item in results
        if item.get("price")
        and item["price"] < GOOD_PRICE
    ]


def get_top3_cheapest(results):
    """
    Top 3 más baratos
    """

    priced = [
        item
        for item in results
        if item.get("price")
    ]

    priced.sort(
        key=lambda x: x["price"]
    )

    return priced[:3]