from django.db import models
from django.contrib.auth.models import User
import uuid
import os

def upload_to(instance, filename):
    """Generate unique file path for uploaded files"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads', filename)

class UserProfile(models.Model):
    """User profile with role information"""
    ROLE_CHOICES = [
        ('user', 'User'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
    def is_manager(self):
        return self.role in ['manager', 'admin']
    
    def is_admin(self):
        return self.role == 'admin'
    
    def can_manage_files(self):
        return self.role in ['manager', 'admin']
    
    def can_delete_any_file(self):
        return self.role == 'admin'
    
    def can_view_all_files(self):
        return self.role in ['manager', 'admin']

class SharedFile(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to=upload_to)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    download_count = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=True)
    share_code = models.CharField(max_length=10, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.share_code:
            self.share_code = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-upload_date']