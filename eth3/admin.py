from django.contrib import admin

# Register your models here.
from eth3.models import ContractLog

admin.site.register(ContractLog)