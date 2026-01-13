# Installation Guide

This guide will walk you through setting up Django SaaS Starter on your local development machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11 or higher** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **PostgreSQL 14+** (recommended) or SQLite for development - [Download PostgreSQL](https://www.postgresql.org/download/)
- **Redis 6+** (optional, for caching) - [Download Redis](https://redis.io/download/)

### Checking Prerequisites

Verify your installations:

```bash
python --version    # Should show Python 3.11+
git --version       # Should show git version
psql --version      # Should show PostgreSQL 14+
redis-server --version  # Should show Redis 6+
```

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/django-saas-starter.git
cd django-saas-starter
```

### 2. Create a Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt, indicating the virtual environment is active.

### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install all required packages including Django, django-allauth, Stripe SDK, boto3, and more.

### 4. Database Setup

#### Option A: PostgreSQL (Recommended for Production-like Development)

1. **Install PostgreSQL** if not already installed

2. **Create a Database:**
```bash
# Access PostgreSQL prompt
psql -U postgres

# Create database and user
CREATE DATABASE django_saas_starter;
CREATE USER saas_user WITH PASSWORD 'your_password_here';
ALTER ROLE saas_user SET client_encoding TO 'utf8';
ALTER ROLE saas_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE saas_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE django_saas_starter TO saas_user;
\q
```

3. **Set DATABASE_URL in .env:**
```bash
DATABASE_URL=postgresql://saas_user:your_password_here@localhost:5432/django_saas_starter
```

#### Option B: SQLite (Quick Start for Development)

No setup required! Django will automatically create a SQLite database file. Just make sure `DATABASE_URL` is not set in your `.env` file, and the development settings will use SQLite.

### 5. Configure Environment Variables

1. **Copy the example environment file:**
```bash
cp .env.example .env
```

2. **Edit `.env` with your configuration:**

**Minimal Configuration for Local Development:**
```bash
# Core Settings
ENV=development
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (if using PostgreSQL)
DATABASE_URL=postgresql://saas_user:your_password_here@localhost:5432/django_saas_starter

# Email (optional for local testing - uses console backend by default)
# EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Disable reCAPTCHA for local development
DISABLE_RECAPTCHA=True
```

**Generate a Secret Key:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Full Configuration (for production-like setup):**

See `.env.example` for all available options including:
- Stripe API keys (for subscription testing)
- AWS S3 credentials (for media uploads)
- Email SMTP settings (for email delivery)
- Google reCAPTCHA keys (for signup protection)
- Redis URL (for caching)

### 6. Run Database Migrations

```bash
python manage.py migrate
```

This will create all necessary database tables for:
- User authentication
- Subscriptions
- Maintenance mode
- Webhook tracking
- And more

### 7. Create a Superuser

Create an admin account to access the Django admin interface:

```bash
python manage.py createsuperuser
```

Follow the prompts to enter:
- Email address (used as username)
- Password
- Password confirmation

### 8. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

This gathers all static files (CSS, JavaScript, images) into a single location for serving.

### 9. Start the Development Server

```bash
python manage.py runserver
```

You should see output like:
```
System check identified no issues (0 silenced).
January 12, 2026 - 15:30:00
Django version 5.1.1, using settings 'config.settings.development'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### 10. Verify Installation

1. **Visit the Homepage:**
   - Open your browser to `http://localhost:8000`
   - You should see the landing page

2. **Access the Admin Interface:**
   - Go to `http://localhost:8000/admin/`
   - Log in with your superuser credentials
   - Explore the admin interface

3. **Test Authentication:**
   - Click "Sign Up" to create a test user account
   - Verify you can log in and out
   - Check the dashboard at `http://localhost:8000/dashboard/`

## Optional Setup

### Redis Cache (Recommended)

Redis improves performance by caching database queries and session data.

1. **Install Redis:**
   - macOS: `brew install redis`
   - Ubuntu: `sudo apt-get install redis-server`
   - Windows: [Download from Redis website](https://redis.io/download/)

2. **Start Redis:**
```bash
redis-server
```

3. **Configure in `.env`:**
```bash
REDIS_URL=redis://localhost:6379/0
```

### Celery for Background Tasks (Optional)

Celery handles asynchronous tasks like webhook processing and email sending.

1. **Start Redis** (Celery uses Redis as a message broker)

2. **Start Celery Worker:**
```bash
celery -A config worker -l info
```

3. **Start Celery Beat (for scheduled tasks):**
```bash
celery -A config beat -l info
```

### Stripe Integration (For Subscription Testing)

1. **Create a Stripe Account:**
   - Go to [stripe.com](https://stripe.com) and sign up
   - Navigate to Developers → API keys

2. **Get Test API Keys:**
   - Copy your test Secret key
   - Copy your test Publishable key

3. **Configure in `.env`:**
```bash
STRIPE_API_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_ACCOUNT_WEBHOOK_SECRET=whsec_... (optional, for webhooks)
```

4. **Test Webhook Locally (optional):**
```bash
# Install Stripe CLI
stripe listen --forward-to localhost:8000/webhooks/stripe/account/
```

## Troubleshooting

### Common Issues

**Issue: `ModuleNotFoundError: No module named 'django'`**
- **Solution:** Make sure your virtual environment is activated
- Run: `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows)

**Issue: Database connection errors**
- **Solution:** Verify PostgreSQL is running and credentials are correct
- Test connection: `psql -U saas_user -d django_saas_starter`

**Issue: `SECRET_KEY` errors**
- **Solution:** Make sure `.env` file exists and has a valid SECRET_KEY
- Generate a new key: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

**Issue: Static files not loading**
- **Solution:** Run `python manage.py collectstatic --noinput`
- Check that `DEBUG=True` in development

**Issue: Port 8000 already in use**
- **Solution:** Use a different port: `python manage.py runserver 8001`
- Or kill the process using port 8000

**Issue: Migration conflicts**
- **Solution:**
  ```bash
  python manage.py migrate --fake-initial
  # Or delete db.sqlite3 and run migrate again
  ```

**Issue: reCAPTCHA errors on signup**
- **Solution:** Set `DISABLE_RECAPTCHA=True` in `.env` for local development

### Getting Help

- Check the [README.md](README.md) for feature documentation
- Review [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- Open an issue on GitHub for bugs or questions

## Next Steps

Now that you have Django SaaS Starter installed:

1. **Explore the Admin Interface** - Familiarize yourself with the models and admin customizations
2. **Read the Documentation** - Review README.md for feature details
3. **Customize for Your Project** - Start adapting the boilerplate to your needs
4. **Set Up Production Environment** - When ready, see DEPLOYMENT.md

## Development Workflow

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Start development server
python manage.py runserver

# In another terminal, start Redis (optional)
redis-server

# In another terminal, start Celery (optional)
celery -A config worker -l info
```

## Verification Checklist

- [ ] Python 3.11+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed from requirements.txt
- [ ] `.env` file created and configured
- [ ] Database migrations applied
- [ ] Superuser created
- [ ] Static files collected
- [ ] Development server starts without errors
- [ ] Can access homepage at http://localhost:8000
- [ ] Can access admin at http://localhost:8000/admin/
- [ ] Can sign up and log in as a test user

Congratulations! You now have Django SaaS Starter running locally.
