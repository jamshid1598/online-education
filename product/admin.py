from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models
from sorl.thumbnail.admin import AdminImageMixin
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    Category,
    Subject,
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


@admin.register(Subject)
class SubjectAdmin(AdminImageMixin, TranslationAdmin):
    list_display = ('category', 'name', 'teacher_info', 'downloaded', 'price', 'discount', 'free',)
    list_display_links=('name', 'downloaded',)
    list_editable = ('category', 'price', 'discount', 'free',)
    ordering = ('category', 'name', 'downloaded', 'price', 'discount', 'free',)
    search_fields = ('category', 'name', 'downloaded',  'price', 'discount', 'free',)

    def teacher_info(self, obj):
        if obj.teacher:
            teacher = obj.teacher.teacher.first_name+" | "+str(obj.teacher.teacher.phone_number)
        else:
            teacher = ''
        return teacher

    prepopulated_fields = {'slug': ['name',]}

    fieldsets = (
        (_('Subject'), {
            "fields": (
                'category',
                'teacher',
                'name',
                'slug',
                'image',
                'short_info',

                'price',
                'discount',
                'free',
            ),
        }),
    )
    
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE}
    }



@admin.register(Lesson)
class LessonAdmin(AdminImageMixin, TranslationAdmin):

    list_display = ('subject', 'name', 'lesson_series', 'published_at', 'updated_at',)
    list_display_links = ('name', 'published_at', 'updated_at',)
    search_fields = ('name', 'lesson_series', 'subject', 'published_at', 'updated_at',)
    ordering = ('name',  'subject', 'lesson_series', 'published_at', 'updated_at',)
    list_editable = ( 'subject', 'lesson_series',)

    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        (_('Subject'), {
            "fields": (
                ('subject',)
            ),
        }),
        (_('Lesson Video/Image'), {
            "fields": (
                ('video_file', 'image')
            ),
        }),
        (_('Lesson Body'), {
            "fields": (
                ('name', 'slug', 'body', )
            ),
        }),
    )
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE}
    }


# admin.site.register(Product, ProductAdmin)
