# 🚀 Django Project Setup Guide

This guide walks you through installing Django, creating your project and apps, configuring PostgreSQL, using Excel/CSV files, and running your development server.

---

## 📦 1. Install Django

Make sure you have Python installed, then install Django with:

```bash
pip install django
```

> ✅ **Tip**: Verify the installation with:
>
> ```bash
> django-admin --version
> ```

---

## 🛠️ 2. Create a New Django Project

You can start a new project using either of the commands below:

**Option 1 (recommended):**

```bash
django-admin startproject BTL
```

**Option 2 (if `django-admin` is not recognized):**

```bash
python -m django startproject BTL
```

This will generate the following structure:

```
BTL/
├── BTL/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
```

---

## 🧩 3. Create a Django Application

Navigate into your project directory and create an app:

```bash
cd BTL
python manage.py startapp Orders
```

> 📌 Be sure to add `'Orders'` to your `INSTALLED_APPS` in `settings.py`.

---

## 🐘 4. Configure PostgreSQL as Your Database

### 🔧 Install PostgreSQL driver:

```bash
pip install psycopg[binary]
```

### 🔧 Update your `settings.py`:

Replace the default `DATABASES` config with:

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

> 🔐 **Tip**: Store sensitive credentials in a `.env` file using `python-decouple` or `django-environ`.

---

## 🔄 5. Apply Migrations

After creating or updating models:

```bash
python manage.py makemigrations
python manage.py migrate
```

This syncs your models with the database.

---

## ▶️ 6. Run the Development Server

Start your Django development server:

```bash
python manage.py runserver
```

Visit your site at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📄 7. Install `openpyxl` for Excel/CSV Support

To work with Excel or CSV files in your Django app (e.g., for admin import functionality), install the `openpyxl` package:

```bash
pip install openpyxl
```

If you're also handling CSV files using Python's built-in `csv` module, no additional package is required.

> ✅ **Tip**: Add it to your `requirements.txt`:
>
> ```bash
> pip freeze > requirements.txt
> ```

---

## 📝 You're All Set!

You now have a working Django project with:

* PostgreSQL integration
* Custom applications
* Excel/CSV file support

From here, you can:

* Build models, views, and templates
* Add authentication and admin features
* Import data from spreadsheets
* Deploy your project to production

---

