from rest_framework.routers import DefaultRouter
from .views import MemeberViewSet
router = DefaultRouter()

router.register('',MemeberViewSet,basename='member curd')

urlpatterns = router.urls