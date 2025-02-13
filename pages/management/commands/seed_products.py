from django.core.management.base import BaseCommand
from pages.factories import ProductFactory

class Command(BaseCommand):
    help = 'Seed the database with sample products'

    def handle(self, *args, **kwargs):
        ProductFactory.create_batch(20)
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with products'))
