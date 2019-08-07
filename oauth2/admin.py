from django.contrib import admin

# Register your models here.
from oauth2.models import Client


admin.site.register(Client)