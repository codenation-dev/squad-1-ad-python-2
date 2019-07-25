from django.db import models
from decimal import Decimal
import datetime
import json
from operator import itemgetter as ig
from django.core.mail import send_mail


class MyDecimal(Decimal):
    def __repr__(self):
        return str(float(self))


class Commission_plan(models.Model):
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
    plan = models.ForeignKey(Commission_plan, on_delete=models.CASCADE, verbose_name="plan")

    def __str__(self):
        return self.name


class Sales(models.Model):
    month = models.IntegerField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    sellers_id = models.ForeignKey(Sellers, on_delete=models.CASCADE, primary_key=False, verbose_name="sid")
    commission = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return "Seller: %s" % self.sellers_id.name

    def register_commission_plan(self, lo, up, mi):
        s = Commission_plan(lower_percentage=lo, upper_percentage=up, min_value=mi)
        s.save()
        return {"id": s.id}
    
    def register_sellers(self, file):
        with open(file) as json_file:
            data = json.load(json_file)
        s = Sellers(name=data["name"], address=data["address"], phone=data["telefone"], age=data["idade"], 
                    email=data["email"], cpf=data["cpf"])
        s.plan = Commission_plan.objects.get(id=data["commission_plan"])
        s.save()
        return {"id": s.id}
    
    def calc_commission(self, seller, amount):
        sel_calc = Sellers.objects.get(id=seller)
        dec_amount = MyDecimal(amount)
        if dec_amount <= MyDecimal(sel_calc.plan.min_value):
            commission = dec_amount * MyDecimal(sel_calc.plan.lower_percentage / 100)
        else:
            commission = dec_amount * MyDecimal(sel_calc.plan.upper_percentage / 100)
        return MyDecimal(round(commission, 2))

    def sales_month(self, seller, amount, month):
        sel_month = Sellers.objects.get(id=seller)
        month_amount = MyDecimal(amount)
        s = Sales(sellers_id=sel_month, amount=month_amount, month=month)
        s.commission = self.calc_commission(seller, month_amount)
        s.save()
        return {"id": s.id, "commission": MyDecimal(s.commission)}

    def return_sellers(self, month):
        return sorted([{"name": i.sellers_id.name, "id": i.sellers_id.id, "commission": MyDecimal(i.commission)} for i in
                      Sales.objects.filter(month=month)], key=lambda x: x['commission'], reverse=True)

    def check_exists(self, seller): # Pegar todas as vendas por vendedor e eliminar esta verificação (order_by limit 5)
        for i in range(len(Sales.objects.filter(sellers_id=seller))):
            try:
                Sales.objects.get(sellers_id=seller, month=i)
            except (Sales.DoesNotExist):
                i += 1
        return i

    def notify_seller(self, seller, month):
        send_mail(
                'Notificação - valor de vendas',
                'Suas vendas no mês estão abaixo da média mensal.',
                'commission_admin@mail.com',
                [Sales.objects.get(sellers_id=seller, month=month).sellers_id.email],
                fail_silently=False
        )
    
    def check_commission(self, seller, amount):
        month = datetime.datetime.now().month
        self.sales_month(seller, MyDecimal(amount), month)
        db_fetch = Sales.objects.select_related('sellers_id').filter(sellers_id=seller).order_by('commission')
        sorted_sales = sorted([{'name': db_fetch[i].sellers_id.name, 'month': db_fetch[i].month, 'amount': 
                                MyDecimal(db_fetch[i].amount), 'commission': MyDecimal(db_fetch[i].commission)} 
                                for i in range(len(db_fetch))], key=ig('commission'), reverse=True) 
        avg_sales = (sum([ig('amount')(sorted_sales[i]) * (len(sorted_sales) - i) for i in range(len(sorted_sales))]) /
                    sum(len([ig('amount')(sorted_sales[i]) * (len(sorted_sales) - i) for i in range(len(sorted_sales))])))
        cut_amount = avg_sales - (avg_sales * 10 / 100)
        notify = [ig('amount')(sorted_sales[i]) for i in range(len(sorted_sales)) if ig('amount')
                    (sorted_sales[i]) < cut_amount and ig('month')(sorted_sales[i]) == month]
        if notify is not []:
            out_message = {"seller_notified": True}
            self.notify_seller(seller, month)
            return out_message
        else:
            out_message = {"seller_notified": False}
            return out_message
