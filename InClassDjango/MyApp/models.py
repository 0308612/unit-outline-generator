
from django.db import models
import uuid

# Create your models here.
class teacher(models.Model):
    Name = models.CharField(max_length=25)
    Area = models.CharField(max_length=30)
    VET = models.BooleanField()
    PDF_Title = models.CharField(max_length=100)
    PDF_File = models.FileField(upload_to = 'uploads/')

    def __str__(self):
        return self.PDF_Title
