from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'kind',
        'date',
        'description_fr',
        'description_en',
        'slug',
        'length'
    )

    list_filter = ('date','kind','title')

    date_hierarchy = 'date'

    ordering = ('date','length','kind')

    search_fields = ('title','kind','description_fr','description_en')

    prepopulated_fields = {'slug':('title',)}
