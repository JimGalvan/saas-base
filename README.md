# Django SaaS Starter 🚀

A production-ready Django SaaS boilerplate extracted from real-world infrastructure. Built with Django 5.1, this starter includes everything you need to launch a subscription-based SaaS application quickly and securely.

[![Django](https://img.shields.io/badge/Django-5.1-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ What's Included

This boilerplate is extracted from a production SaaS application and includes:

- 🔐 **Complete Authentication System** - Email-based auth with django-allauth
- 💳 **Stripe Subscriptions** - Full subscription management with webhooks
- 🎨 **Modern UI** - Tailwind CSS with HTMX and Alpine.js
- 🔧 **Admin Tools** - Maintenance mode, webhook logging, comprehensive admin
- 📊 **Observability** - Structured logging, error tracking ready
- 🌍 **Internationalization** - Multi-language support built-in
- 🚀 **Production Ready** - Security hardened, environment configs, deployment ready

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Apps Overview](#apps-overview)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Features

### Core Infrastructure
- **Django 5.1.1** - Latest stable Django framework with modern features
- **PostgreSQL** - Production-grade relational database
- **Redis** - Caching layer and message broker
- **Celery** (optional) - Async task processing for webhooks and background jobs
- **AWS S3** - Scalable media file storage with boto3
- **WhiteNoise** - Efficient static file serving

### Authentication & User Management
- **Custom User Model** - UUID primary keys, timestamps, subscription integration
- **django-allauth** - Robust email-based authentication
- **reCAPTCHA** - Bot protection on signup forms
- **Rate Limiting** - django-ratelimit on auth endpoints
- **Password Reset** - Secure email-based password recovery
- **Email Verification** - Optional email confirmation flow

### Subscription Management
- **Stripe Integration** - Complete payment processing with Stripe API
- **Customer Model** - Links users to Stripe customer IDs
- **Subscription Model** - Tracks plan type, status, payment history
- **Webhook Handling** - Automated sync with Stripe events
- **Plan Management** - FREE/PLUS tiers (easily customizable)
- **Idempotency** - Webhook deduplication and retry logic

### Maintenance & Operations
- **Maintenance Mode** - Database-backed singleton with admin toggle
- **CLI Command** - `python manage.py maintenance_mode --enable/--disable`
- **Cache Integration** - 60-second TTL for performance
- **Custom Templates** - Full-page and HTMX partial maintenance pages

### Webhook Infrastructure
- **WebhookEvent Model** - Comprehensive webhook tracking
- **Stripe Routers** - Separate handlers for account and connect webhooks
- **Signature Verification** - Production-safe with DEBUG mode bypass
- **Status Tracking** - RECEIVED → PROCESSING → PROCESSED/FAILED
- **Admin Interface** - Color-coded status badges for debugging
- **Async Processing** - Celery task examples included

### UI & Frontend
- **Tailwind CSS** - Utility-first CSS framework via CDN
- **HTMX** - Dynamic interactions without JavaScript frameworks
- **Alpine.js** - Lightweight JavaScript for reactive components
- **Responsive Design** - Mobile-first approach
- **Custom Components** - Buttons, cards, forms, inputs with consistent styling
- **Flash Messages** - Automatic display and dismissal

### Developer Experience
- **Multi-Environment Settings** - base, development, qa, production configs
- **Environment Variables** - `.env.example` with all required variables
- **Middleware Stack** - Security, maintenance, i18n, HTMX support
- **Context Processors** - Environment, subscription, reCAPTCHA helpers
- **Management Commands** - Custom commands for common tasks
- **Admin Customization** - Enhanced admin interfaces for all models

### Security & Compliance
- **CSRF Protection** - Django CSRF middleware enabled
- **Security Headers** - HSTS, XSS protection, content type sniffing protection
- **Rate Limiting** - Protection against brute force attacks
- **Environment Isolation** - DEBUG-aware security settings
- **Password Validation** - Django's comprehensive password validators
- **Legal Templates** - Privacy policy and terms of service pages

## 🛠 Tech Stack

### Backend
- **Django 5.1.1** - Web framework
- **Python 3.11+** - Programming language
- **PostgreSQL 14+** - Database
- **Redis 6+** - Cache & message broker

### Frontend
- **Tailwind CSS 3.x** - Utility-first CSS
- **HTMX 2.0** - HTML-over-the-wire
- **Alpine.js 3.x** - Minimal JavaScript framework

### Infrastructure
- **Gunicorn** - WSGI HTTP Server
- **WhiteNoise** - Static file serving
- **boto3** - AWS SDK for S3
- **Celery** - Task queue (optional)

### Third-Party Services
- **Stripe** - Payment processing
- **AWS S3** - Media storage
- **SendGrid/SMTP** - Email delivery
- **Google reCAPTCHA** - Bot protection

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- PostgreSQL 14 or higher (or SQLite for development)
- Redis 6 or higher (optional, for caching)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/django-saas-starter.git
cd django-saas-starter
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to see your application!

## 📁 Project Structure

```
django-saas-starter/
├── apps/
│   ├── accounts/          # User authentication & management
│   │   ├── models.py      # Custom User model
│   │   ├── forms.py       # Auth forms with reCAPTCHA
│   │   ├── adapters.py    # Allauth customization
│   │   └── admin.py       # User admin interface
│   ├── core/              # Core utilities & base models
│   │   ├── models.py      # BaseModel with UUID & timestamps
│   │   ├── middleware.py  # Maintenance, i18n, Firebase
│   │   ├── storage.py     # S3 storage backend
│   │   ├── utils.py       # Common utilities
│   │   ├── context_processors.py  # Template context
│   │   └── views.py       # Core views (home, dashboard)
│   ├── subscription/      # Stripe subscription management
│   │   ├── models.py      # Customer, Subscription models
│   │   ├── enums.py       # PlanType, SubscriptionStatus
│   │   ├── utils.py       # Stripe helper functions
│   │   └── admin.py       # Subscription admin
│   ├── maintenance/       # Maintenance mode system
│   │   ├── models.py      # MaintenanceMode singleton
│   │   ├── admin.py       # Admin toggle interface
│   │   └── management/commands/  # CLI commands
│   └── webhooks/          # Webhook handling infrastructure
│       ├── models.py      # WebhookEvent tracking
│       ├── handlers.py    # Stripe webhook routers
│       └── admin.py       # Webhook admin interface
├── config/
│   ├── settings/          # Environment-specific settings
│   │   ├── base.py        # Shared settings
│   │   ├── development.py # Local development
│   │   ├── qa.py          # QA environment
│   │   └── prod.py        # Production settings
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI configuration
├── templates/
│   ├── base.html          # Base template with navigation
│   ├── home.html          # Landing page
│   ├── dashboard.html     # User dashboard
│   ├── account/           # Authentication templates
│   ├── legal/             # Privacy & terms pages
│   └── maintenance/       # Maintenance mode templates
├── static/
│   ├── css/               # Custom stylesheets
│   ├── js/                # Custom JavaScript
│   └── favicon/           # Favicon files
├── requirements.txt       # Python dependencies
├── manage.py              # Django management script
├── .env.example           # Environment variables template
└── README.md              # This file
```

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

**Core Settings**
```bash
ENV=development  # development, qa, production
SECRET_KEY=your-secret-key-here
DEBUG=True  # False in production
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Database**
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
# Or use SQLite for development
```

**Stripe**
```bash
STRIPE_API_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_ACCOUNT_WEBHOOK_SECRET=whsec_...
STRIPE_CONNECT_WEBHOOK_SECRET=whsec_...
```

**AWS S3**
```bash
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

**Email**
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

**reCAPTCHA**
```bash
RECAPTCHA_PUBLIC_KEY=your-site-key
RECAPTCHA_PRIVATE_KEY=your-secret-key
DISABLE_RECAPTCHA=False  # True for development
```

## 📦 Apps Overview

### Core App
Base utilities, models, middleware, and context processors used across the project.

**Key Components:**
- `BaseModel` - Abstract model with UUID, created_at, updated_at
- `MaintenanceModeMiddleware` - Handles maintenance mode
- `S3MediaStorage` - Custom S3 storage backend
- Context processors for environment, subscriptions, reCAPTCHA

### Accounts App
User authentication and account management.

**Key Components:**
- Custom `User` model with UUID primary key
- `CaptchaSignupForm` - Signup with reCAPTCHA
- `CustomLoginForm` - Login with improved error messages
- `AccountAdapter` - Allauth customization

### Subscription App
Stripe subscription management and billing.

**Key Components:**
- `Customer` model - Links users to Stripe
- `Subscription` model - Tracks plans and status
- Utility functions for syncing with Stripe
- Admin interface for subscription management

### Maintenance App
Site-wide maintenance mode control.

**Key Components:**
- `MaintenanceMode` singleton model
- Admin interface with visual indicators
- CLI management command
- Cached status checking for performance

### Webhooks App
Webhook event handling and tracking.

**Key Components:**
- `WebhookEvent` model - Stores webhook payloads
- Stripe webhook routers (account & connect)
- Idempotency checking
- Admin interface with color-coded status badges

## 💻 Development

### Running Tests
```bash
pytest
# With coverage
pytest --cov=apps
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Maintenance Mode
```bash
# Enable maintenance mode
python manage.py maintenance_mode --enable

# Disable maintenance mode
python manage.py maintenance_mode --disable

# Check status
python manage.py maintenance_mode --status

# Custom message
python manage.py maintenance_mode --enable --message "Upgrading database"
```

### Collecting Static Files
```bash
python manage.py collectstatic --noinput
```

### Running Celery (Optional)
```bash
# Worker
celery -A config worker -l info

# Beat (for scheduled tasks)
celery -A config beat -l info
```

## 🚢 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions including:
- Heroku deployment
- AWS deployment
- Docker deployment
- Environment configuration
- Security checklist

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

This boilerplate was extracted from production infrastructure at NexMenus, a restaurant website builder SaaS platform.

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [django-allauth Documentation](https://django-allauth.readthedocs.io/)
- [Stripe API Documentation](https://stripe.com/docs/api)
- [HTMX Documentation](https://htmx.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

## 💬 Support

For questions, issues, or feature requests, please open an issue on GitHub.

---

**Built with ❤️ using Django**
