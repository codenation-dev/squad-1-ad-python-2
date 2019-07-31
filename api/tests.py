from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models import Commission_plan, Sellers, Sales
from decimal import Decimal


class TelesalesViewTestCase(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            username="usuario",
            email="usuario@email.com",
            password="pass"
        )
        self.user.save()

        # Create a plan
        self.p1 = Commission_plan.objects.create(
            lower_percentage=2.5,
            upper_percentage=10.5,
            min_value=5000,
        )

        # Create a seller
        self.s1 = Sellers.objects.create(
            name="Cadastro Teste",
            address="Rua Teste, 1223",
            phone="47123456789",
            age=30,
            email="teste@teste.com",
            cpf="11223344556",
            plan=Commission_plan.objects.get(),
        )

        # Create a month comission
        self.mc1 = Sales.objects.create(
            month=1,
            amount=10000,
            sellers_id=Sellers.objects.get(),
            commission=1050,
        )

    def test_create_auth(self):
        resp = self.client.post("/auth/", {"username": "usuario", "password": "pass"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_plan_201(self):
        resp = self.client.post("/auth/", {"username": "usuario", "password": "pass"}, format="json")
        token = resp.data["token"]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {
                "lower_percentage": 2.5,
                "upper_percentage": 10.5,
                "min_value": 5000
                }
        response = client.post("/commissions/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_plan_400(self):
        resp = self.client.post("/auth/", {"username": "usuario", "password": "pass"}, format="json")
        token = resp.data["token"]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {
                }
        response = client.post("/commissions/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_seller_201(self):
        resp = self.client.post("/auth/", {"username": "usuario", "password": "pass"}, format="json")
        token = resp.data["token"]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {
                "name": "José Vendedor",
                "address": "Rua abcd, 123",
                "phone": "48012345678",
                "age": 30,
                "email": "email@email.com",
                "cpf": "12345678910",
                "plan": 1
                }
        response = client.post("/sellers/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_seller_400(self):
        resp = self.client.post("/auth/", {"username": "usuario", "password": "pass"}, format="json")
        token = resp.data["token"]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {
                "name": "José Vendedor",
                "address": "Rua abcd, 123",
                "phone": "48012345678",
                "age": 30,
                "email": "email@email.com",
                "cpf": "12345678910",
                "plan": 99
                }
        response = client.post("/sellers/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_month_comission_201(self):
        resp = self.client.post("/auth/", {"username": "usuario", "password": "pass"}, format="json")
        token = resp.data["token"]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {
                "sellers_id": 1,
                "amount": 10000,
                "month": 2
                }
        response = client.post("/month_commission/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_month_comission_400(self):
        resp = self.client.post("/auth/", {"username": "usuario", "password": "pass"}, format="json")
        token = resp.data["token"]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {
                "sellers_id": 99,
                "amount": 10000,
                "month": 13
                }
        response = client.post("/month_commission/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_month_list(self):
        resp = self.client.post("/auth/", {"username": "usuario", "password": "pass"}, format="json")
        token = resp.data["token"]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = client.get("/vendedores/1/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_notify_200(self):
        resp = self.client.post("/auth/", {"username": "usuario", "password": "pass"}, format="json")
        token = resp.data["token"]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {
                "sellers_id": 1,
                "amount": 1000.65
                }
        response = client.post("/check_commission/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_notify_400(self):
        resp = self.client.post("/auth/", {"username": "usuario", "password": "pass"}, format="json")
        token = resp.data["token"]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        data = {
                "sellers_id": 99,
                "amount": 1000.65
                }
        response = client.post("/check_commission/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ModelsTestCase(TestCase):
    def setUp(self):
        Commission_plan.objects.create(lower_percentage=2.5, upper_percentage=10.5, min_value=5000.00)
        Commission_plan.objects.create(lower_percentage=1.5, upper_percentage=5, min_value=4500)
        Sellers.objects.create(name="Ricardo Almeida", address="Rua abc, 213", phone="11932455678",
                               age=35, email="mail@email.com.br", cpf="65478932102",
                               plan=Commission_plan.objects.get(id=1))
        Sellers.objects.create(name="José Vendedor", address="Rua Rasa, 01", phone="5547993548264",
                               age=42, email="email@email.com.uk", cpf="456123987",
                               plan=Commission_plan.objects.get(id=2))
        Sales.objects.create(sellers_id=Sellers.objects.get(id=1), amount=1238.00, month=1,
                             commission=round(Sales.calc_commission(self, 1, 1238.00), 2))
        Sales.objects.create(sellers_id=Sellers.objects.get(id=2), amount=10950.00, month=1,
                             commission=round(Sales.calc_commission(self, 2, 10950.00), 2))

    def test_calc_commission(self):
        self.assertEqual(Sales.calc_commission(self, 1, 1238.00), round(Decimal(30.95), 2))
        self.assertEqual(Sales.calc_commission(self, 2, 10950.00), round(Decimal(547.50), 2))

    def test_return_sellers(self):
        self.assertEqual(len(Sales.return_sellers(self, 1)), 2)
        self.assertEqual(Sales.return_sellers(self, 2).status_code, 404)

    def test_check_commission(self):
        self.assertEqual(Sales.check_commission(Sales ,1, 1325.00), {"seller_notified": False})
        self.assertEqual(Sales.check_commission(Sales, 2, 3200.00), {"seller_notified": True})
