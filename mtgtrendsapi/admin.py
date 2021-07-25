from mtgtrendsapi.models import Item, Scrape
from django.contrib import admin
from .models import Scrape, Item

# Register your models here.
admin.site.register(Scrape)
admin.site.register(Item)