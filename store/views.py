from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating, ProductGallery
from category.models import Category, Brand
from carts.models import CartItem
from django.db.models import Q

from django.utils.translation import gettext_lazy as _

from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct


def store(request, category_slug=None):
    category = None
    if category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category_id__in=[item.id for item in category.get_descendants(include_self=True)], is_available=True).order_by('-created_date')
    else:
        products = Product.objects.all()

    if request.GET.get:
        price_r = {}
        if request.GET.get('lower') and request.GET.get('upper'):
            price_r['original_price__gt'] = request.GET.get('lower')
            price_r['original_price__lt'] = request.GET.get('upper')
            products = products.filter(is_available=True, **price_r).order_by('-created_date')

    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()

    r_products = Product.objects.all().filter(is_available=True).order_by('created_date')[:10]

    context = {
        'products': paged_products,
        'product_count': product_count,
        'r_products': r_products,
        "category_slug": category_slug,
        "cat": category
    }
    return render(request, 'store/store.html', context)


def store_by_brand(request, brand_slug):
    brand = get_object_or_404(Brand, slug=brand_slug)
    # price__lte=50, price__gte=50
    products = Product.objects.filter(
        brand=brand, is_available=True).order_by('-created_date')
    r_products = Product.objects.all().filter(is_available=True).order_by('created_date')[:10]

    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'r_products': r_products,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, product_slug):
    try:
        single_product = Product.objects.get(slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    # Get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    # Get the related product
    r_products = Product.objects.all().filter(is_available=True).order_by('-reviewrating')[:10]

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
        'r_products': r_products,
    }
    return render(request, 'store/product_detail.html', context)


def product_detail_by_brand(request, brand_slug, product_slug):
    try:
        single_product = Product.objects.get(brand__slug=brand_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    # Get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    # Get the related product
    r_products = Product.objects.all().filter(is_available=True).order_by('-reviewrating')[:10]

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
        'r_products': r_products,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(translations__description__icontains=keyword) | Q(translations__product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, _('Thank you! Your review has been updated.'))
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, _('Thank you! Your review has been submitted.'))
                return redirect(url)
