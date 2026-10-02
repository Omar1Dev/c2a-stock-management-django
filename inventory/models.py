from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    initial_quantity = models.PositiveIntegerField()
    current_quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    LOW_STOCK_PERCENTAGE = 10

    @property
    def low_stock_threshold(self):
        return self.initial_quantity * self.LOW_STOCK_PERCENTAGE / 100

    @property
    def status(self):

        if self.current_quantity == 0:
            return "Out of Stock"

        if self.current_quantity <= self.low_stock_threshold:
            return "Low Stock"

        return "In Stock"

    def __str__(self):
        return self.name