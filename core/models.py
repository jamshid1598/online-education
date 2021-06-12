from django.db import models
from django.urls import reverse
from urllib.parse import urlparse, parse_qs
from sorl.thumbnail import ImageField
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _


class AboutUs(models.Model):
    title = models.CharField(_("Sarlavha"), max_length=300, blank=True, null=True, )

    image = models.ImageField(_('Rasm'), upload_to="about-us-images/%Y/%m/%d/", blank=True, null=True,)
    video = models.FileField(_('Video'), upload_to='about-us-videos/%Y/%m/%d/', blank=True, null=True,)

    description = models.TextField(_("Tavsif"))

    pub_date = models.DateTimeField(_("Yaratilgan Vaqti"), auto_now_add=True,)

    def __str__(self):
        return str(self.title) + " | " + str(self.pk)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    class Meta:
        ordering = ["pub_date"]
        verbose_name_plural = _("About Us")


