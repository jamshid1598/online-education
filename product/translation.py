from modeltranslation.translator import register, TranslationOptions
from .models import  Category, Subject, Lesson


@register(Lesson)
class LessonTranslationOption(TranslationOptions):
    fields = ('name', 'body')

@register(Subject)
class SubjectTranslationOption(TranslationOptions):
    field = ('name', 'short_info',)

@register(Category)
class CategoryTranslationOption(TranslationOptions):
    field = ('name',)

