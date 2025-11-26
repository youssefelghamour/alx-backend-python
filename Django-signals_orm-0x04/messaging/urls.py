from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, NotificationViewSet, UserViewSet, MessageHistoryViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'users', UserViewSet)
router.register(r'message-history', MessageHistoryViewSet)


urlpatterns = router.urls