from .models import Category, Brand


def menu_links(request):
    categories = Category.objects.all()
    return {"categories": categories}


def brands(request):
    brands = Brand.objects.all()
    return {"brands": brands}
