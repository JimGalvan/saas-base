# Contributing to Django SaaS Starter

Thank you for your interest in contributing to Django SaaS Starter! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Community](#community)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of experience level, background, or identity.

### Expected Behavior

- Be respectful and considerate in all interactions
- Provide constructive feedback
- Accept constructive criticism gracefully
- Focus on what's best for the community and project
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Personal attacks or trolling
- Publishing others' private information without permission
- Any conduct that would be inappropriate in a professional setting

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- Python 3.11 or higher
- Git installed and configured
- PostgreSQL 14+ (or SQLite for simple changes)
- Familiarity with Django framework
- Read the [README.md](README.md) and [INSTALLATION.md](INSTALLATION.md)

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork locally:**
```bash
git clone https://github.com/your-username/django-saas-starter.git
cd django-saas-starter
```

3. **Add upstream remote:**
```bash
git remote add upstream https://github.com/original-owner/django-saas-starter.git
```

4. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

5. **Install dependencies:**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If exists
```

6. **Set up pre-commit hooks (optional but recommended):**
```bash
pip install pre-commit
pre-commit install
```

### Set Up Development Environment

1. **Copy environment variables:**
```bash
cp .env.example .env
```

2. **Configure for development:**
```bash
# .env
ENV=development
DEBUG=True
SECRET_KEY=dev-secret-key-not-for-production
DISABLE_RECAPTCHA=True
```

3. **Run migrations:**
```bash
python manage.py migrate
```

4. **Create a superuser:**
```bash
python manage.py createsuperuser
```

5. **Start development server:**
```bash
python manage.py runserver
```

## Development Process

### Branching Strategy

We use a simplified Git workflow:

- `master` - Main branch, always deployable
- `feature/feature-name` - New features
- `fix/bug-name` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Creating a Branch

```bash
# Update your local master
git checkout master
git pull upstream master

# Create a new branch
git checkout -b feature/your-feature-name
```

### Making Changes

1. **Make your changes** in logical, atomic commits
2. **Write clear commit messages:**
```bash
# Good commit messages
git commit -m "Add user profile picture upload to accounts app"
git commit -m "Fix subscription status sync bug in webhooks"
git commit -m "Update README with Stripe configuration steps"

# Bad commit messages
git commit -m "Fix bug"
git commit -m "Update code"
git commit -m "WIP"
```

3. **Follow the commit message format:**
```
<type>: <subject>

<body (optional)>

<footer (optional)>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat: Add email notifications for subscription changes

- Send email when subscription is created
- Send email when subscription is cancelled
- Add email templates for notifications

Closes #123
```

### Testing Your Changes

1. **Run tests before committing:**
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.accounts

# Run with pytest (if configured)
pytest
```

2. **Check code style (if configured):**
```bash
# flake8
flake8 apps/

# black
black --check apps/

# isort
isort --check-only apps/
```

3. **Manual testing:**
- Test in browser at `http://localhost:8000`
- Verify all affected functionality works
- Test with DEBUG=False locally
- Check admin interface if applicable

### Keeping Your Branch Updated

```bash
# Fetch latest changes from upstream
git fetch upstream

# Rebase your branch
git rebase upstream/master

# If conflicts occur, resolve them and continue
git add .
git rebase --continue

# Force push to your fork (only if already pushed)
git push --force-with-lease origin feature/your-feature-name
```

## Coding Standards

### Python Style Guide

Follow [PEP 8](https://pep8.org/) style guide:

- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters (relaxed from 79)
- Use descriptive variable and function names
- Add docstrings to classes and functions
- Group imports: standard library, third-party, local

### Django Best Practices

- Use Django's built-in features when possible
- Follow Django's model field conventions
- Use class-based views appropriately
- Keep views thin, move logic to models/utils
- Use Django's ORM efficiently (avoid N+1 queries)
- Write database-agnostic code

### Code Organization

```python
# Order of class attributes in models:
class MyModel(BaseModel):
    # 1. Database fields
    name = models.CharField(max_length=255)

    # 2. Meta class
    class Meta:
        ordering = ['-created_at']

    # 3. Magic methods
    def __str__(self):
        return self.name

    # 4. Properties
    @property
    def display_name(self):
        return self.name.upper()

    # 5. Custom methods
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
```

### File Structure

- Keep apps focused and cohesive
- Use descriptive file and function names
- Separate business logic from view logic
- Keep templates organized by app
- Group related functionality

### Documentation

- Add docstrings to classes and non-obvious functions
- Update README.md when adding features
- Document configuration changes
- Include examples in docstrings
- Keep comments current with code changes

Example:
```python
def sync_subscription_status(user_id: str) -> bool:
    """
    Synchronize user's subscription status with Stripe.

    Args:
        user_id: UUID string of the user

    Returns:
        True if sync successful, False otherwise

    Raises:
        stripe.error.StripeError: If Stripe API call fails
    """
    pass
```

## Submitting Changes

### Before Submitting

- [ ] All tests pass locally
- [ ] Code follows style guidelines
- [ ] Commit messages are clear and descriptive
- [ ] Documentation is updated if needed
- [ ] No debug code or console.log statements
- [ ] No commented-out code
- [ ] Environment variables documented in .env.example

### Creating a Pull Request

1. **Push your changes:**
```bash
git push origin feature/your-feature-name
```

2. **Open a Pull Request on GitHub:**
- Go to your fork on GitHub
- Click "Pull Request" button
- Select your feature branch
- Fill out the PR template

3. **PR Title and Description:**
```markdown
## Description
Brief description of what this PR does

## Changes
- Added feature X
- Fixed bug Y
- Updated documentation Z

## Testing
- Tested locally with Python 3.11
- All tests pass
- Manually tested signup flow

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Checklist
- [x] Tests added/updated
- [x] Documentation updated
- [x] Follows coding standards
- [x] No breaking changes
```

### PR Review Process

1. **Automated checks run** (tests, linting)
2. **Maintainers review** your code
3. **Address feedback** if requested
4. **Merge** once approved

### After Merge

- Delete your feature branch locally:
```bash
git branch -d feature/your-feature-name
```

- Update your fork:
```bash
git checkout master
git pull upstream master
git push origin master
```

## Reporting Bugs

### Before Reporting

1. **Search existing issues** to avoid duplicates
2. **Try the latest version** to see if bug is fixed
3. **Test with minimal configuration** to isolate issue

### Bug Report Template

```markdown
**Description**
A clear description of the bug

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen

**Actual Behavior**
What actually happened

**Environment**
- OS: [e.g., macOS 13.0]
- Python version: [e.g., 3.11.2]
- Django version: [e.g., 5.1.1]
- Browser: [e.g., Chrome 120]

**Additional Context**
- Error messages
- Screenshots
- Logs
```

## Suggesting Features

### Before Suggesting

1. **Check if feature already exists** or is planned
2. **Search existing feature requests**
3. **Consider if feature fits project scope**

### Feature Request Template

```markdown
**Problem**
What problem does this solve?

**Proposed Solution**
How would this feature work?

**Alternatives Considered**
Other ways to solve this problem

**Benefits**
- Who benefits from this feature?
- How common is this use case?

**Implementation Ideas**
Technical approach (optional)
```

## Community

### Getting Help

- **GitHub Issues** - For bugs and feature requests
- **Discussions** - For questions and general discussion
- **Email** - For security issues only

### Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md (if created)
- Credited in release notes for significant contributions
- Thanked in commit messages and PRs

## Types of Contributions

We welcome all types of contributions:

### Code Contributions

- New features
- Bug fixes
- Performance improvements
- Code refactoring
- Test coverage improvements

### Non-Code Contributions

- Documentation improvements
- Bug reports
- Feature suggestions
- Code reviews
- Answering questions
- Tutorial writing
- Translation

## Development Tips

### Useful Commands

```bash
# Run specific tests
python manage.py test apps.accounts.tests.test_models

# Create migrations
python manage.py makemigrations

# Check for issues
python manage.py check

# Shell with Django context
python manage.py shell

# Database shell
python manage.py dbshell

# Create test data
python manage.py createsuperuser
```

### Debugging

- Use Django Debug Toolbar (if installed)
- Check logs in console
- Use `import pdb; pdb.set_trace()` for debugging
- Test with `DEBUG=True` and `DEBUG=False`
- Check database queries with Django ORM

### Common Pitfalls

- Forgetting to run migrations after model changes
- Not activating virtual environment
- Using test Stripe keys in production
- Committing `.env` file
- Not testing with PostgreSQL before submitting
- Introducing N+1 query problems

## Questions?

If you have questions about contributing:

1. Check existing documentation
2. Search closed issues
3. Ask in GitHub Discussions
4. Open a new issue with the "question" label

## License

By contributing to Django SaaS Starter, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Django SaaS Starter!
