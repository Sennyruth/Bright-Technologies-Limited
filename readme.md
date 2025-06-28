<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [📦 2. Install Django](#-2-install-django)
- [🛠️ 3. Start a Django Project](#-3-start-a-django-project)
- [🧩 4. Create a Django Application](#-4-create-a-django-application)
- [🐘 5. Configure PostgreSQL as Your Database](#-5-configure-postgresql-as-your-database)
  - [🔧 Install the PostgreSQL driver:](#-install-the-postgresql-driver)
  - [🔧 Update your `settings.py`:](#-update-your-settingspy)
- [📄 6. Install `openpyxl` for Excel/CSV Support](#-6-install-openpyxl-for-excelcsv-support)
- [🔄 7. Apply Migrations](#-7-apply-migrations)
- [▶️ 8. Run the Development Server](#-8-run-the-development-server)
- [📁 9. Collect Static Files (for Deployment)](#-9-collect-static-files-for-deployment)
- [💾 10. Create `requirements.txt`](#-10-create-requirementstxt)
- [🚀 11. Deployment Options](#-11-deployment-options)
  - [Option 1: 🖥️ Deploy to a Linux Server (Gunicorn + Nginx)](#option-1--deploy-to-a-linux-server-gunicorn--nginx)
    - [Install server tools:](#install-server-tools)
    - [Set up the project:](#set-up-the-project)
    - [Set environment variables:](#set-environment-variables)
    - [Apply migrations & collect static files:](#apply-migrations--collect-static-files)
    - [Create Gunicorn service `/etc/systemd/system/btl.service`:](#create-gunicorn-service-etcsystemdsystembtlservice)
    - [Configure Nginx:](#configure-nginx)
  - [Option 2: 🌥️ Deploy on Render.com (Simple Cloud Hosting)](#option-2--deploy-on-rendercom-simple-cloud-hosting)
- [📝 You're All Set!](#-youre-all-set)
- [📦 Extras](#-extras)
  - [Optional: Example `.env` File](#optional-example-env-file)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

* Django setup
* PostgreSQL config
* Excel/CSV import via `openpyxl`
* Creating & activating a local virtual environment
* Deployment options
* `requirements.txt` instructions

---

```markdown
# 🚀 Django Project Setup Guide – Bright Technology Limited

This guide walks you through setting up a Django project with PostgreSQL, managing a virtual environment, enabling Excel/CSV support, and deploying your project.

---

## 📁 Project Structure

```

BrightTechnologyLimited/
├── BTL/                  # Main Django project folder
├── Orders/               # Django app (you'll create this)
├── manage.py
├── requirements.txt
└── README.md

````

---

## 🧪 1. Set Up and Activate a Virtual Environment

Before installing anything, create and activate a virtual environment:

```bash
# Navigate to your project folder (or create it)
cd BrightTechnologyLimited

# Create a virtual environment
python -m venv myenv

# Activate the environment (use the one for your OS)
# Windows
myenv\Scripts\activate

# macOS/Linux
source myenv/bin/activate
````

> ✅ You should see `(myenv)` appear in your terminal prompt after activation.

---

## 📦 2. Install Django

```bash
pip install django
```

> ✅ Verify installation:

```bash
django-admin --version
```

---

## 🛠️ 3. Start a Django Project

```bash
django-admin startproject BTL .
```

---

## 🧩 4. Create a Django Application

```bash
python manage.py startapp Orders
```

Add the app to `INSTALLED_APPS` in `BTL/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'Orders',
]
```

---

## 🐘 5. Configure PostgreSQL as Your Database

### 🔧 Install the PostgreSQL driver:

```bash
pip install psycopg[binary]
```

### 🔧 Update your `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

> 🔐 **Tip**: Store credentials in a `.env` file and use `django-environ` or `python-decouple` for better security.

---

## 📄 6. Install `openpyxl` for Excel/CSV Support

To import Excel `.xlsx` files into your Django models or admin:

```bash
pip install openpyxl
```

> If you're also working with CSVs using Python’s `csv` module, no extra install is needed.

---

## 🔄 7. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## ▶️ 8. Run the Development Server

```bash
python manage.py runserver
```

Visit your site at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📁 9. Collect Static Files (for Deployment)

```bash
python manage.py collectstatic
```

Make sure `STATIC_ROOT` is defined in `settings.py`:

```python
import os
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

---

## 💾 10. Create `requirements.txt`

After installing all necessary packages, save them:

```bash
pip freeze > requirements.txt
```

Example content:

```
Django>=5.2,<6.0
psycopg[binary]>=3.1
openpyxl>=3.1
```

---

## 🚀 11. Deployment Options

### Option 1: 🖥️ Deploy to a Linux Server (Gunicorn + Nginx)

#### Install server tools:

```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

#### Set up the project:

```bash
git clone <your-repo-url>
cd BrightTechnologyLimited
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Set environment variables:

Use `.env` or environment secrets:

```env
DEBUG=False
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=yourdomain.com
```

#### Apply migrations & collect static files:

```bash
python manage.py migrate
python manage.py collectstatic
```

#### Create Gunicorn service `/etc/systemd/system/btl.service`:

```ini
[Unit]
Description=BTL Django App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/project
ExecStart=/path/to/project/venv/bin/gunicorn BTL.wsgi:application --bind 127.0.0.1:8001

[Install]
WantedBy=multi-user.target
```

#### Configure Nginx:

Create `/etc/nginx/sites-available/btl`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/project/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        include proxy_params;
    }
}
```

Then run:

```bash
sudo ln -s /etc/nginx/sites-available/btl /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

---

### Option 2: 🌥️ Deploy on Render.com (Simple Cloud Hosting)

1. Go to [https://render.com](https://render.com)
2. Click **New Web Service**
3. Connect your GitHub repo
4. Set:

   * **Build Command:**

     ```bash
     pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
     ```
   * **Start Command:**

     ```bash
     gunicorn BTL.wsgi
     ```
   * Add environment variables for `SECRET_KEY`, `DEBUG=False`, etc.
5. Deploy 🎉

---

## 📝 You're All Set!

You now have a working Django project with:

* Local virtual environment
* PostgreSQL database
* Excel/CSV import support
* Static file collection
* Ready-to-deploy structure

---

## 📦 Extras

### Optional: Example `.env` File

```
DEBUG=True
SECRET_KEY=your_dev_secret_key
DATABASE_URL=postgres://user:password@localhost:5432/dbname
ALLOWED_HOSTS=127.0.0.1,localhost
```


