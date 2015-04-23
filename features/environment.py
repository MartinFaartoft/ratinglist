import os, django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
from django.conf import settings
from django.core import management

django.setup()
    
def before_scenario(context, scenario):
    management.call_command('flush', verbosity=0, interactive=False)
    management.call_command('loaddata', 'fixtures/eight_players.json', verbosity=0)

    if not hasattr(context, 'client') or context.client is None:
        context.client = requests.session()