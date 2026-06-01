from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, ApplicationViewSet, JobRawAPIView, ApplicationRawAPIView

router = DefaultRouter()
router.register(r'jobs', JobViewSet)
router.register(r'applications', ApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('raw-jobs/', JobRawAPIView.as_view(), name='raw-jobs'),
    path('raw-jobs/<int:pk>/', JobRawAPIView.as_view(), name='raw-jobs-detail'),
    path('raw-applications/', ApplicationRawAPIView.as_view(), name='raw-applications'),
    path('raw-applications/<int:pk>/', ApplicationRawAPIView.as_view(), name='raw-applications-detail'),
]
