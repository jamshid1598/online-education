from modeltranslation.translator import register, TranslationOptions
from .models import  Category, SubCategory, Lesson


@register(Lesson)
class ProductTranslationOption(TranslationOptions):
    fields = ('name', 'short_info', 'body')


@register(Category)
class CategoryTranslationOption(TranslationOptions):
    field = ('name',)

@register(SubCategory)
class CategoryTranslationOption(TranslationOptions):
    field = ('name',)