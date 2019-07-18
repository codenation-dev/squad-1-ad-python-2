from django.db import models

class Sellers(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.IntegerField()
    age = models.IntegerField()
    email = models.EmailField(max_length=100)
    cpf = models.IntegerField()
    plan = models.IntegerField()

    def __str__(self):
        return self.name

class Comission_plan(models.Model):
    comission_plan = models.IntegerField()
    sellers_id = models.ForeignKey(Sellers, on_delete=models.CASCADE, primary_key=False, verbose_name="sid")
    lower_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="lo")
    upper_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="up")
    min_value = models.DecimalField(max_digits=19, decimal_places=2,verbose_name="min")

    def __srt__(self):
        return "%s" % self.plan

class Sales(models.Model):
    month = models.IntegerField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    sellers_id = models.ForeignKey(Sellers, on_delete=models.CASCADE, primary_key=False, verbose_name="si")
    comission = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return "%s" % self.sellers
    
    def calc_comission(self, sellers, amount, month):
        if c.amount <= sellers.comission_plan.min_value:
            return c.amount * sellers.comission_plan.lower_percentage / 100
        else:
            return c.amount * sellers.comission_plan.upper_percentage / 100