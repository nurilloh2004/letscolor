from rest_framework.viewsets import ModelViewSet
from .serializers import *
from category.models import *
from .models import *


class ProductViewSet(ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer


class CategoryViewSet(ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	
	def create(self, request, *args, **kwargs):
		print(request.data)
		return super(CategoryViewSet, self).create(request, *args, **kwargs)

class ProductGalleryViewSet(ModelViewSet):
	queryset = ProductGallery.objects.all()
	serializer_class = ProductGallerySerializer
