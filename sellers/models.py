from django.db import models

class Comission_plan(models.Model):
    lower_percentage = models.DecimalField(max_digits=3, decimal_places=2)
    upper_percentage = models.DecimalField(max_digits=3, decimal_places=2)
    min_value = models.DecimalField(max_digits=10, decimal_places=2)

class Sellers(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.IntegerField()
    age = models.IntegerField()
    email = models.CharField(max_length=100)
    cpf = models.IntegerField()
    comission_id = models.ForeignKey(Comission_plan, on_delete=models.CASCADE)

class Sales(models.Model):
    month = models.IntegerField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    seller_id = models.ForeignKey(Sellers, on_delete=models.CASCADE)
    comission = models.DecimalField(max_digits=20, decimal_places=2)

