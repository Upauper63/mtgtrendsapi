import django_filters
from rest_framework import viewsets, filters

from .models import Item
from .serializer import ItemsSerializer, ItemSerializer


class ItemsViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('-diff_price_prev', '-current_price')
    serializer_class = ItemsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['id']
