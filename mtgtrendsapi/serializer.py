from rest_framework import serializers

from .models import Item, Scrape

class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'diff_price_prev')

class ItemSerializer(serializers.ModelSerializer):
    trends = serializers.SerializerMethodField()
    class Meta:
        model = Item
        fields = ('id', 'name', 'diff_price_prev', 'trends')
    def get_trends(self, instance):
        return instance.get_trends()