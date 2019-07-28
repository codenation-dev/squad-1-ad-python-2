from rest_framework import serializers
from api.models import Commission_plan, Sellers, Sales


class CommissionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commission_plan
        fields = ['id', 'lower_percentage', 'upper_percentage', 'min_value']


class SellersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sellers
        fields = ['id', 'name', 'address', 'phone', 'age', 'email', 'cpf', 'plan']


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = ['id', 'month', 'amount', 'commission', 'sellers_id']


class CheckCommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = ['amount', 'sellers_id']
