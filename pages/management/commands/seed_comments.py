from django.core.management.base import BaseCommand
from pages.factories import CommentFactory

class Command(BaseCommand):
    help = 'Seed the database with sample comments'

    def handle(self, *args, **kwargs):
        CommentFactory.create_batch(20)
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with comments'))
