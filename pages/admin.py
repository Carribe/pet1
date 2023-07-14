from django.contrib import admin
from .models import *


class PageAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "time_create", "photo", "is_published")
    list_display_links = ("id", "title")
    search_fields = ("title", "content")
    list_editable = ("is_published",)
    list_filter = ("is_published", "time_create")
    prepopulated_fields = {"slug": ("title",)}

class FilmTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    prepopulated_fields = {"slug":("name",)}


# Register your models here.
admin.site.register(Page, PageAdmin)
admin.site.register(FilmType, FilmTypeAdmin)
