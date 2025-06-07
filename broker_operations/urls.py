from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InterviewScriptViewSet, ScriptSectionViewSet, health_check

router = DefaultRouter()
router.register(r'interview-scripts', InterviewScriptViewSet)
router.register(r'script-sections', ScriptSectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('health/', health_check, name='health-check'),
] 