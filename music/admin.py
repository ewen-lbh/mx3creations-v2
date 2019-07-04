from django.contrib import admin
from .models import *

class TrackInline(admin.TabularInline):
    model = Track
    fields = (
        'track_number',
        'title',
        'collection',
        'artist',
        'is_remix',
        'goodness',
        'video_url',
        'slug'
    )
# Register your models here.
@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = (
        'track_number',
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

    list_display_links = ('title',)

    list_editable = (
        'track_number',
        'collection',
        'artist',
        'is_remix',
        'goodness',
        'video_url',
        'slug'
    )

    def get_date(self, obj):
        return obj.collection.date
    get_date.short_description = 'Date'
    get_date.admin_order_field = 'collection__date'

    list_filter = ('collection','artist','is_remix','collection','goodness', 'collection__kind')

    search_fields = ('collection','artist','title','video_url')

    prepopulated_fields = {'slug':('title',)}

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'kind',
        'date',
        'description_fr',
        'description_en',
        'cover_color',
        'cover_accent_color',
        'work_time',
        'playlist_url',
        'slug'
    )
    list_editable = (
        'kind',
        'work_time',
        'playlist_url',
        'slug'
    )

    inlines = [TrackInline,]

    list_filter = ('date','kind','work_time','cover_color')

    date_hierarchy = 'date'

    ordering = ('date',)

    search_fields = ('title','kind','playlist_url','description_fr','description_en', 'cover_accent_color')

    prepopulated_fields = {'slug':('title',)}

