# File Share System

A simple Django-based file sharing system that allows users to upload, share, and download files.

## Features

- **User Registration & Authentication**: Users can create accounts and log in
- **File Upload**: Upload files with title, description, and privacy settings
- **File Sharing**: Generate shareable links for files
- **File Download**: Download files directly or through share links
- **File Management**: View, delete, and manage uploaded files
- **Public/Private Files**: Control file visibility
- **Download Tracking**: Track download counts for files

## Installation

1. **Clone or download the project**
   ```bash
   cd fileshare_system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000`
   - Register a new account or use the admin account

## Usage

### For Users
1. **Register**: Create a new account
2. **Upload Files**: Click "Upload" to add files
3. **Manage Files**: View your files in "My Files"
4. **Share Files**: Use the share button to get shareable links
5. **Download Files**: Download files directly or through share links

### For Administrators
- Access the admin panel at `http://127.0.0.1:8000/admin`
- Manage users and files
- Monitor system activity

## File Structure

```
fileshare_system/
├── files/                    # Main app
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── forms.py             # Form definitions
│   └── urls.py              # URL patterns
├── templates/               # HTML templates
│   └── files/
│       ├── base.html        # Base template
│       ├── home.html        # Home page
│       ├── register.html    # Registration page
│       ├── upload.html      # File upload page
│       ├── my_files.html    # User's files page
│       └── share.html       # File sharing page
├── media/                   # Uploaded files (created automatically)
├── manage.py                # Django management script
└── requirements.txt         # Project dependencies
```

## Key Features Explained

### File Upload
- Users can upload files with custom titles and descriptions
- Files are stored securely with unique names
- Privacy settings control file visibility

### File Sharing
- Each file gets a unique share code
- Shareable links work without authentication
- Download tracking for analytics

### Security
- File uploads are validated
- Unique file names prevent conflicts
- User authentication required for uploads

## Customization

### File Size Limits
Modify the file size limit in `settings.py`:
```python
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
```

### Allowed File Types
Add file type validation in `forms.py`:
```python
def clean_file(self):
    file = self.cleaned_data.get('file')
    # Add validation logic here
    return file
```

## Troubleshooting

### Common Issues
1. **Media files not loading**: Ensure `MEDIA_URL` and `MEDIA_ROOT` are set correctly
2. **File upload errors**: Check file size limits and permissions
3. **Database errors**: Run `python manage.py migrate` to apply migrations

### Development Tips
- Use `python manage.py runserver` for development
- Check Django logs for error details
- Use the admin panel to manage data

## License

This project is open source and available under the MIT License.
