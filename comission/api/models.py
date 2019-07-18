from django.db import models

class Sellers(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.IntegerField()
    age = models.IntegerField()
    email = models.EmailField(max_length=100)
    cpf = models.IntegerField()
    comission_plan = models.IntegerField()

    def __str__(self):
        return self.name

class Comission_plan(models.Model):
    plan = models.CharField(max_length=100)
    sellers = models.OneToOneField(Sellers, on_delete=models.CASCADE, primary_key=False, related_name="selec")
    lower_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    upper_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    min_value = models.DecimalField(max_digits=19, decimal_places=2)

    def __srt__(self):
        return "%s" % self.plan

class Sales(models.Model):
    month = models.IntegerField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    sellers = models.ForeignKey(Sellers, on_delete=models.CASCADE, primary_key=False)
    comission = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return "%s" % self.sellers
    
    def calc_comission(self, sellers, amount, month):
        c = Sales(month=month, amount=amount, sellers=sellers)
        if c.amount <= sellers.comission_plan.min_value:
            return c.amount * sellers.comission_plan.lower_percentage / 100
        else:
            return c.amount * sellers.comission_plan.upper_percentage / 100