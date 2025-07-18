# django-hidp-django-admin

A Django-admin-themed template pack for [Hello, ID Please (HIdP)](https://github.com/leukeleu/django-hidp).

## Overview

This package provides Django admin-styled templates and static files for use with HIdP, allowing seamless integration of HIdP authentication flows into Django projects that use the Django admin interface.

## Features

- Django admin look and feel for HIdP authentication and account management
- Easily pluggable into existing Django projects
- Customizable templates and styles

## Installation

1. Install the package:

    ```sh
    pip install django-hidp-django-admin
    ```

2. Add `hidp_django_admin` to your `INSTALLED_APPS` **above** `hidp` and `django.contrib.admin` in your Django settings:

    ```python
    INSTALLED_APPS = [
        # ...
        "hidp_django_admin",
        "hidp",
        "django.contrib.admin",
        # ...
    ]
    ```

3. Update your `urls.py` to include the following, above the HIdP URLs:

    ```python
    from django.contrib import admin
    from django.urls import path
    from django.views.generic.base import RedirectView

    urlpatterns = [
        # ...
        path(
            "django-admin/login/",
            RedirectView.as_view(pattern_name="hidp_accounts:login"),
        ),
        path("django-admin/", admin.site.urls),
        # ...
    ]
    ```

## Development

This project comes with a sandbox environment set up for local development. Use the
provided `compose.yml` to start the sandbox. `django-hidp-django-admin`
is installed in editable mode so changes to the package are immediately reflected
in the sandbox.

Start the sandbox environment:

    ```sh
    docker compose up --build
    ```

## License

[BSD 3-Clause](LICENSE)

## Links

- [Repository](https://github.com/leukeleu/django-hidp-django-admin/)
- [Issues](https://github.com/leukeleu/django-hidp-django-admin/issues)
- [Releases](https://github.com/leukeleu/django-hidp-django-admin/releases)
