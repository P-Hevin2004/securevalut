# SecureValut 🔐

A beautiful, responsive file sharing web app built with Django. Upload, manage, and securely share files with ease.

[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

## 🌟 Features

- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices.
- **Secure Authentication**: User registration and login system.
- **File Management**: Upload files with titles and descriptions.
- **Sharing Options**: 
  - **Public**: Auto-generated shareable links.
  - **Private**: Secure access for specific users.
- **Download Tracking**: Monitor how many times your files are downloaded.
- **Admin Dashboard**: Manage users and files via Django Admin.

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, CSS3, Bootstrap 5 / Custom CSS
- **Database**: SQLite (Development)
- **Icons**: FontAwesome

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- [Python 3.8+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## 🚀 Installation & Setup

Follow these steps to get the project running on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/Dhruv-4985/securevalut.git
cd securevalut
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirement.txt
```

### 4. Apply Database Migrations

Initialize the database tables.

```bash
python manage.py migrate
```

### 5. Create a Superuser (Optional)

To access the Django admin panel, create a superuser account.

```bash
python manage.py createsuperuser
```
Follow the prompts to set a username, email, and password.

### 6. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and navigate to: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 📂 Project Structure

```
securevalut/
├── files/              # Main application logic (views, models, urls)
├── fileshare_system/   # Project settings and configuration
├── media/              # User uploaded files
├── static/             # Static assets (CSS, JS, Images)
├── templates/          # HTML Templates
│   ├── files/          # App-specific templates
│   └── ...
├── db.sqlite3          # Database file
├── manage.py           # Django management script
└── requirement.txt     # Project dependencies
```

## 📝 Usage Guide

1. **Register/Login**: Create an account to start uploading files.
2. **Upload**: Click the "Upload" button, select a file, and choose visibility settings.
3. **Share**: 
   - For **Public** files, copy the generated link or QR code.
   - For **Private** files, only authorized users can access them.
4. **Manage**: View your uploaded files in the "My Files" section.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

**Dhruv** - [GitHub Profile](https://github.com/P-Hevin2004)

Project Link: [https://github.com/Dhruv-4985/securevalut](https://github.com/P-Hevin2004/securevalut)
