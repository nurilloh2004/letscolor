import requests


def send_message(text, user_id):
    data = {
        "chat_id": user_id,
        "text": text,
        "parse_mode": "html",
    }
    return requests.post("https://api.telegram.org/bot2117541852:AAHQLTxBfEi1Z9KPCZeGUQiKr15KEx7iWO8/sendMessage", json=data)


def generate_order_text(order):
    text = f"Buyurtma raqami: {order.id}\n\n"
    for op in order.items.all():
        text += """{} {}so'm x {} = {}so'm\n\n""".format(op.product.product_name, op.product_price, op.quantity, op.product_price * op.quantity)
    text += "\nJami: {}so'm".format(order.total_price)
    text += "\n\nManzil: {} {} {}".format(order.state or "", order.city or "", order.full_address())
    text += "\n\nTo'liq ism: {}".format(order.full_name())
    print(text)
    return text

def generate_contact_text(name, message):
    text = f"Telefon Nomeri: {name}\n"
    text += f"\nText: {message}"
    return text

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip