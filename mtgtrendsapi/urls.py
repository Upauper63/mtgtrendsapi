from rest_framework import routers
from .views import ItemsViewSet, ItemViewSet

router = routers.DefaultRouter()
router.register(r'items', ItemsViewSet)
router.register(r'item', ItemViewSet)