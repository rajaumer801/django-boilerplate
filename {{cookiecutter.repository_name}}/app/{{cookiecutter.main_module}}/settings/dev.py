from secure_tax.settings.base import *

INTERNAL_IPS = ['127.0.0.1']

# django-debug-toolbar
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa: F405
INSTALLED_APPS += ("debug_toolbar",)
