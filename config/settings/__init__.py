"""
Settings package for Django SaaS Starter

Auto-loads environment-specific settings based on the ENV environment variable:
- ENV=development → development.py (default)
- ENV=qa → qa.py
- ENV=production → prod.py
"""
import os

# Determine which settings to use based on ENV environment variable
env = os.environ.get('ENV', 'development').lower()

if env == 'production':
    from .prod import *
elif env == 'qa':
    from .qa import *
else:
    # Default to development settings
    from .development import *

print(f"[Settings] Loaded configuration for: {env.upper()}")
