from django.db import models


# Create your models here.
class Client(models.Model):
    client_id = models.TextField(null=False, blank=False, max_length=200)
    client_secret = models.TextField(null=False, blank=False, max_length=200)
