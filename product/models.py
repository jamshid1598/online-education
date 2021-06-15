from django.db import models
from django.urls import reverse

# from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from urllib.parse import urlparse, parse_qs
from django.template.defaultfilters import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model
User = get_user_model()


from users.models import Teacher

# Create your models here.
class Category(models.Model):
    name  = models.CharField(_('Category'), max_length=200, unique=True,)
    image = ImageField(_('Category Image'), upload_to="category/%Y/%m/%d/", blank=True, null=True,)

    class Meta:
        ordering            = ['name']
        verbose_name        = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url




class Subject(models.Model):
    category     = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_subject', verbose_name=_("Category"))
    teacher      = models.ForeignKey(Teacher, blank=True, null=True, on_delete=models.SET_NULL, related_name='subject_teacher', verbose_name=_("Teacher"))
    name         = models.CharField(_("Subject Name"), max_length=200, unique=True, )
    slug         = models.SlugField(max_length=350, null=True)
    image        = ImageField(_("Subject Image"), upload_to="subject/%Y/%m/%d/", blank=True, null=True,)

    short_info   = models.TextField(_("Short Info"), null=True)

    price        = models.BigIntegerField(_('Price'), blank=True, null=True, validators=(MinValueValidator(1), MaxValueValidator(100000000),))
    discount     = models.BigIntegerField(_('Discount'), blank=True, null=True, validators=(MinValueValidator(1), MaxValueValidator(100000000),))

    downloaded   = models.IntegerField(_("Downloaded"), default=0, )

    free         = models.BooleanField(_("Free"), default=False, )

    like         = models.ManyToManyField(User, blank=True, null=True, related_name="user_like",)

    published_at = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering            = ['name']
        verbose_name        = _('Subject')
        verbose_name_plural = _('Subjects')

    def __str__(self):
        return self.name

    @property
    def discount_per(self):
        if self.discount:
            sub = self.price - self.discount
            discount_per = (sub/self.price)*100
            return discount_per
        else:
            return None 

    @property
    def is_updated(self):
        if self.published_at == self.updated_at:
            return self.published_at
        else:
            return self.updated_at

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Lesson(models.Model):
    subject      = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_lesson', verbose_name=_('Subject'))

    video_file   = models.FileField(_("Video File"), upload_to='videos/%Y/%m/%d/',)
    image        = ImageField(_("Video Image"), upload_to="video-image/%Y/%m/%d/",)

    name         = models.CharField(_("Lesson Name"), max_length=300,)
    slug         = models.SlugField(max_length=320)

    lesson_series= models.IntegerField(_("Lesson Series"), default=1,)

    body         = models.TextField(_('Lesson Body'))

    published_at = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    # cart_field = models.BooleanField(default=False)  # this field is only changed through cart page

    class Meta:
        ordering            = ['name', 'published_at', 'updated_at']
        verbose_name        = _('Lesson')
        verbose_name_plural = _('Lessons')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if Lesson.objects.filter(subject=self.subject) and self.published_at == self.updated_at:
            lessons = Lesson.objects.filter(subject=self.subject).order_by("lesson_series")
            lesson = lessons.last()
            self.lesson_series = lesson.lesson_series + 1
        super().save(*args, **kwargs)

    @property
    def is_updated(self):
        if self.published_at == self.updated_at:
            return self.published_at
        else:
            return self.updated_at


    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
