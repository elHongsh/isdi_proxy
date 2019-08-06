from django.db import models


# Create your models here.
class ContractLog(models.Model):
    contract_name = models.TextField(max_length=100, null=False, blank=False)
    abi = models.TextField(max_length=100_000, null=False, blank=False)
    bytecode = models.TextField(max_length=100_000, null=False, blank=False)
    address = models.TextField(max_length=42, null=False, blank=False)

    def __str__(self):
        return f"{self.contract_name} (abi: {len(self.abi)}, bytecode: {len(self.bytecode)})"
