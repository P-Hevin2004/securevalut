from django.db import models
from django.contrib.auth.models import User
import uuid
import os

def upload_to(instance, filename):
    """Generate unique file path for uploaded files"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads', filename)

class Group(models.Model):
    """Group model for sharing files with multiple users"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(User, related_name='file_groups', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']

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
    is_public = models.BooleanField(default=False)  # Changed default to False
    share_code = models.CharField(max_length=10, unique=True, blank=True)
    # Permission fields
    allowed_users = models.ManyToManyField(User, related_name='shared_files', blank=True)
    allowed_groups = models.ManyToManyField(Group, related_name='shared_files', blank=True)
    
    def save(self, *args, **kwargs):
        if not self.share_code:
            self.share_code = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)
    
    def can_access(self, user):
        """Check if a user can access this file"""
        # Owner can always access
        if self.uploaded_by == user:
            return True
        # Public files can be accessed by anyone
        if self.is_public:
            return True
        # Check if user is in allowed_users
        if self.allowed_users.filter(id=user.id).exists():
            return True
        # Check if user is in any allowed_groups
        if self.allowed_groups.filter(members=user).exists():
            return True
        return False
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-upload_date']