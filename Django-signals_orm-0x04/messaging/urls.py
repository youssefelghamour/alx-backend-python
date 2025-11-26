from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import MessageViewSet, NotificationViewSet, UserViewSet, MessageHistoryViewSet, ThreadsViewSet
from .views import delete_user

router = DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'users', UserViewSet)
router.register(r'message-history', MessageHistoryViewSet)
router.register('threads', ThreadsViewSet, basename='threads')

urlpatterns = router.urls + [
    path('delete-user/', delete_user),
]