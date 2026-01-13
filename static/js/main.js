// Django SaaS Starter - Main JavaScript

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('Django SaaS Starter initialized');

    // Auto-dismiss messages after 5 seconds
    const messages = document.querySelectorAll('[role="alert"]');
    messages.forEach(function(message) {
        setTimeout(function() {
            message.style.transition = 'opacity 0.5s';
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 500);
        }, 5000);
    });
});

// HTMX configuration
document.body.addEventListener('htmx:configRequest', function(event) {
    // Add CSRF token to HTMX requests
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfToken) {
        event.detail.headers['X-CSRFToken'] = csrfToken.value;
    }
});

// Handle HTMX errors
document.body.addEventListener('htmx:responseError', function(event) {
    console.error('HTMX Error:', event.detail);
    alert('An error occurred. Please try again.');
});

// Utility functions
window.SaaSStarter = {
    // Show loading indicator
    showLoading: function(element) {
        element.classList.add('opacity-50', 'pointer-events-none');
    },

    // Hide loading indicator
    hideLoading: function(element) {
        element.classList.remove('opacity-50', 'pointer-events-none');
    },

    // Copy to clipboard
    copyToClipboard: function(text) {
        navigator.clipboard.writeText(text).then(function() {
            alert('Copied to clipboard!');
        });
    }
};
