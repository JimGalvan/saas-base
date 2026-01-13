# Deployment Guide

This guide covers deploying Django SaaS Starter to production environments including Heroku, AWS, and Docker.

## Table of Contents

- [Pre-Deployment Checklist](#pre-deployment-checklist)
- [Environment Configuration](#environment-configuration)
- [Heroku Deployment](#heroku-deployment)
- [AWS Deployment](#aws-deployment)
- [Docker Deployment](#docker-deployment)
- [Post-Deployment](#post-deployment)
- [Security Hardening](#security-hardening)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Pre-Deployment Checklist

Before deploying to production, ensure you have:

- [ ] Set `ENV=production` in environment variables
- [ ] Set `DEBUG=False`
- [ ] Generated a strong, unique `SECRET_KEY`
- [ ] Configured production database (PostgreSQL)
- [ ] Set up AWS S3 for media file storage
- [ ] Configured email backend (SendGrid, AWS SES, etc.)
- [ ] Set up Stripe webhook endpoints
- [ ] Configured allowed hosts
- [ ] Enabled HTTPS/SSL certificates
- [ ] Set up Redis for caching and sessions
- [ ] Configured error logging (Sentry, etc.)
- [ ] Reviewed security settings
- [ ] Tested all critical functionality
- [ ] Backed up database

## Environment Configuration

### Production Settings

Create a `.env` file with production values:

```bash
# Core Settings
ENV=production
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (PostgreSQL required for production)
DATABASE_URL=postgresql://username:password@host:5432/database

# Redis
REDIS_URL=redis://your-redis-host:6379/0

# AWS S3 (Required for production media storage)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
AWS_S3_CUSTOM_DOMAIN=your-bucket-name.s3.amazonaws.com

# Email (SendGrid example)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Stripe
STRIPE_API_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_ACCOUNT_WEBHOOK_SECRET=whsec_...
STRIPE_CONNECT_WEBHOOK_SECRET=whsec_...

# reCAPTCHA
RECAPTCHA_PUBLIC_KEY=your-site-key
RECAPTCHA_PRIVATE_KEY=your-secret-key
DISABLE_RECAPTCHA=False

# Security
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Logging (optional - Sentry)
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
```

### Generate Secure Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

## Heroku Deployment

### Prerequisites

- Heroku CLI installed: `brew install heroku/brew/heroku` or [download](https://devcenter.heroku.com/articles/heroku-cli)
- Heroku account created

### Step-by-Step Deployment

1. **Login to Heroku:**
```bash
heroku login
```

2. **Create a Heroku App:**
```bash
heroku create your-app-name
```

3. **Add PostgreSQL Database:**
```bash
heroku addons:create heroku-postgresql:essential-0
```

4. **Add Redis:**
```bash
heroku addons:create heroku-redis:mini
```

5. **Set Environment Variables:**
```bash
heroku config:set ENV=production
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
heroku config:set DISABLE_COLLECTSTATIC=1

# AWS S3
heroku config:set AWS_ACCESS_KEY_ID="your-key"
heroku config:set AWS_SECRET_ACCESS_KEY="your-secret"
heroku config:set AWS_STORAGE_BUCKET_NAME="your-bucket"
heroku config:set AWS_S3_REGION_NAME="us-east-1"

# Stripe
heroku config:set STRIPE_API_KEY="sk_live_..."
heroku config:set STRIPE_PUBLISHABLE_KEY="pk_live_..."

# Email
heroku config:set EMAIL_HOST_USER="your-email-user"
heroku config:set EMAIL_HOST_PASSWORD="your-email-password"

# reCAPTCHA
heroku config:set RECAPTCHA_PUBLIC_KEY="your-site-key"
heroku config:set RECAPTCHA_PRIVATE_KEY="your-secret-key"
```

6. **Create Procfile:**
```bash
# Procfile already exists in the repo with:
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A config worker --loglevel=info
```

7. **Deploy to Heroku:**
```bash
git push heroku master
```

8. **Run Migrations:**
```bash
heroku run python manage.py migrate
```

9. **Create Superuser:**
```bash
heroku run python manage.py createsuperuser
```

10. **Collect Static Files:**
```bash
heroku run python manage.py collectstatic --noinput
```

11. **Scale Dynos:**
```bash
# Scale web dyno
heroku ps:scale web=1

# Scale worker dyno (optional, for Celery)
heroku ps:scale worker=1
```

12. **Configure Stripe Webhooks:**
- Go to Stripe Dashboard → Developers → Webhooks
- Add endpoint: `https://your-app-name.herokuapp.com/webhooks/stripe/account/`
- Select events to listen for
- Copy webhook signing secret and set: `heroku config:set STRIPE_ACCOUNT_WEBHOOK_SECRET="whsec_..."`

13. **Open Your App:**
```bash
heroku open
```

### Heroku Maintenance Mode

```bash
# Enable Heroku maintenance mode
heroku maintenance:on

# Disable Heroku maintenance mode
heroku maintenance:off
```

## AWS Deployment

### Architecture Overview

- **EC2** - Application server running Gunicorn
- **RDS** - PostgreSQL database
- **ElastiCache** - Redis cache
- **S3** - Static and media file storage
- **CloudFront** - CDN for static assets
- **ALB** - Application Load Balancer
- **ACM** - SSL certificate management

### Prerequisites

- AWS account with appropriate permissions
- AWS CLI configured
- Domain name configured in Route 53

### Deployment Steps

1. **Create RDS PostgreSQL Instance:**
```bash
# Via AWS Console or CLI
aws rds create-db-instance \
    --db-instance-identifier saas-starter-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username admin \
    --master-user-password YourPassword \
    --allocated-storage 20
```

2. **Create ElastiCache Redis Cluster:**
```bash
aws elasticache create-cache-cluster \
    --cache-cluster-id saas-starter-redis \
    --cache-node-type cache.t3.micro \
    --engine redis \
    --num-cache-nodes 1
```

3. **Create S3 Bucket:**
```bash
aws s3 mb s3://your-saas-starter-bucket
aws s3api put-public-access-block \
    --bucket your-saas-starter-bucket \
    --public-access-block-configuration \
    BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```

4. **Configure S3 CORS:**
```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "HEAD"],
        "AllowedOrigins": ["https://yourdomain.com"],
        "ExposeHeaders": []
    }
]
```

5. **Launch EC2 Instance:**
- Ubuntu 22.04 LTS
- t3.small or larger
- Security group allowing HTTP (80), HTTPS (443), SSH (22)

6. **Install Dependencies on EC2:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip postgresql-client nginx supervisor -y
```

7. **Deploy Application:**
```bash
# Clone repository
git clone https://github.com/yourusername/django-saas-starter.git
cd django-saas-starter

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Set environment variables (create .env file)
nano .env

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser
```

8. **Configure Gunicorn with Supervisor:**
```ini
# /etc/supervisor/conf.d/saas-starter.conf
[program:saas-starter]
directory=/home/ubuntu/django-saas-starter
command=/home/ubuntu/django-saas-starter/venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 3
user=ubuntu
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/saas-starter.log
```

9. **Configure Nginx:**
```nginx
# /etc/nginx/sites-available/saas-starter
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/ubuntu/django-saas-starter/staticfiles/;
    }
}
```

10. **Enable Site and Restart Services:**
```bash
sudo ln -s /etc/nginx/sites-available/saas-starter /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start saas-starter
```

11. **Configure SSL with Let's Encrypt:**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## Docker Deployment

### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: django_saas
      POSTGRES_USER: django
      POSTGRES_PASSWORD: change-me
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis

  worker:
    build: .
    command: celery -A config worker --loglevel=info
    volumes:
      - .:/app
    env_file:
      - .env
    depends_on:
      - db
      - redis

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
```

### Deploy with Docker Compose

```bash
# Build and start services
docker-compose up -d --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# View logs
docker-compose logs -f web
```

## Post-Deployment

### Verification Checklist

- [ ] Site loads over HTTPS
- [ ] Static files load correctly
- [ ] Media uploads work (S3)
- [ ] User signup and login work
- [ ] Email sending works
- [ ] Stripe webhooks receive events
- [ ] Admin interface accessible
- [ ] reCAPTCHA works on signup
- [ ] Rate limiting works on auth endpoints
- [ ] Maintenance mode toggles correctly

### Configure Stripe Webhooks

1. Go to Stripe Dashboard → Developers → Webhooks
2. Add endpoint: `https://yourdomain.com/webhooks/stripe/account/`
3. Select events:
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.paid`
   - `invoice.payment_failed`
4. Copy webhook signing secret
5. Set in environment: `STRIPE_ACCOUNT_WEBHOOK_SECRET=whsec_...`

### Test Webhook Delivery

```bash
# Using Stripe CLI
stripe trigger customer.subscription.created
```

## Security Hardening

### Django Security Settings

Ensure these are enabled in production settings:

```python
# config/settings/prod.py
DEBUG = False
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'
```

### Security Checklist

- [ ] Run `python manage.py check --deploy`
- [ ] Disable DEBUG in production
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS everywhere
- [ ] Configure HSTS headers
- [ ] Enable CSRF protection
- [ ] Use secure session cookies
- [ ] Configure CORS properly
- [ ] Keep dependencies updated
- [ ] Use strong database passwords
- [ ] Restrict admin access by IP (optional)
- [ ] Enable rate limiting
- [ ] Configure Content Security Policy
- [ ] Regular security audits

### Run Security Check

```bash
python manage.py check --deploy
```

## Monitoring

### Logging

Configure structured logging in production:

```python
# config/settings/prod.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/saas-starter.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}
```

### Error Tracking (Sentry)

1. **Install Sentry SDK:**
```bash
pip install sentry-sdk
```

2. **Configure in settings:**
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=False,
    environment=os.environ.get('ENV', 'production'),
)
```

### Performance Monitoring

- Set up application performance monitoring (APM)
- Monitor database query performance
- Track Celery task execution
- Monitor Redis memory usage
- Set up uptime monitoring (Pingdom, UptimeRobot)

## Troubleshooting

### Static Files Not Loading

```bash
# Check static files are collected
python manage.py collectstatic --noinput

# Verify STATIC_ROOT is correct
python manage.py findstatic admin/css/base.css

# Check nginx configuration serves static files
curl https://yourdomain.com/static/css/main.css
```

### Database Connection Issues

```bash
# Test database connection
python manage.py dbshell

# Check DATABASE_URL format
echo $DATABASE_URL

# Verify security group allows connections
```

### Celery Not Processing Tasks

```bash
# Check Celery logs
heroku logs --tail --dyno worker  # Heroku
sudo tail -f /var/log/celery.log  # EC2

# Test Celery connection
celery -A config inspect ping

# Check Redis connection
redis-cli ping
```

### SSL/HTTPS Issues

```bash
# Test SSL certificate
openssl s_client -connect yourdomain.com:443

# Check SSL redirect
curl -I http://yourdomain.com

# Verify SECURE_SSL_REDIRECT is enabled
```

### High Memory Usage

```bash
# Check running processes
heroku ps  # Heroku
top        # EC2/Docker

# Optimize Gunicorn workers
# Workers = (2 x CPU cores) + 1

# Enable connection pooling for database
# Add ?pool=true to DATABASE_URL
```

## Backup and Recovery

### Database Backups

**Heroku:**
```bash
heroku pg:backups:capture
heroku pg:backups:download
```

**AWS RDS:**
- Enable automated backups (7-35 days retention)
- Create manual snapshots before major changes

### Media File Backups

- Enable S3 versioning
- Configure S3 lifecycle policies
- Set up cross-region replication (optional)

### Disaster Recovery Plan

1. Document all environment variables
2. Keep database backups (automated + manual)
3. Version control all code
4. Document infrastructure setup
5. Test recovery procedures regularly

---

## Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/)
- [Heroku Django Guide](https://devcenter.heroku.com/articles/django-app-configuration)
- [AWS EC2 Best Practices](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-best-practices.html)
- [Docker Django Guide](https://docs.docker.com/samples/django/)
- [Let's Encrypt Certbot](https://certbot.eff.org/)

For issues or questions, open an issue on GitHub.
