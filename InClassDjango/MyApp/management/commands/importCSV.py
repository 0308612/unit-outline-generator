import csv
from django.core.management import BaseCommand
from models import teacher

class Command(BaseCommand):
    help = "This is some help text"
    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)
    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt', encoding='utf-8-sig') as f:
            reader = csv.reader(f, dialect='excel')
            for row in reader:
                teacher.objects.create(Name=row[0], Area=row[1])
