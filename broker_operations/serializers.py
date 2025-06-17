from rest_framework import serializers
from .models import (
    InterviewScript, ScriptSection, Client, Application, 
    Document, Task, Reminder, User
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ClientSerializer(serializers.ModelSerializer):
    application_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Client
        fields = [
            'id', 'name', 'email', 'phone', 'address', 'status',
            'created_at', 'updated_at', 'application_count'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_application_count(self, obj):
        return obj.applications.count()

class ApplicationSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'client', 'client_name', 'loan_amount', 'property_address',
            'status', 'progress', 'loan_type', 'submitted_date',
            'expected_close_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class DocumentSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)
    
    class Meta:
        model = Document
        fields = [
            'id', 'client', 'client_name', 'application', 'name',
            'document_type', 'file_path', 'file_size', 'status', 'uploaded_at'
        ]
        read_only_fields = ['uploaded_at']

class TaskSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'client', 'client_name',
            'application', 'priority', 'status', 'due_date',
            'completed_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ReminderSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)
    
    class Meta:
        model = Reminder
        fields = [
            'id', 'title', 'description', 'client', 'client_name',
            'application', 'reminder_date', 'reminder_type',
            'is_completed', 'created_at'
        ]
        read_only_fields = ['created_at']

class ScriptSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScriptSection
        fields = ['id', 'title', 'duration_seconds', 'content', 'order', 'key_notes']

class InterviewScriptSerializer(serializers.ModelSerializer):
    sections = ScriptSectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = InterviewScript
        fields = [
            'id', 'title', 'description', 'script_type', 'version',
            'is_active', 'created_at', 'updated_at', 'total_duration',
            'general_notes', 'sections'
        ]
        read_only_fields = ['created_at', 'updated_at']

class InterviewScriptCreateSerializer(serializers.ModelSerializer):
    sections = ScriptSectionSerializer(many=True)

    class Meta:
        model = InterviewScript
        fields = [
            'title', 'description', 'script_type', 'version',
            'is_active', 'total_duration', 'general_notes', 'sections'
        ]

    def create(self, validated_data):
        sections_data = validated_data.pop('sections')
        script = InterviewScript.objects.create(**validated_data)
        
        for section_data in sections_data:
            section = ScriptSection.objects.create(**section_data)
            script.sections.add(section)
        
        return script
