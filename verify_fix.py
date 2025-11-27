import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'securevalut.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from files.models import SharedFile
from files.views import download_file

def verify_fix():
    # Create a user
    user, created = User.objects.get_or_create(username='testuser')
    
    # Create a file without extension in title
    file_content = b"Hello World"
    uploaded_file = SimpleUploadedFile("test_file.txt", file_content, content_type="text/plain")
    
    shared_file = SharedFile.objects.create(
        title="Test File No Extension",
        file=uploaded_file,
        uploaded_by=user
    )
    
    print(f"Created file: {shared_file.title} (Path: {shared_file.file.path})")
    
    # Create a request
    factory = RequestFactory()
    request = factory.get(f'/download/{shared_file.id}/')
    request.user = user
    
    # Call the view
    response = download_file(request, shared_file.id)
    
    # Check Content-Disposition
    content_disposition = response.get('Content-Disposition', '')
    print(f"Content-Disposition: {content_disposition}")
    
    expected_filename = 'Test File No Extension.txt'
    if expected_filename in content_disposition:
        print("SUCCESS: Filename has correct extension.")
    else:
        print(f"FAILURE: Expected filename '{expected_filename}' not found in header.")

    # Clean up
    shared_file.delete()
    # User cleanup is optional/skipped to avoid affecting other tests if any

if __name__ == '__main__':
    verify_fix()
