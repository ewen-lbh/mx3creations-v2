from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'kind',
        'date',
        'description_fr',
        'description_en',
        'slug',
        'dimensions'
    )

    list_filter = ('date','kind','title')

    date_hierarchy = 'date'

    ordering = ('date','dimensions','kind')

    search_fields = ('title','kind','description_fr','description_en')

    prepopulated_fields = {'slug':('title',)}
