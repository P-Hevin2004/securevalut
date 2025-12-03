from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('upload/', views.upload_file, name='upload'),
    path('my-files/', views.my_files, name='my_files'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('assign-role/<int:user_id>/', views.assign_role, name='assign_role'),
    path('download/<int:file_id>/', views.download_file, name='download'),
    path('share/<str:share_code>/', views.share_file, name='share'),
    path('view-share/<str:share_code>/', views.view_share_page, name='view_share'),
    path('download-shared/<str:share_code>/', views.download_shared_file, name='download_shared'),
    path('delete/<int:file_id>/', views.delete_file, name='delete'),
    # Group management URLs
    path('groups/', views.groups_list, name='groups_list'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
]
