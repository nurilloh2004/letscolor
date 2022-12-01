from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import *
from carts.models import *
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from greatkart.utils import get_current_utc
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .utils import *

from clickuz import ClickUz
from paycomuz import Paycom

paycom = Paycom()


def payments(request):
    body = json.loads(request.body)

    ip = get_client_ip(request)

    if request.user.is_authenticated:
        order = Order.objects.get(
            user=request.user,
            is_ordered=False,
            order_number=body['orderID']
        )
    else:
        order = Order.objects.get(
            ip=ip,
            is_ordered=False,
            order_number=body['orderID']
        )

    payment = Payment(
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status=body['status'],
    )
    if request.user.is_authenticated:
        payment.user = request.user
    else:
        payment.user = ip
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    cart_items = CartItem.objects.filter(is_active=True)
    if request.user.is_authenticated:
        cart_items = cart_items.filter(user=request.user)
    else:
        cart_items = cart_items.filter(ip=ip)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        if item.reduced_price:
            orderproduct.product_price = item.reduced_price
        else:
            orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    cart_items = CartItem.objects.filter(is_active=True)
    if request.user.is_authenticated:
        cart_items = cart_items.filter(user=request.user)
    else:
        cart_items = cart_items.filter(ip=ip)
    
    cart_items.delete()
    
    try:
        mail_subject = 'Thank you for your order!'
        message = render_to_string('orders/order_recieved_email.html', {
            'user': request.user,
            'order': order,
        })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
    except:
        pass

    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)


def place_order(request, total=0, quantity=0, ):
    context = {}

    ip = get_client_ip(request)

    cart_items = CartItem.objects.filter(is_active=True)
    if request.user.is_authenticated:
        cart_items = cart_items.filter(user=request.user)
    else:
        cart_items = cart_items.filter(ip=ip)
    
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

        if cart_item.reduced_price:
            total += cart_item.reduced_price
        else:
            total += cart_item.product.price

    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()

            if request.user.is_authenticated:
                data.user = request.user
            else:
                data.ip = ip

            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.save()

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")

            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            for cart_item in cart_items:
                orderproduct = OrderProduct()
                orderproduct.order = data
                orderproduct.product = cart_item.product
                orderproduct.quantity = cart_item.quantity

                if cart_item.reduced_price:
                    orderproduct.product_price = cart_item.reduced_price
                else:
                    orderproduct.product_price = cart_item.product.price

                orderproduct.save()

                for var in cart_item.variations.all():
                    orderproduct.variations.add(var)

            order = Order.objects.filter(
                is_ordered=False,
                order_number=order_number
            )
            if request.user.is_authenticated:
                order = order.filter(user=request.user)
            else:
                order = order.filter(ip=ip)
            
            order = order.first()

            context["order"] = order
            context["cart_items"] = cart_items
            context["total"] = order.total_price
            context["tax"] = tax
            context["grand_total"] = order.total_price
            context["click_url"] = ClickUz.generate_url(order_id=order.id, amount=order.total_price)
            context["payme_url"] = paycom.create_initialization(amount=order.total_price * 100, order_id=str(data.id), return_url="https://letscolor.uz/store/")
            return render(request, 'orders/payments.html', context)

        elif request.POST.get("coupon-code", None):
            coupon_code = request.POST.get("coupon-code", None)
            coupons = Coupon.objects.filter(code=coupon_code, is_used=False)
            if not coupons.exists():
                messages.success(request, _("The coupon code doesn't exist"))
            else:
                coupon = coupons.first()
                if get_current_utc() > coupon.expires_in:
                    messages.success(request, _("The coupon code expired."))
                else:
                    for cartitem in cart_items:
                        categories = []
                        for category in coupon.category.all():
                            categories.append(category.name)

                        category = cartitem.product.category.name

                        if category in categories:
                            if cartitem.reduced_price:
                                cartitem.reduced_price = (cartitem.reduced_price * (100 - coupon.stock)) / 100
                            else:
                                cartitem.reduced_price = (cartitem.product.price * (100 - coupon.stock)) / 100
                            cartitem.save()
                            coupon.is_used = True
                            coupon.save()
                            print(cartitem.reduced_price)


            cart_items = CartItem.objects.filter(is_active=True)
            if request.user.is_authenticated:
                cart_items = cart_items.filter(user=request.user)
            else:
                cart_items = cart_items.filter(ip=ip)
            
            order = Order.objects.filter(is_ordered=False)
            if request.user.is_authenticated:
                order = order.filter(user=request.user)
            else:
                order = order.filter(ip=ip)
            order = order.order_by("-id").first()

            grand_total = 0
            for cart_item in cart_items:
                if cart_item.reduced_price > 0:
                    total = (cart_item.reduced_price * cart_item.quantity)
                    quantity += cart_item.quantity
                else:
                    total = (cart_item.product.price * cart_item.quantity)
                    quantity += cart_item.quantity

            grand_total = total

            context["order"] = order
            context["cart_items"] = cart_items
            context["total"] = order.total_price
            context["tax"] = tax
            context["grand_total"] = order.total_price
            context["click_url"] = ClickUz.generate_url(order_id=order.id, amount=order.total_price)
            context["payme_url"] = paycom.create_initialization(amount=order.total_price * 100, order_id=str(order.id), return_url="https://letscolor.uz/store/")
            return render(request, 'orders/payments.html', context)
    else:
        return render(request, 'orders/payments.html', context)


def order_complete(request):
    order_number = request.GET.get('order_number', None)
    transID = request.GET.get('payment_id', None)
    ip = get_client_ip(request)

    if order_number and transID:
        cart_items = CartItem.objects.filter(is_active=True)
        if request.user.is_authenticated:
            cart_items = cart_items.filter(user=request.user)
        else:
            cart_items = cart_items.filter(ip=ip)

        cart_items.delete()

        try:
            order = Order.objects.get(order_number=order_number, is_ordered=True)
            ordered_products = OrderProduct.objects.filter(order_id=order.id)

            admins = BotAdmin.objects.filter(is_active=True)
            for admin in admins:
                text = generate_order_text(order)
                res = send_message(text, admin.user_id)

            subtotal = 0
            for i in ordered_products:
                subtotal += i.product_price * i.quantity

            payment = Payment.objects.get(payment_id=transID)

            context = {
                'order': order,
                'ordered_products': ordered_products,
                'order_number': order.order_number,
                'transID': payment.payment_id,
                'payment': payment,
                'subtotal': subtotal,
            }
            return render(request, 'orders/order_complete.html', context)
        except (Payment.DoesNotExist, Order.DoesNotExist):
            return redirect('home')
    elif order_number:
        cart_items = CartItem.objects.filter(is_active=True)
        if request.user.is_authenticated:
            cart_items = cart_items.filter(user=request.user)
        else:
            cart_items = cart_items.filter(ip=ip)
        
        cart_items.delete()
        order = Order.objects.get(id=order_number)
        order.status = "Accepted"
        order.is_ordered = True
        order.save()
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        admins = BotAdmin.objects.filter(is_active=True)
        for admin in admins:
            text = generate_order_text(order)
            res = send_message(text, admin.user_id)
        
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html')
    else:
        return render(request, 'orders/order_complete.html')


def order_status_check(request):
    data = request.GET

    order_id = data.get("order_id", 0)

    try:
        order = Order.objects.get(id=order_id)
    except:
        return JsonResponse({"status": False})
    
    return JsonResponse({
        "status": order.status == "Completed"
    })