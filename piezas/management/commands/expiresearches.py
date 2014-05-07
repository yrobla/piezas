from django.core.management.base import BaseCommand, CommandError
from piezas import settings
from piezas.apps.catalogue.models import SearchRequest
from datetime import datetime, timedelta
from django.utils.timezone import now

class Command(BaseCommand):
    def handle(self, *args, **options):
        date_limit = now() - timedelta(seconds=5*settings.SEARCH_INTERVAL_MIN*60)
        SearchRequest.objects.filter(date_created__lt=date_limit).update(state='expired')

