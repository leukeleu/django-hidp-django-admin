import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hidp_django_admin_sandbox.settings")

application = get_wsgi_application()
