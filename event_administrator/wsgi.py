import os

from django.core.wsgi import get_wsgi_application

from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_administrator.settings.dev")

application = get_wsgi_application()
