from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    InterviewScriptViewSet, ScriptSectionViewSet, ClientViewSet,
    ApplicationViewSet, DocumentViewSet, TaskViewSet, ReminderViewSet,
    health_check, dashboard_summary
)

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'applications', ApplicationViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'reminders', ReminderViewSet)
router.register(r'interview-scripts', InterviewScriptViewSet)
router.register(r'script-sections', ScriptSectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('health/', health_check, name='health-check'),
    path('dashboard/summary/', dashboard_summary, name='dashboard-summary'),
]
