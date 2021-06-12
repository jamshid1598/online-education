from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models
from sorl.thumbnail.admin import AdminImageMixin
from modeltranslation.admin import TranslationAdmin

from .models import (
    AboutUs,
)


# Register your models here.
@admin.register(AboutUs)
class AboutUsAdmin(TranslationAdmin):
    # ('title', 'image', 'video', 'description', 'pub_date', )
    list_display = ('pk', 'title', 'image', 'video', 'pub_date',)
    list_display_links = ('pk', 'title', 'image', 'video', 'pub_date',)
    # list_editable      = ('author', )
    ordering = ('title', 'image', 'video', 'pub_date',)
    search_fields = ('title', 'image', 'video', 'pub_date',)

    fieldsets = (
        (
            'Contents: ', {
                'fields':
                    ('title', 'image', 'video', 'description',),
            }
        ),

    )

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE}
    }


# admin.site.register(AboutUs, AboutUsAdmin)
