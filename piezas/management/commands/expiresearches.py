#!/usr/bin/env python
import os
from django.core.management.base import BaseCommand, CommandError
from piezas import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "piezas.settings")
from piezas.apps.catalogue.models import SearchRequest
from datetime import datetime, timedelta
from django.utils.timezone import now

date_limit = now() - timedelta(seconds=5*settings.SEARCH_INTERVAL_MIN*60)
result = SearchRequest.objects.filter(date_created__lt=date_limit).exclude(state='expired')
result.update(state='expired')

