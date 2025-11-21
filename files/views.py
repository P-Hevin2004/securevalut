from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.auth.models import User
import os
import qrcode
import io
import base64
from .models import SharedFile, UserProfile
from .forms import FileUploadForm
from .decorators import manager_required, admin_required, user_or_manager_required

def home(request):
    """Home page showing all public files"""
    files = SharedFile.objects.filter(is_public=True)
    return render(request, 'files/home.html', {'files': files})

def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'files/login.html')

def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'files/register.html', {'form': form})

@login_required
def upload_file(request):
    """File upload view"""
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = form.save(commit=False)
            file_obj.uploaded_by = request.user
            file_obj.save()
            messages.success(request, 'File uploaded successfully!')
            return redirect('my_files')
    else:
        form = FileUploadForm()
    return render(request, 'files/upload.html', {'form': form})

@login_required
def my_files(request):
    """Show user's uploaded files"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if profile.can_view_all_files():
        # Managers and admins can see all files
        files = SharedFile.objects.all()
    else:
        # Regular users can only see their own files
        files = SharedFile.objects.filter(uploaded_by=request.user)
    return render(request, 'files/my_files.html', {'files': files})

def download_file(request, file_id):
    """Download file by ID"""
    file_obj = get_object_or_404(SharedFile, id=file_id)
    
    # Increment download count
    file_obj.download_count += 1
    file_obj.save()
    
    # Serve the file
    file_path = file_obj.file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_obj.title}"'
            return response
    else:
        raise Http404("File not found")

def share_file(request, share_code):
    """Share file using share code"""
    file_obj = get_object_or_404(SharedFile, share_code=share_code)
    
    # Generate QR code for the share link
    share_url = request.build_absolute_uri()
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(share_url)
    qr.make(fit=True)
    
    # Create QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for embedding in HTML
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    qr_code_data = base64.b64encode(buffer.getvalue()).decode()
    
    return render(request, 'files/share.html', {
        'file': file_obj,
        'qr_code_data': qr_code_data,
        'share_url': share_url
    })

def download_shared_file(request, share_code):
    """Download file using share code"""
    file_obj = get_object_or_404(SharedFile, share_code=share_code)
    
    # Increment download count
    file_obj.download_count += 1
    file_obj.save()
    
    # Serve the file
    file_path = file_obj.file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_obj.title}"'
            return response
    else:
        raise Http404("File not found")

@login_required
def delete_file(request, file_id):
    """Delete file"""
    file_obj = get_object_or_404(SharedFile, id=file_id)
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Check permissions
    if not profile.can_delete_any_file() and file_obj.uploaded_by != request.user:
        messages.error(request, 'You do not have permission to delete this file.')
        return redirect('my_files')
    
    # Delete the actual file from storage
    if file_obj.file:
        if os.path.exists(file_obj.file.path):
            os.remove(file_obj.file.path)
    
    file_obj.delete()
    messages.success(request, 'File deleted successfully!')
    return redirect('my_files')

@manager_required
def manage_users(request):
    """Manager/Admin view to manage users"""
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'files/manage_users.html', {'users': users})

@admin_required
def assign_role(request, user_id):
    """Admin view to assign roles to users"""
    user = get_object_or_404(User, id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        new_role = request.POST.get('role')
        if new_role in ['user', 'manager', 'admin']:
            profile.role = new_role
            profile.save()
            messages.success(request, f'Role updated for {user.username}')
        else:
            messages.error(request, 'Invalid role selected')
        return redirect('manage_users')
    
    return render(request, 'files/assign_role.html', {'user': user, 'profile': profile})

@manager_required
def admin_dashboard(request):
    """Manager/Admin dashboard"""
    total_users = User.objects.count()
    total_files = SharedFile.objects.count()
    total_downloads = sum(file.download_count for file in SharedFile.objects.all())
    recent_files = SharedFile.objects.all().order_by('-upload_date')[:5]
    
    context = {
        'total_users': total_users,
        'total_files': total_files,
        'total_downloads': total_downloads,
        'recent_files': recent_files,
    }
    return render(request, 'files/admin_dashboard.html', context)

@login_required
def user_profile(request):
    """User profile page"""
    return render(request, 'files/user_profile.html')

@login_required
def logout_view(request):
    """Log the user out and redirect to login page"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')