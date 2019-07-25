from django.db import models
from decimal import Decimal
import datetime
from operator import itemgetter as ig


class MyDecimal(Decimal):
    def __repr__(self):
        return str(float(self))


class Comission_plan(models.Model):
    lower_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="lo")
    upper_percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="up")
    min_value = models.DecimalField(max_digits=19, decimal_places=2, verbose_name="min")

    def __srt__(self):
        return self.id


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


class Sales(models.Model):
    month = models.IntegerField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    sellers_id = models.ForeignKey(Sellers, on_delete=models.CASCADE, primary_key=False, verbose_name="sid")
    comission = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return "Seller: %s" % self.sellers_id.name

    def calc_comission(self, seller, amount):
        sel_calc = Sellers.objects.get(id=seller)
        dec_amount = MyDecimal(amount)
        if dec_amount <= Decimal(sel_calc.plan.min_value):
            comission = dec_amount * Decimal(sel_calc.plan.lower_percentage / 100)
        else:
            comission = dec_amount * Decimal(sel_calc.plan.upper_percentage / 100)
        return MyDecimal(round(comission, 2))

    def sales_month(self, seller, amount, month):
        sel_month = Sellers.objects.get(id=seller)
        month_amount = Decimal(amount)
        s = Sales(sellers_id=sel_month, amount=month_amount, month=month)
        s.comission = self.calc_comission(seller, month_amount)
        s.save()
        return s.id, MyDecimal(s.comission)

    def return_sellers(self, month):
        return sorted([{"name": i.sellers_id.name, "id": i.sellers_id.id, "comission": MyDecimal(i.comission)} for i in
                      Sales.objects.filter(month=month)], key=lambda x: x['comission'], reverse=True)

    def check_exists(self, seller):
        for i in range(len(Sales.objects.filter(sellers_id=seller))):
            try:
                Sales.objects.get(sellers_id=seller, month=i)
            except (Sales.DoesNotExist):
                i += 1
        return i

    def check_comission(self, seller, amount):
        month = datetime.datetime.now().month
        check_amount = self.sales_month(seller, MyDecimal(amount), month)
        sorted_sales = sorted([{'name': Sales.objects.get(sellers_id=seller, month=i).sellers_id.name, 'month':
                                Sales.objects.get(sellers_id=seller, month=i).month, 'amount':
                                MyDecimal(Sales.objects.get(sellers_id=seller, month=i).amount), 'comission':
                                MyDecimal(Sales.objects.get(sellers_id=seller, month=i).comission)} for i in
                              range(month+1-self.check_exists(seller), month+1)], key=ig('comission'), reverse=True)
        dividend = sum([len([ig('amount')(sorted_sales[i]) * (len(sorted_sales) - i) for i in range(len(sorted_sales))])
                        - i for i in range(len([ig('amount')(sorted_sales[i]) * (len(sorted_sales) - i) for i in
                                                range(len(sorted_sales))]))])
        avg_sales = (sum([ig('amount')(sorted_sales[i]) * (len(sorted_sales) - i) for i in range(len(sorted_sales))]) /
                     dividend)
        cut_amount = avg_sales - (avg_sales * 10 / 100)
        notify = [ig('amount')(sorted_sales[i]) for i in range(len(sorted_sales)) if ig('amount')
                    (sorted_sales[i]) < cut_amount and ig('month') == month]
        if notify is True:
            out_message = {"should_notify": True}
            return out_message
        else:
            out_message = {"should_notify": False}
            return out_message
