from django.db import models
from django.urls import reverse

# from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from urllib.parse import urlparse, parse_qs
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Category(models.Model):
    name = models.CharField(_('Category'), max_length=200, unique=True,)
    image = ImageField(_('Category Image'), upload_to="category/%Y/%m/%d/", blank=True, null=True,)

    class Meta:
        ordering = ['name']
        verbose_name = _('Primary Category')
        verbose_name_plural = _('Primary Categories')

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url




class SubCategory(models.Model):
    primary_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='primary_category', verbose_name=_("Primary Category"))
    name = models.CharField(_("Category"), max_length=200, unique=True, )
    slug = models.SlugField(max_length=350, null=True)
    image = ImageField(_("Category Image"), upload_to="category/%Y/%m/%d/", blank=True, null=True,)

    price    = models.BigIntegerField(_('Price'), blank=True, null=True, validators=(MinValueValidator(1), MaxValueValidator(100000000),))
    discount = models.BigIntegerField(_('Discount'), blank=True, null=True, validators=(MinValueValidator(1), MaxValueValidator(100000000),))

    paid = models.BooleanField(_("Paid"), default=True, )
    free = models.BooleanField(_("Free"), default=False, )

    class Meta:
        ordering = ['name']
        verbose_name = _('Sub-Category')
        verbose_name_plural = _('Sub-Categories')

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Lesson(models.Model):
    # video_url  = models.URLField(_("Video Url"), unique=True, blank=True, null=True, )
    video_file = models.FileField(_("Video File"), upload_to='videos/%Y/%m/%d/', blank=True, null=True, )
    image = ImageField(_("Video Image"), upload_to="video-image/%Y/%m/%d/",)

    name = models.CharField(_("Lesson Name"), max_length=300,)
    slug = models.SlugField(max_length=320)

    short_info  = models.CharField(_("Short Info About Lesson"), max_length=500,)
    body = models.TextField(_('Lesson Body'))

    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='sub_category', verbose_name=_('Category'))
    downloaded = models.IntegerField(_("Downloaded"), default=0, )

    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    cart_field = models.BooleanField(default=False)  # this field is only changed through cart page

    class Meta:
        ordering = ['name', 'published_at', 'updated_at']
        verbose_name = _('Lesson')
        verbose_name_plural = _('Lessons')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def is_updated(self):
        if self.published_at == self.updated_at:
            return self.published_at
        else:
            self.updated_at

    # def extract_video_id(self):
        # Examples:
        # - http://youtu.be/SA2iWivDJiE
        # - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
        # - http://www.youtube.com/embed/SA2iWivDJiE
        # - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
        # if self.video_url:
        #     query = urlparse(self.video_url)
        #     if query.hostname == 'youtu.be': return query.path[1:]
        #     if query.hostname in {'www.youtube.com', 'youtube.com'}:
        #         if query.path == '/watch': return parse_qs(query.query)['v'][0]
        #         if query.path[:7] == '/embed/': return query.path.split('/')[2]
        #         if query.path[:3] == '/v/': return query.path.split('/')[2]
        # # fail?
        # return None

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
