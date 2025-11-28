📁 File Share System

A simple and powerful Django-based file sharing system that allows users to upload, manage, share, and download files securely.

🚀 Features
👤 User Management

User registration

Secure login & authentication

📤 File Upload

Upload files with title & description

Choose public or private visibility

🔗 File Sharing

Auto-generated shareable links

Share without login

⬇️ File Download

Direct downloads

Protected download handler

🗂 File Management

View files in My Files

Delete uploaded files

Manage visibility

📊 Analytics

Track file download count

🛠 Installation
1️⃣ Clone the project
cd fileshare_system

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run migrations
python manage.py migrate

4️⃣ Create admin user (optional)
python manage.py createsuperuser

5️⃣ Start development server
python manage.py runserver

6️⃣ Access the application

User site → http://127.0.0.1:8000

Admin panel → http://127.0.0.1:8000/admin

📘 Usage
👤 For Users

Register a new account

Upload files

View & manage your files

Share using unique links

Download your or shared files

🛠 For Admins

Manage users

Monitor activity

Delete or review uploaded files

📂 Project Structure

<img width="526" height="526" alt="image" src="https://github.com/user-attachments/assets/2d5299ea-6ffe-44ec-9126-6cb76029561e" />

🔐 Security Features

Unique file names

Authentication required for private files

Secure share-code-based access

Validated uploads

🎛 Customization
📏 Change upload size limit (settings.py)
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

🔍 Validate file type (forms.py)
def clean_file(self):
    file = self.cleaned_data.get('file')
    # Add validation rules here
    return file

🧰 Troubleshooting
❗ Media files not loading

Verify:

MEDIA_URL
MEDIA_ROOT


are configured properly.

❗ File upload issues

Check file size limit

Check media folder permissions

❗ Database errors

Run:

python manage.py migrate

🧪 Development Tips

Use python manage.py runserver

Monitor Django server logs

Use Django Admin for debugging
