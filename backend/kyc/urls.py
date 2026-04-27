from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KYCSubmissionViewSet, reviewer_dashboard
from .views import KYCSubmissionViewSet, reviewer_dashboard, DocumentViewSet

router = DefaultRouter()
router.register(r'submissions', KYCSubmissionViewSet, basename='submission')
router.register('documents', DocumentViewSet, basename='document')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', reviewer_dashboard),
]