from django.db import models
from phone_field import PhoneField

# Create your models here.
class Notifier(models.Model):
    phone = PhoneField(blank=True, help_text='Contact phone number', null=True)
    