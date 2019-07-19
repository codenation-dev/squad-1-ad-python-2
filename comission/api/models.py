from django.db import models
from decimal import Decimal


class Comission_plan(models.Model):
    lower_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="lo")
    upper_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="up")
    min_value = models.DecimalField(max_digits=19, decimal_places=2,verbose_name="min")

    def __srt__(self):
        return "Plano: %s" % self.id

class Sellers(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.IntegerField()
    age = models.IntegerField()
    email = models.EmailField(max_length=100)
    cpf = models.IntegerField()
    plan = models.ForeignKey(Comission_plan, on_delete=models.CASCADE, verbose_name="plan")

    def __str__(self):
        return self.name
    
    # Envio de e-mail para vendedores abaixo da média.

class Sales(models.Model):
    month = models.IntegerField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    sellers_id = models.ForeignKey(Sellers, on_delete=models.CASCADE, primary_key=False, verbose_name="sid")
    comission = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return "%s" % self.sellers_id.name
    
    def calc_comission(self, sellers, amount, month):
        if amount <= sellers.plan.min_value:
            comission = amount * sellers.plan.lower_percentage / 100
        else:
            comission = amount * sellers.plan.upper_percentage / 100
        return round(comission, 2)
    
    def sales_month(self, sellers, amount, month):
        s = Sales(sellers, Decimal(amount), month)
        s.comission = self.calc_comission(sellers, Decimal(amount), month)
        s.save()
        return s.id
