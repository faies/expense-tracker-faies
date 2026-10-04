from django.db import models

# Create your models here.
class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    category = models.CharField(max_length=50)
    date = models.DateField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.description