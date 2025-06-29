from django.db import models

class SalesOrder(models.Model):
    creation_date = models.DateField()
    customer = models.CharField(max_length=255)
    currency = models.CharField(max_length=20)
    order_reference = models.CharField(max_length=100, primary_key=True)
    salesperson = models.CharField(max_length=255)
    status = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    # Optional fields
    primary_contact = models.CharField(max_length=50, blank=True, null=True)
    finance_contact = models.CharField(max_length=50, blank=True, null=True)
    delivery_address = models.TextField(blank=True, null=True)
    invoice_address = models.TextField(blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    delivery_office_location = models.CharField(max_length=255, blank=True, null=True)
    tell_no = models.CharField(max_length=20, blank=True, null=True)
    designation = models.CharField(max_length=150, blank=True, null=True)
    department = models.CharField(max_length=150, blank=True, null=True)
    lpo_confirmation_date = models.DateField(blank=True, null=True)
    lpo_date = models.DateField(blank=True, null=True)
    lpo_number = models.CharField(max_length=100, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.order_reference} - {self.customer}"


class SalesOrderLines(models.Model):
    order_reference = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='order_lines')
    product = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    margin = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    margin_percentage = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.unit_price and self.cost:
            self.margin = self.unit_price - self.cost
            if self.unit_price != 0:
                self.margin_percentage = (self.margin / self.unit_price) * 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} ({self.order_reference})"
