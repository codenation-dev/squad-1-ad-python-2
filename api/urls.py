from django.urls import path
from api import views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    path('sellers/', views.sellers),
    path('commissions/', views.commissions),
    path('month_commission/', views.month_commission),
    path('vendedores/<int:month>/', views.vendedores),
    path('check_commission/', views.check_commission),
    path('auth/', obtain_jwt_token),
    path('auth/refresh-token/', refresh_jwt_token),
]
