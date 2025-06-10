from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db.models import Q
from .models import InterviewScript, ScriptSection, Client, Document, Application, Task, Reminder
from .serializers import (
    InterviewScriptSerializer,
    InterviewScriptCreateSerializer,
    ScriptSectionSerializer,
    UserSerializer, UserCreateSerializer, ClientSerializer,
    DocumentSerializer, ApplicationSerializer, TaskSerializer,
    ReminderSerializer
)
from django.utils import timezone

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

# Authentication Views
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
    except User.DoesNotExist:
        pass
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data)

# Client Views
class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email', 'phone']

    def get_queryset(self):
        return Client.objects.filter(broker=self.request.user)

    def perform_create(self, serializer):
        serializer.save(broker=self.request.user)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        clients = self.get_queryset().filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )
        serializer = self.get_serializer(clients, many=True)
        return Response(serializer.data)

# Document Views
class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(client__broker=self.request.user)

    @action(detail=False, methods=['post'])
    def upload_client_document(self, request, client_id=None):
        try:
            client = Client.objects.get(id=client_id, broker=request.user)
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(client=client)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Client.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# Application Views
class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(broker=self.request.user)

    def perform_create(self, serializer):
        serializer.save(broker=self.request.user)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        application = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()
            return Response(self.get_serializer(application).data)
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

# Dashboard Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    user = request.user
    summary = {
        'total_clients': Client.objects.filter(broker=user).count(),
        'active_applications': Application.objects.filter(broker=user, status__in=['submitted', 'under_review']).count(),
        'pending_tasks': Task.objects.filter(broker=user, status='pending').count(),
        'upcoming_reminders': Reminder.objects.filter(broker=user, is_completed=False).count(),
    }
    return Response(summary)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_activity(request):
    user = request.user
    activities = {
        'recent_applications': ApplicationSerializer(
            Application.objects.filter(broker=user).order_by('-created_at')[:5],
            many=True
        ).data,
        'recent_tasks': TaskSerializer(
            Task.objects.filter(broker=user).order_by('-created_at')[:5],
            many=True
        ).data,
    }
    return Response(activities)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_reminders(request):
    user = request.user
    reminders = Reminder.objects.filter(
        broker=user,
        is_completed=False,
        due_date__gte=timezone.now()
    ).order_by('due_date')
    return Response(ReminderSerializer(reminders, many=True).data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_tasks(request):
    user = request.user
    tasks = Task.objects.filter(
        broker=user,
        status__in=['pending', 'in_progress']
    ).order_by('due_date')
    return Response(TaskSerializer(tasks, many=True).data)
