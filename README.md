# Django SaaS Starter

A production-ready Django SaaS boilerplate extracted from real-world infrastructure. Built with Django 5.1, this starter includes everything you need to launch a subscription-based SaaS application.

## 🌟 Features

### Core Infrastructure
- **Django 5.1.1** - Latest stable Django framework
- **PostgreSQL** - Production-grade database
- **Redis** - Caching and message broker
- **Celery** - Async task processing
- **AWS S3** - Scalable media storage
- **WhiteNoise** - Efficient static file serving

### Authentication & User Management
- **django-allauth** - Email-based authentication
- **Custom User Model** - UUID primary keys for distributed systems
- **reCAPTCHA Integration** - Bot protection on signup
- **Rate Limiting** - Comprehensive protection on auth endpoints
- **Security Headers** - HSTS, XSS, CSRF protection

### Subscription Management
- **Stripe Integration** - Complete payment processing
- **Webhook Handling** - Automated subscription sync
- **Plan Management** - Flexible subscription tiers
- **Customer Portal** - Self-service subscription management

### Developer Experience
- **Multi-Environment Settings** - Development, QA, Production configs
- **Maintenance Mode** - Database-backed with admin toggle
- **Internationalization** - i18n/l10n support (English/Spanish)
- **HTMX Integration** - Modern dynamic interactions
- **Admin Interface** - Customized Django admin

### Production Ready
- **Heroku Deployment** - Ready for Heroku with Procfile
- **Sentry Integration** - Error tracking and monitoring
- **Email Backend** - Configured for SendGrid/SMTP
- **Security Hardening** - Environment-aware security settings

## 📋 Requirements

- Python 3.11+
- PostgreSQL 14+
- Redis 6+
- AWS S3 bucket (for media storage in production)
- Stripe account (for subscriptions)

## 🚀 Quick Start

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

### 4. Environment Configuration

Copy the example environment file and configure:

```bash
cp .env.example .env
```

Edit `.env` with your settings (see Configuration section below).

### 5. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to see your application!

## ⚙️ Configuration

Key environment variables to configure in `.env`:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ENV=development
BASE_URL=http://localhost:8000

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Redis
REDIS_URL=redis://localhost:6379/0

# AWS S3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1

# Stripe
STRIPE_API_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_ACCOUNT_WEBHOOK_SECRET=whsec_...

# reCAPTCHA
RECAPTCHA_PUBLIC_KEY=your-site-key
RECAPTCHA_PRIVATE_KEY=your-secret-key
```

See `.env.example` for complete configuration options.

## 📁 Project Structure

```
django-saas-starter/
├── config/                 # Main project configuration
│   ├── settings/          # Environment-specific settings
│   │   ├── base.py       # Base settings
│   │   ├── development.py
│   │   ├── qa.py
│   │   └── prod.py
│   ├── urls.py
│   └── wsgi.py
├── apps/                  # Django applications
│   ├── core/             # Core utilities (Phase 2)
│   ├── accounts/         # User management (Phase 3)
│   ├── subscription/     # Stripe integration (Phase 4)
│   ├── maintenance/      # Maintenance mode (Phase 5)
│   └── webhooks/         # Webhook handlers (Phase 6)
├── templates/            # HTML templates
├── static/              # Static assets (CSS, JS, images)
├── locale/              # i18n translation files
├── docs/                # Documentation
└── requirements.txt     # Python dependencies
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with browser UI (for Playwright tests)
pytest --headed

# Run specific test file
pytest tests/test_authentication.py
```

## 📚 Documentation

Detailed documentation is available in the `docs/` directory:

- [Installation Guide](docs/INSTALLATION.md) - Detailed setup instructions
- [Configuration Guide](docs/CONFIGURATION.md) - All environment variables explained
- [Stripe Setup](docs/STRIPE_SETUP.md) - Stripe integration walkthrough
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment instructions
- [Customization Guide](docs/CUSTOMIZATION.md) - How to customize for your needs

## 🔧 Development Commands

```bash
# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Start Celery worker
celery -A config worker -l info

# Toggle maintenance mode
python manage.py maintenance_mode on|off
```

## 🚢 Deployment

This project is optimized for Heroku deployment but can be deployed to any platform that supports Django.

### Heroku Deployment

```bash
# Install Heroku CLI and login
heroku login

# Create Heroku app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Add Redis
heroku addons:create heroku-redis:mini

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ENV=production
# ... (see docs/DEPLOYMENT.md for complete list)

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed deployment instructions.

## 🎨 Customization

This is a boilerplate - customize it for your needs:

1. **Branding**: Update templates, logo, colors, site name
2. **Features**: Add your app-specific functionality in `apps/`
3. **Subscription Plans**: Configure your pricing in Stripe dashboard
4. **Email Templates**: Customize in `templates/account/email/`
5. **Landing Page**: Update `templates/home.html`

See [docs/CUSTOMIZATION.md](docs/CUSTOMIZATION.md) for detailed guidance.

## 🛡️ Security

This boilerplate includes production-ready security:

- HTTPS enforcement in production
- Secure session cookies
- CSRF protection
- XSS prevention
- Rate limiting on authentication
- Security headers (HSTS, X-Frame-Options, etc.)
- reCAPTCHA bot protection

Always review and test security settings before production deployment.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

This boilerplate was extracted from [NexMenus](https://github.com/yourusername/NexMenus), a production SaaS application. It represents real-world, battle-tested infrastructure.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Support

- **Documentation**: Check the `docs/` directory
- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions

---

**Status**: 🚧 In Development - Phase 1 Complete

This project is being actively developed. See [SAAS_EXTRACTION_PLAN.md](SAAS_EXTRACTION_PLAN.md) for the development roadmap.
