from django.db import models

class SalesOrder(models.Model):
    creation_date = models.DateField()
    customer = models.CharField(max_length=255)
    currency = models.CharField(max_length=20)  # increased from 10 to 20
    order_reference = models.CharField(max_length=100, primary_key=True)
    salesperson = models.CharField(max_length=255)
    status = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    # Optional fields with updated lengths
    primary_contact = models.CharField(max_length=50, blank=True, null=True)
    finance_contact = models.CharField(max_length=50, blank=True, null=True)
    delivery_address = models.TextField(blank=True, null=True)
    invoice_address = models.TextField(blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    delivery_office_location = models.CharField(max_length=255, blank=True, null=True)
    tell_no = models.CharField(max_length=20, blank=True, null=True)  # increased from 14 to 20
    designation = models.CharField(max_length=150, blank=True, null=True)
    department = models.CharField(max_length=150, blank=True, null=True)
    lpo_confirmation_date = models.DateField(blank=True, null=True)
    lpo_date = models.DateField(blank=True, null=True)
    lpo_number = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.order_reference
