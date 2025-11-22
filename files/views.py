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
from .models import SharedFile, UserProfile, Group
from .forms import FileUploadForm
from .decorators import manager_required, admin_required, user_or_manager_required
from django.db.models import Q

def home(request):
    """Home page showing files accessible to the user"""
    if request.user.is_authenticated:
        # Show files user can access: own files, public files, or files shared with user/groups
        files = SharedFile.objects.filter(
            Q(uploaded_by=request.user) |
            Q(is_public=True) |
            Q(allowed_users=request.user) |
            Q(allowed_groups__members=request.user)
        ).distinct()
    else:
        # Unauthenticated users cannot see any files - they must login
        files = SharedFile.objects.none()
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
        form = FileUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            file_obj = form.save(commit=False)
            file_obj.uploaded_by = request.user
            file_obj.save()
            # Save many-to-many relationships
            form.save_m2m()
            messages.success(request, 'File uploaded successfully!')
            return redirect('my_files')
    else:
        form = FileUploadForm(user=request.user)
    return render(request, 'files/upload.html', {'form': form})

@login_required
def my_files(request):
    """Show files accessible to the user"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if profile.can_view_all_files():
        # Managers and admins can see all files
        files = SharedFile.objects.all()
    else:
        # Regular users see: own files, public files, or files shared with them/groups
        files = SharedFile.objects.filter(
            Q(uploaded_by=request.user) |
            Q(is_public=True) |
            Q(allowed_users=request.user) |
            Q(allowed_groups__members=request.user)
        ).distinct()
    return render(request, 'files/my_files.html', {'files': files})

@login_required
def download_file(request, file_id):
    """Download file by ID"""
    file_obj = get_object_or_404(SharedFile, id=file_id)
    
    # Check permissions
    if not file_obj.can_access(request.user):
        messages.error(request, 'You do not have permission to download this file.')
        return redirect('my_files')
    
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
    """Share file using share code - redirects to direct download"""
    # Always redirect to download when share link is accessed
    return redirect('download_shared', share_code=share_code)

def view_share_page(request, share_code):
    """View share page with QR code (for use within the app)"""
    file_obj = get_object_or_404(SharedFile, share_code=share_code)
    
    # Generate QR code for the download link
    from django.urls import reverse
    download_url = request.build_absolute_uri(
        reverse('download_shared', args=[share_code])
    )
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(download_url)
    qr.make(fit=True)
    
    # Create QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for embedding in HTML
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    qr_code_data = base64.b64encode(buffer.getvalue()).decode()
    
    # Share URL should be the download link (what gets shared)
    share_url = download_url
    
    return render(request, 'files/share.html', {
        'file': file_obj,
        'qr_code_data': qr_code_data,
        'share_url': share_url,
        'download_url': download_url
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

@login_required
def groups_list(request):
    """List all groups the user is a member of or created"""
    user_groups = Group.objects.filter(
        Q(created_by=request.user) | Q(members=request.user)
    ).distinct()
    return render(request, 'files/groups_list.html', {'groups': user_groups})

@login_required
def create_group(request):
    """Create a new group"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        member_ids = request.POST.getlist('members')
        
        if name:
            group = Group.objects.create(
                name=name,
                description=description,
                created_by=request.user
            )
            # Add members
            if member_ids:
                members = User.objects.filter(id__in=member_ids)
                group.members.set(members)
            # Always add creator as member
            group.members.add(request.user)
            messages.success(request, f'Group "{name}" created successfully!')
            return redirect('groups_list')
        else:
            messages.error(request, 'Group name is required.')
    
    # Get all users except current user for member selection
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'files/create_group.html', {'users': users})

@login_required
def group_detail(request, group_id):
    """View and manage group details"""
    group = get_object_or_404(Group, id=group_id)
    
    # Check if user has access (creator or member)
    if group.created_by != request.user and not group.members.filter(id=request.user.id).exists():
        messages.error(request, 'You do not have permission to view this group.')
        return redirect('groups_list')
    
    if request.method == 'POST':
        # Handle member addition/removal
        action = request.POST.get('action')
        if action == 'add_member':
            user_id = request.POST.get('user_id')
            if user_id:
                user = get_object_or_404(User, id=user_id)
                group.members.add(user)
                messages.success(request, f'{user.username} added to group.')
        elif action == 'remove_member':
            user_id = request.POST.get('user_id')
            if user_id:
                user = get_object_or_404(User, id=user_id)
                if user != group.created_by:  # Can't remove creator
                    group.members.remove(user)
                    messages.success(request, f'{user.username} removed from group.')
        elif action == 'delete_group':
            if group.created_by == request.user:
                group.delete()
                messages.success(request, 'Group deleted successfully!')
                return redirect('groups_list')
            else:
                messages.error(request, 'Only the group creator can delete the group.')
    
    # Get all users for adding members
    all_users = User.objects.exclude(id=request.user.id)
    group_files = group.shared_files.all()
    
    return render(request, 'files/group_detail.html', {
        'group': group,
        'all_users': all_users,
        'group_files': group_files
    })