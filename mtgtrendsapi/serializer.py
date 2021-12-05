from rest_framework import serializers

from .models import Item, Scrape

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'diff_price_prev')
        read_only_fields = [f.name for f in Item._meta.get_fields()]

class ItemSerializer(serializers.ModelSerializer):
    trends = serializers.SerializerMethodField()
    class Meta:
        model = Item
        fields = ('id', 'name', 'diff_price_prev', 'trends')
        read_only_fields = [f.name for f in Item._meta.get_fields()]
    def get_trends(self, instance):
        return instance.get_trends()