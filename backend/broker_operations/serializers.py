from rest_framework import serializers
from .models import InterviewScript, ScriptSection

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
