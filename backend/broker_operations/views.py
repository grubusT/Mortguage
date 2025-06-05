from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import InterviewScript, ScriptSection
from .serializers import (
    InterviewScriptSerializer,
    InterviewScriptCreateSerializer,
    ScriptSectionSerializer
)

# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint to verify API connectivity
    """
    return Response({
        'status': 'healthy',
        'message': 'API is running',
        'version': '1.0.0'
    })

class InterviewScriptViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing interview scripts.
    """
    queryset = InterviewScript.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['script_type', 'is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'total_duration']

    def get_serializer_class(self):
        if self.action == 'create':
            return InterviewScriptCreateSerializer
        return InterviewScriptSerializer

    def get_queryset(self):
        """
        Optionally filter by active status and script type
        """
        queryset = InterviewScript.objects.all()
        active_only = self.request.query_params.get('active_only', None)
        script_type = self.request.query_params.get('script_type', None)
        
        if active_only is not None:
            queryset = queryset.filter(is_active=True)
        if script_type:
            queryset = queryset.filter(script_type=script_type)
            
        return queryset

class ScriptSectionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing script sections.
    """
    queryset = ScriptSection.objects.all()
    serializer_class = ScriptSectionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order']
