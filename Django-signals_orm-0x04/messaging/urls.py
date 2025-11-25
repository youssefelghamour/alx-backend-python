from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, NotificationViewSet, UserViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'users', UserViewSet)


urlpatterns = router.urls