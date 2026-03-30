from tkinter import TRUE
from xml.etree.ElementTree import tostring
from django.db import models

# Create your models here.
class teacher(models.Model):
    Name = models.CharField(max_length=25)
    Area = models.CharField(max_length=30)
    VET = models.BooleanField()
