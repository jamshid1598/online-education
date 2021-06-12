from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models
from sorl.thumbnail.admin import AdminImageMixin
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    Category,
    SubCategory,
    Lesson,
)


@admin.register(Category)
class CategoryAdmin(AdminImageMixin, TranslationAdmin):
    lsit_display = ('name', )
    ordering = ('name',)
    search_fields = ('name',)

    fieldsets = (
        (_('Category'), {
            "fields": (
                'name',
                'image',
            ),
        }),
    )


@admin.register(SubCategory)
class SubCategoryAdmin(AdminImageMixin, TranslationAdmin):
    list_display = ('primary_category', 'name', 'price', 'discount', 'paid', 'free',)
    list_display_links=('name',)
    list_editable = ('primary_category', 'price', 'discount', 'paid', 'free',)
    ordering = ('primary_category', 'name', 'price', 'discount', 'paid', 'free',)
    search_fields = ('primary_category', 'name',  'price', 'discount', 'paid', 'free',)

    fieldsets = (
        (_('Sub-Category'), {
            "fields": (
                'primary_category',
                'name',
                'image',
            ),
        }),
    )



@admin.register(Lesson)
class LessonAdmin(AdminImageMixin, TranslationAdmin):

    list_display = ('category', 'name', 'downloaded', 'published_at', 'updated_at',)
    list_display_links = ('name', 'downloaded', 'published_at', 'updated_at',)
    search_fields = ('name',  'category', 'downloaded', 'published_at', 'updated_at',)
    ordering = ('name',  'category', 'downloaded', 'published_at', 'updated_at',)
    list_editable = ( 'category',)

    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        (_('Lesson Category'), {
            "fields": (
                ('category',)
            ),
        }),
        (_('Lesson Video/Image'), {
            "fields": (
                ('video_url', 'video_file', 'image')
            ),
        }),
        (_('Lesson'), {
            "fields": (
                ('name', 'slug', 'short_info', 'body', )
            ),
        }),
    )
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE}
    }


# admin.site.register(Product, ProductAdmin)
