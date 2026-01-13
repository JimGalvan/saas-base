# Changelog

All notable changes to Django SaaS Starter will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned Features
- Comprehensive test suite with pytest
- Docker deployment configuration
- Additional subscription plan tiers
- User profile management interface
- Email notification system
- API documentation with OpenAPI/Swagger
- Multi-language support expansion
- Advanced admin analytics dashboard

## [1.0.0] - 2026-01-12

### Added - Initial Release

#### Core Infrastructure
- Django 5.1.1 framework with multi-environment settings (development, qa, production)
- PostgreSQL database support with SQLite fallback for development
- Redis caching and session management
- Celery task queue integration for background processing
- AWS S3 integration for media file storage with boto3
- WhiteNoise for efficient static file serving
- Comprehensive environment variable configuration via .env

#### Authentication System
- Custom User model with UUID primary keys and timestamps
- Email-based authentication with django-allauth
- Google reCAPTCHA v2 integration on signup forms
- Rate limiting on authentication endpoints with django-ratelimit
- Secure password reset flow
- Optional email verification
- Login, signup, and password reset templates
- Custom authentication forms with validation

#### Subscription Management
- Stripe payment integration for subscription processing
- Customer model linking users to Stripe customer IDs
- Subscription model with plan types (FREE, PLUS) and status tracking
- Subscription utility functions for status synchronization
- Webhook infrastructure for automated Stripe event handling
- Idempotent webhook processing with deduplication
- Admin interface for subscription management
- Plan status indicators and user subscription checks

#### Maintenance Mode
- Database-backed MaintenanceMode singleton model
- Admin interface for toggling maintenance mode
- CLI management command for maintenance mode control
- Cached status checking with 60-second TTL
- Full-page and HTMX partial maintenance templates
- Middleware for maintenance mode enforcement
- Custom maintenance messages

#### Webhook System
- WebhookEvent model for comprehensive event tracking
- Stripe webhook routers for account and connect webhooks
- Signature verification with DEBUG mode bypass
- Webhook status lifecycle (RECEIVED → PROCESSING → PROCESSED/FAILED)
- Retry count tracking and error logging
- Color-coded admin interface with status badges
- Idempotency via unique constraints
- Optional Celery task processing

#### Frontend & UI
- Tailwind CSS 3.x utility-first styling via CDN
- HTMX 2.0 for dynamic HTML-over-the-wire interactions
- Alpine.js 3.x for lightweight reactive components
- Responsive mobile-first design
- Custom CSS components (buttons, cards, forms, inputs)
- Automatic flash message display and dismissal
- Base template with navigation and footer
- Landing page with hero section and features
- User dashboard with stats and quick actions
- Authentication pages (login, signup, password reset)
- Legal pages (privacy policy, terms of service)
- 404 and 500 error pages

#### Developer Experience
- Multi-environment settings architecture (base, development, qa, production)
- Comprehensive .env.example with all configuration options
- Middleware stack for security, maintenance, internationalization
- Context processors for environment, subscriptions, reCAPTCHA
- Custom management commands for common tasks
- Enhanced admin interfaces for all models
- BaseModel abstract class with UUID and timestamps
- Structured logging configuration
- Pre-configured CORS and security headers

#### Security & Compliance
- CSRF protection enabled
- Security headers (HSTS, XSS protection, content type sniffing)
- Rate limiting on authentication endpoints
- Environment-based security settings
- Django password validation
- Secure session and CSRF cookies in production
- Legal page templates for privacy and terms

#### Documentation
- Comprehensive README.md with features and quick start
- INSTALLATION.md with detailed setup instructions
- DEPLOYMENT.md with Heroku, AWS, and Docker guides
- CONTRIBUTING.md with contribution guidelines
- Detailed .env.example with all environment variables
- CHANGELOG.md for version tracking

#### Project Structure
- Apps namespace organization (apps/accounts, apps/subscription, etc.)
- Separation of concerns (core, accounts, subscription, maintenance, webhooks)
- Clean URL configuration with app-specific routing
- Template organization by app and functionality
- Static files organized by type (css, js, images)

### Technical Details

#### Dependencies
- Django 5.1.1
- django-allauth for authentication
- stripe for payment processing
- boto3 for AWS S3 integration
- django-recaptcha for bot protection
- django-ratelimit for rate limiting
- redis for caching
- celery for background tasks
- gunicorn for WSGI server
- whitenoise for static files
- psycopg2-binary for PostgreSQL

#### Database Schema
- Custom User model with UUID primary key
- Customer model with Stripe integration
- Subscription model with plan and status tracking
- MaintenanceMode singleton model
- WebhookEvent model for webhook tracking
- All models inherit from BaseModel with created_at/updated_at timestamps

#### Settings Configuration
- Base settings in config/settings/base.py
- Environment-specific overrides in development.py, qa.py, prod.py
- Environment selection via ENV variable
- Secure defaults with production hardening
- Database configuration via DATABASE_URL
- Redis configuration via REDIS_URL
- AWS S3 configuration for media storage
- Stripe API configuration
- Email backend configuration
- Security middleware enabled

### Extraction Source

This boilerplate was extracted from [NexMenus](https://nexmenus.com), a production SaaS application for restaurant website building. The extraction process involved:

1. Identifying reusable infrastructure components
2. Removing domain-specific business logic
3. Generalizing models, views, and templates
4. Creating comprehensive documentation
5. Adding example configurations
6. Preserving production-tested patterns

### Breaking Changes

N/A - Initial release

### Deprecated

N/A - Initial release

### Removed

N/A - Initial release

### Fixed

N/A - Initial release

### Security

N/A - Initial release

---

## Version History

### [1.0.0] - 2026-01-12
- Initial public release
- Extracted from NexMenus production infrastructure
- Complete Django SaaS boilerplate with authentication, subscriptions, and more

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

## Links

- [GitHub Repository](https://github.com/yourusername/django-saas-starter)
- [Issue Tracker](https://github.com/yourusername/django-saas-starter/issues)
- [Documentation](README.md)
- [Source Project: NexMenus](https://nexmenus.com)

## Legend

- `Added` - New features
- `Changed` - Changes in existing functionality
- `Deprecated` - Soon-to-be removed features
- `Removed` - Removed features
- `Fixed` - Bug fixes
- `Security` - Security fixes and improvements
