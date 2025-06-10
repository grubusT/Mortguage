from django.db import models
from django.contrib.auth.models import User
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

class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    broker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('id', 'Identification'),
        ('income', 'Income Proof'),
        ('bank', 'Bank Statement'),
        ('property', 'Property Documents'),
        ('other', 'Other'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    uploaded_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} - {self.client}"

class Application(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='applications')
    broker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    property_value = models.DecimalField(max_digits=12, decimal_places=2)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Application {self.id} - {self.client}"

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    broker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return self.title

class Reminder(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    broker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reminders', null=True, blank=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='reminders', null=True, blank=True)
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return self.title
