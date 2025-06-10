from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'clients', views.ClientViewSet, basename='client')
router.register(r'documents', views.DocumentViewSet, basename='document')
router.register(r'applications', views.ApplicationViewSet, basename='application')

urlpatterns = [
    # Authentication URLs
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout, name='logout'),
    path('auth/me/', views.me, name='me'),

    # Dashboard URLs
    path('dashboard/summary/', views.dashboard_summary, name='dashboard-summary'),
    path('dashboard/activity/', views.dashboard_activity, name='dashboard-activity'),
    path('dashboard/reminders/', views.dashboard_reminders, name='dashboard-reminders'),
    path('dashboard/tasks/', views.dashboard_tasks, name='dashboard-tasks'),

    # Include router URLs
    path('', include(router.urls)),
] 