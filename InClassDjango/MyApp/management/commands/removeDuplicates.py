from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Min
from MyApp.models import teacher

class Command(BaseCommand):
    help = "This is some help text"
    
    def add_arguments(self, parser):
        # Set up 2 arguments so we can have a bit more control over everything
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--del', action='store_true')
    
    def handle(self, *args, **options):
        
        # Identify field to check for duplicates
        duplicate_field = 'Name' 
        
        # Find IDs of duplicates to keep (the ones with minimum PK)
        keep_ids = teacher.objects.values(duplicate_field).annotate(
            min_id=Min('id')
        ).values_list('min_id', flat=True)

        # Identify duplicates to remove
        to_delete = teacher.objects.exclude(id__in=keep_ids)
        count = to_delete.count()
        # Lists all the duplicates found
        if options['list']:
            if to_delete:
                for teach in to_delete:
                    print(teach.Name)
            else:
                print('No duplicates found')
        if options['del']:
            # Delete in an atomic transaction - Basically means do it all if it can, do nothing if it can't
            with transaction.atomic():
                to_delete.delete()
                self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} duplicate items.'))
