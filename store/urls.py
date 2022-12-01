from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('product/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('brand/<slug:brand_slug>/', views.store_by_brand, name='store_by_brands'),
    path('brand/<slug:brand_slug>/<slug:product_slug>/', views.product_detail_by_brand, name='product_detail_by_brand'),
]



















