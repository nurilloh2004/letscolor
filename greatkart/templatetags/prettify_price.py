from django import template

register = template.Library()

@register.simple_tag
def prettify_price(price):
    price = str(price)
    if price.isalpha():
        return price
    
    try:
        price = int(float(price))
    except Exception as e:
        print(e)
        return price

    price = intWithCommas(price)

    return price


def intWithCommas(x):
    if x < 0:
        return "-" + intWithCommas(-x)
    result = ""
    x = int(x)
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = " %03d%s" % (r, result)
    return "%d%s" % (x, result)