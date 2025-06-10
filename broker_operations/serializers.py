from rest_framework import serializers
from django.contrib.auth.models import User
from .models import InterviewScript, ScriptSection, Client, Document, Application, Task, Reminder

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'address', 
                 'created_at', 'updated_at', 'notes']
        read_only_fields = ['id', 'created_at', 'updated_at']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'client', 'title', 'file', 'document_type', 
                 'uploaded_at', 'notes']
        read_only_fields = ['id', 'uploaded_at']

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'client', 'broker', 'status', 'created_at', 
                 'updated_at', 'loan_amount', 'property_value', 'notes']
        read_only_fields = ['id', 'created_at', 'updated_at']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'broker', 'client', 
                 'application', 'due_date', 'priority', 'status', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ['id', 'title', 'description', 'broker', 'client', 
                 'application', 'due_date', 'is_completed', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

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