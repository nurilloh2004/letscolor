from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


# Create your models here.

class Partners(models.Model):
    image = models.ImageField(upload_to='store/partners', verbose_name=_('Image'))

    def __unicode__(self):
        return self.image

    class Meta:
        verbose_name = _('Partner')
        verbose_name_plural = _('Partners')


class Menu(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=155, verbose_name=_('Title'))
    )
    icon = models.CharField(max_length=100, verbose_name=_('Icon'))
    link = models.CharField(max_length=155, blank=True, verbose_name=_('Link'))

    def __str__(self):
        return self.safe_translation_getter('title')

    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menu')


class About(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=155, verbose_name=_('Title')),
        content=RichTextField(blank=True, verbose_name=_('Content'))
    )

    def __str__(self):
        return self.safe_translation_getter('title')

    class Meta:
        verbose_name = _('About')
        verbose_name_plural = _("About")


class Banners(models.Model):
    image = models.ImageField(upload_to='images/banners', blank=False, verbose_name=_('Image'))

    def __unicode__(self):
        return self.image

    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')
