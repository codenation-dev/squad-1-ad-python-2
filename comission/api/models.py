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
    
    def calc_comission(self, seller, amount):
        sel_calc = Sellers.objects.get(id=seller)
        if amount <= sel_calc.plan.min_value:
            comission = amount * sel_calc.plan.lower_percentage / 100
        else:
            comission = amount * sel_calc.plan.upper_percentage / 100
        return round(comission, 2)
    
    def sales_month(self, seller, amount, month):
        sel_month = Sellers.object.get(id=seller)
        month_amount = Decimal(amount)
        s = Sales(sellers_id=sel_month, amount=month_amount, month=month)
        s.comission = self.calc_comission(seller, month_amount)
        s.save()
        return s.id, s.comission
