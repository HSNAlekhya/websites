from django.db import models
from accounts.models import Employee

class Asset(models.Model):
    name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default="Available")

    def __str__(self):
        return self.name


class AssetRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return f"{self.employee} - {self.asset}"

# Create your models here.
