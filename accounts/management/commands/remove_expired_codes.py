from django.core.management.base import BaseCommand
from django.db.models.functions import Now

from accounts.models import OtpModel


class Command(BaseCommand):
    help = 'Remove expired codes'

    def handle(self, *args, **options):
        OtpModel._base_manager.filter(expiration_time__gte=Now()).delete()
