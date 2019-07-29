from django.test import TestCase
from api.models import Sellers, Sales, Commission_plan
from decimal import Decimal

class TelesalesTestCase(TestCase):
    def setUp(self):
        Commission_plan.objects.create(lower_percentage=2.5, upper_percentage=10.5, min_value=5000.00)
        Commission_plan.objects.create(lower_percentage=1.5, upper_percentage=5, min_value=4500)
        Sellers.objects.create(name="Ricardo Almeida", address="Rua abc, 213", phone="11932455678", age=35, email="mail@email.com.br", cpf="65478932102", plan=Commission_plan.objects.get(id=1))
        Sellers.objects.create(name="José Vendedor", address="Rua Rasa, 01", phone="5547993548264", age=42, email="email@email.com.uk", cpf="456123987", plan=Commission_plan.objects.get(id=2))
        Sales.objects.create(sellers_id=Sellers.objects.get(id=1), amount=1238.00, month=1, commission=round(Sales.calc_commission(self, 1, 1238.00), 2))
        Sales.objects.create(sellers_id=Sellers.objects.get(id=2), amount=10950.00, month=1, commission=round(Sales.calc_commission(self, 2, 10950.00), 2))

    def test_calc_commission(self):
        self.assertEqual(Sales.calc_commission(self, 1, 1238.00), round(Decimal(30.95), 2))
        self.assertEqual(Sales.calc_commission(self, 2, 10950.00), round(Decimal(547.50), 2))
    
    def test_return_sellers(self):
        self.assertEqual(len(Sales.return_sellers(self, 1)), 2)
        self.assertEqual(Sales.return_sellers(self, 2), 404)
    
    def test_check_commission(self):
        self.assertEqual(Sales.check_commission(self, 1, 1325.00), {"seller_notified": False})
        self.assertEqual(Sales.check_commission(self, 2, 3200.00), {"seller_notified": False})


