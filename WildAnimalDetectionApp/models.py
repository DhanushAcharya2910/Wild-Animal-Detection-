from django.db import models

# Create your models here.
class User(models.Model):

    class Meta:
        db_table = 'user'

    name = models.CharField(blank=False, max_length=50)
    contact = models.CharField(blank=False, max_length=50)
    email = models.CharField(blank=False, max_length=50)
    address = models.CharField(blank=False, max_length=250)
    user_name = models.CharField(blank=False, max_length=25, default=None)
    password = models.CharField(max_length=10, blank=False, default=None)
