from django.shortcuts import redirect, render
from store.models import Product, ReviewRating, ProductGallery
from main.models import Partners, Menu, Banners
from django.contrib.auth.decorators import login_required
from dynamic_preferences.registries import global_preferences_registry
from django.urls import reverse


def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('-created_date')[:10]
    r_products = Product.objects.all().filter(is_available=True).order_by('-reviewrating')[:10]
    n_products = Product.objects.all().filter(is_available=True).order_by('-stock')[:6]
    partners = Partners.objects.all()
    menu = Menu.objects.all()
    banners = Banners.objects.all()
    # Get the product gallery
    product_gallery = ProductGallery.objects.all()
    # Get the reviews
    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': products,
        'r_products': r_products,
        'n_products': n_products,
        'reviews': reviews,
        'partners': partners,
        'menu': menu,
        'product_gallery': product_gallery,
        'banners': banners,
    }
    return render(request, 'home.html', context)


@login_required
def currency(request):
    if not request.user.is_superuser:
        return redirect(reverse("store"))
    
    gpm = global_preferences_registry.manager()
    if request.method == "POST":
        usd = request.POST.get("usd", None)
        print(usd)
        if usd:
            usd = usd.replace(",", ".")
            gpm["currency__usd"] = float(usd)
            print(gpm)
    
    context = {
        "usd": gpm["currency__usd"]
    }
    return render(request, "currency.html", context)