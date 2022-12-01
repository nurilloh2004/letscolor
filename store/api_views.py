from django.contrib.contenttypes.models import ContentType
import requests
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from category.models import *
from .serializers import *
from .models import *
import json
from django.core import files
from io import BytesIO


def translate_text(text, from_lang, to_lang):
    from googletrans import Translator
    translator = Translator()
    result = translator.translate(str(text), src=from_lang, dest=to_lang)
    return result.text


class ProductViewSet(ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	tm = ContentType.objects.get(app_label="store", model="producttranslation").model_class()

	def create(self, request, *args, **kwargs):
		data = request.data

		category_name = data["category"].strip()
		category = Category.objects.filter(translations__name__contains=category_name)
		if category.exists():
			category = category.first()
		else:
			category = Category.objects.all().first()

		product = Product(
			slug=data["slug"],
			old_price=data["price"],
			original_price=data["price"],
			currency="uzs",
			stock=1000,
			category=category
		)
		product.save()

		if data.get("photo", None):
			url = data["photo"]
			resp = requests.get(url)
			if resp.status_code != requests.codes.ok:
				pass
			else:
				fp = BytesIO()
				fp.write(resp.content)
				filename = url.split("/")[-1]
				product.images.save(filename, files.File(fp))

		self.tm(
			product_name=data["title"],
			description=data["description"],
			language_code="ru",
			master_id=product.id
		).save()

		self.tm(
			product_name=translate_text(data["title"], "ru", "uz"),
			description=translate_text(data["description"], "ru", "uz"),
			language_code="uz",
			master_id=product.id
		).save()

		self.tm(
			product_name=translate_text(data["title"], "ru", "en"),
			description=translate_text(data["description"], "ru", "en"),
			language_code="en",
			master_id=product.id
		).save()

		return Response(status=status.HTTP_200_OK)


class CategoryViewSet(ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	tm = ContentType.objects.get(app_label="category", model="categorytranslation").model_class()
	
	def create(self, request, *args, **kwargs):
		data = request.data
		translations = json.loads(data["translations"])
		category = Category(slug=data["slug"])
		if data.get("icon", None):
			category.icon = data["icon"]
		if data.get("parent", None):
			parent = Category.objects.get(id=data["parent"])
			category.parent = parent
		category.save()
		for t in translations.keys():
			print(t, translations[t])
			tmo = self.tm(name=translations[t]["name"], master_id=category.id, language_code=t)
			tmo.save()
		s = self.serializer_class(category)
		print(s.data)
		return Response(s.data, status=status.HTTP_200_OK)

class ProductGalleryViewSet(ModelViewSet):
	queryset = ProductGallery.objects.all()
	serializer_class = ProductGallerySerializer