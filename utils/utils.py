def price_format(value):
    return f'$ {value:.2f}'.replace('.', ',')


def cart_total_qty(cart):
    return sum([item['quantity'] for item in cart.values()])


def cart_totals(cart):
    return sum(
        [
            item.get('promo_quantitative_price')
            if item.get('promo_quantitative_price')
            else item.get('quantitative_price')
            for item
            in cart.values()
        ]
    )
