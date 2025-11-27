import os
import django
from django.conf import settings

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fileshare_system.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from files.models import SharedFile
from django.core.files.uploadedfile import SimpleUploadedFile

def test_security():
    # Setup
    print("Setting up users and files...")
    # Create users
    user_a, _ = User.objects.get_or_create(username='user_a', email='a@example.com', password='password')
    user_b, _ = User.objects.get_or_create(username='user_b', email='b@example.com', password='password')
    
    # Create a PRIVATE file for User A
    file_content = b"Secret content"
    file_a = SharedFile.objects.create(
        title="Secret File",
        file=SimpleUploadedFile("secret.txt", file_content),
        uploaded_by=user_a,
        is_public=False  # PRIVATE
    )
    print(f"Created private file '{file_a.title}' for User A. Share code: {file_a.share_code}")

    client = Client()

    # Test 1: User B tries to download via ID (should fail)
    print("\nTest 1: User B tries to download via ID...")
    client.force_login(user_b)
    resp = client.get(f'/download/{file_a.id}/')
    if resp.status_code == 302: # Redirects to my_files on error
        print("PASS: User B cannot download via ID (redirected).")
    elif resp.status_code == 200:
        print("FAIL: User B downloaded via ID!")
    else:
        print(f"Unexpected status: {resp.status_code}")

    # Test 2: Anonymous user tries to download via Share Link (should probably fail if we want strict security, but currently passes)
    print("\nTest 2: Anonymous user tries to download via Share Link...")
    client.logout()
    resp = client.get(f'/download-shared/{file_a.share_code}/')
    if resp.status_code == 200:
        print("FAIL (Vulnerability Confirmed): Anonymous user downloaded private file via share link!")
        print(f"Content: {resp.content}")
    else:
        print(f"PASS: Anonymous user could not download. Status: {resp.status_code}")

if __name__ == '__main__':
    try:
        test_security()
    except Exception as e:
        print(f"Error: {e}")
