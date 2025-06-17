import logging
from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from rest_framework import viewsets, filters, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    InterviewScript, ScriptSection, Client, Application,
    Document, Task, Reminder
)
from .serializers import (
    InterviewScriptSerializer, InterviewScriptCreateSerializer,
    ScriptSectionSerializer, ClientSerializer, ApplicationSerializer,
    DocumentSerializer, TaskSerializer, ReminderSerializer
)

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint to verify API connectivity"""
    try:
        # Test database connection
        client_count = Client.objects.count()
        return Response({
            'status': 'healthy',
            'message': 'API is running',
            'version': '1.0.0',
            'database': 'connected',
            'client_count': client_count
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return Response({
            'status': 'error',
            'message': f'Database connection failed: {str(e)}',
            'version': '1.0.0',
            'database': 'disconnected'
        }, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_summary(request):
    """Dashboard summary endpoint"""
    try:
        total_clients = Client.objects.count()
        active_applications = Application.objects.filter(
            status__in=['pre-approval', 'documentation', 'under-review']
        ).count()
        pending_tasks = Task.objects.filter(status='pending').count()
        completed_this_month = Application.objects.filter(
            status='approved',
            updated_at__month=timezone.now().month
        ).count()
        
        return Response({
            'total_clients': total_clients,
            'active_applications': active_applications,
            'pending_tasks': pending_tasks,
            'completed_this_month': completed_this_month,
        })
    except Exception as e:
        logger.error(f"Dashboard summary failed: {str(e)}")
        return Response({
            'total_clients': 0,
            'active_applications': 0,
            'pending_tasks': 0,
            'completed_this_month': 0,
            'error': str(e)
        }, status=500)

class ClientViewSet(viewsets.ModelViewSet):
    """API endpoint for managing clients"""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['created_at', 'updated_at', 'name']

class ApplicationViewSet(viewsets.ModelViewSet):
    """API endpoint for managing applications"""
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'loan_type']
    search_fields = ['client__name', 'property_address']
    ordering_fields = ['created_at', 'updated_at', 'submitted_date']

class DocumentViewSet(viewsets.ModelViewSet):
    """API endpoint for managing documents"""
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'document_type']
    search_fields = ['name', 'client__name']
    ordering_fields = ['uploaded_at']

class TaskViewSet(viewsets.ModelViewSet):
    """API endpoint for managing tasks"""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['title', 'description', 'client__name']
    ordering_fields = ['created_at', 'due_date', 'priority']

class ReminderViewSet(viewsets.ModelViewSet):
    """API endpoint for managing reminders"""
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['reminder_type', 'is_completed']
    search_fields = ['title', 'description', 'client__name']
    ordering_fields = ['reminder_date', 'created_at']

class InterviewScriptViewSet(viewsets.ModelViewSet):
    """API endpoint for managing interview scripts"""
    queryset = InterviewScript.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['script_type', 'is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'total_duration']

    def get_serializer_class(self):
        if self.action == 'create':
            return InterviewScriptCreateSerializer
        return InterviewScriptSerializer

class ScriptSectionViewSet(viewsets.ModelViewSet):
    """API endpoint for managing script sections"""
    queryset = ScriptSection.objects.all()
    serializer_class = ScriptSectionSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order']
