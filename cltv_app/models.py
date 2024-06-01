from django.db import models


class CustomerData(models.Model):
    upload = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)


class CLTVResult(models.Model):
    customer_data = models.OneToOneField(CustomerData, on_delete=models.CASCADE)
    cltv = models.DecimalField(max_digits=10, decimal_places=2)
    calculated_at = models.DateTimeField(auto_now_add=True)
