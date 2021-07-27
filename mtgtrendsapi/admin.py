from mtgtrendsapi.models import Item, Scrape
from django.contrib import admin
from .models import Scrape, Item

class ScrapeAdmin(admin.ModelAdmin):
    readonly_fields = ('started_at', 'finished_at', 'is_finished', 'status', 'status_info')

admin.site.register(Scrape, ScrapeAdmin)
admin.site.register(Item)