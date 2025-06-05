from django.db import models
from django.utils import timezone

# Create your models here.

class ScriptSection(models.Model):
    title = models.CharField(max_length=200)
    duration_seconds = models.IntegerField()
    content = models.TextField()
    order = models.IntegerField()
    key_notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.duration_seconds}s)"

class InterviewScript(models.Model):
    SCRIPT_TYPES = [
        ('initial_call', 'Initial Client Call'),
        ('follow_up', 'Follow-up Call'),
        ('closing', 'Closing Call'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    script_type = models.CharField(max_length=20, choices=SCRIPT_TYPES)
    version = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    total_duration = models.IntegerField(help_text="Total duration in seconds")
    general_notes = models.TextField(blank=True, null=True)
    sections = models.ManyToManyField(ScriptSection, related_name='scripts')

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} (v{self.version})"
