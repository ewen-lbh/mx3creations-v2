from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'collection',
        'artist',
        'is_remix',
        'duration',
        'goodness',
        'video_url',
        'get_date',
        'slug'
    )

    def get_date(self, obj):
        return obj.collection.date
    get_date.short_description = 'Date'
    get_date.admin_order_field = 'collection__date'

    list_filter = ('collection','artist','is_remix','collection','goodness')

    search_fields = ('collection','artist','title','video_url')

    prepopulated_fields = {'slug':('title',)}

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'kind',
        'date',
        'cover_color',
        'work_time',
        'playlist_url',
        'slug'
    )

    list_filter = ('date','kind','work_time','cover_color')

    date_hierarchy = 'date'

    ordering = ('date',)

    search_fields = ('title','kind','playlist_url')

    prepopulated_fields = {'slug':('title',)}
