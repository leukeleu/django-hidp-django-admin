# HIdP templates for Django-admin

## Overview

This package contains Django-admin-styled templates for HIdP.

## Installation

1. Install the package using pip:

```bash
pip install django-hidp-django-admin
```

2. Add the package to your `INSTALLED_APPS` in your Django settings:

```python
INSTALLED_APPS = [
    ...
    # Hello, ID Please
    path(
        "django-admin/login/",
        RedirectView.as_view(pattern_name="hidp_accounts:login"),
    ),
    "hidp_django_admin",  # Should be above "hidp" for templates to work
]
```