# HIdP templates for Django-admin

## Overview

This package contains Django-admin-styled templates for HIdP.

## Installation

1. Install the package using pip:

```bash
pip install django-hidp-django-admin
```

2. Add the package to your `INSTALLED_APPS` in your Django settings.

Note: Make sure to add it above the `hidp` and the `django.contrib.admin` apps so that templates are loaded correctly.

```python
INSTALLED_APPS = [
    ...
    "hidp_django_admin",
    ...
]
```

3. Add the following urls to your projects `urls.py` above the `hidp_urls`.

```python
url_patterns = [
    ...
    # Hello, ID Please
    path(
        "django-admin/login/",
        RedirectView.as_view(pattern_name="hidp_accounts:login"),
    ),
    path("django-admin/", admin.site.urls),
    ...
]
