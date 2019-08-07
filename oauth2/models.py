from django.db import models


# Create your models here.
class Client(models.Model):
    client_name = models.TextField(null=False, blank=False, default="Unknown")
    client_id = models.TextField(null=False, blank=False, max_length=200)
    client_secret = models.TextField(null=False, blank=False, max_length=200)

    def __str__(self):
        return f"{self.client_name}({self.client_id})"
