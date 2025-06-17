from django.db import models
from django.utils import timezone

# Create your models here.

class Client(models.Model):
    """Client model for mortgage broker operations"""
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('inactive', 'Inactive'),
    ], default='active')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'broker_operations_client'
    
    def __str__(self):
        return self.name

class Application(models.Model):
    """Mortgage application model"""
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='applications')
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    property_address = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('pre-approval', 'Pre-approval'),
        ('documentation', 'Documentation'),
        ('under-review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='pre-approval')
    progress = models.IntegerField(default=0)
    loan_type = models.CharField(max_length=50)
    submitted_date = models.DateTimeField(default=timezone.now)
    expected_close_date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'broker_operations_application'
    
    def __str__(self):
        return f"{self.client.name} - {self.loan_type}"

class Document(models.Model):
    """Document model for client documents"""
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='documents')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    name = models.CharField(max_length=255)
    document_type = models.CharField(max_length=100)
    file_path = models.CharField(max_length=500)
    file_size = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('under-review', 'Under Review'),
    ], default='pending')
    uploaded_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'broker_operations_document'
    
    def __str__(self):
        return f"{self.client.name} - {self.name}"

class Task(models.Model):
    """Task model for broker operations"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    priority = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], default='medium')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('in-progress', 'In Progress'),
        ('completed', 'Completed'),
    ], default='pending')
    due_date = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'broker_operations_task'
    
    def __str__(self):
        return self.title

class Reminder(models.Model):
    """Reminder model for important dates and follow-ups"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reminders', null=True, blank=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='reminders', null=True, blank=True)
    reminder_date = models.DateTimeField()
    reminder_type = models.CharField(max_length=50, choices=[
        ('call', 'Call'),
        ('meeting', 'Meeting'),
        ('document', 'Document'),
        ('follow-up', 'Follow-up'),
    ])
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'broker_operations_reminder'
    
    def __str__(self):
        return self.title

class ScriptSection(models.Model):
    title = models.CharField(max_length=200)
    duration_seconds = models.IntegerField()
    content = models.TextField()
    order = models.IntegerField()
    key_notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['order']
        db_table = 'broker_operations_scriptsection'

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
        db_table = 'broker_operations_interviewscript'

    def __str__(self):
        return f"{self.title} (v{self.version})"
