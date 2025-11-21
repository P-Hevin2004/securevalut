from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles):
    """
    Decorator to check if user has required role
    Usage: @role_required(['admin', 'manager'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'You must be logged in to access this page.')
                return redirect('login')
            
            if request.user.role not in allowed_roles:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('home')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def manager_required(view_func):
    """Decorator to require manager or admin role"""
    return role_required(['manager', 'admin'])(view_func)

def admin_required(view_func):
    """Decorator to require admin role"""
    return role_required(['admin'])(view_func)

def user_or_manager_required(view_func):
    """Decorator to require user, manager, or admin role"""
    return role_required(['user', 'manager', 'admin'])(view_func)
