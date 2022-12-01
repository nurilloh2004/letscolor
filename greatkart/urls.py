from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from .paycom import *
from .click import *
from store.api_views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("products", ProductViewSet, basename="products")
router.register("categories", CategoryViewSet, basename="categories")
router.register("gallery", ProductGalleryViewSet, basename="gallaries")


urlpatterns = i18n_patterns(
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('securelogin/', admin.site.urls),
    path("currency/", views.currency),
    path('', views.home, name='home'),
    path('store/', include('store.urls')),
    path('cart/', include('carts.urls')),
    path('accounts/', include('accounts.urls')),
    path('main/', include('main.urls')),
    # ORDERS
    path('orders/', include('orders.urls')),
    # CKEDITOR
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
)


urlpatterns += [
    path('rosetta/', include('rosetta.urls')),
    path('paycom/', PaymeView.as_view()),
    path('click/', ClickView.as_view()),
    path("api/", include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
