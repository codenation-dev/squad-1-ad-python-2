from django.urls import path
from api import views

urlpatterns = [
    path('sellers/', views.sellers),
    path('commissions/', views.commissions),
    path('month_commission/', views.month_commission),
    path('vendedores/<int:month>/', views.vendedores),
    path('check_commission/', views.check_commission),
]
