from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Commission_plan, Sales, Sellers
from api.serializers import CommissionPlanSerializer, SalesSerializer, SellersSerializer, CheckCommissionSerializer


@api_view(["POST"])
def sellers(request):
    if request.method == "POST":
        serializer = SellersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"id": serializer.data["id"]}, status=status.HTTP_201_CREATED)
        return Response({"message": "Bad request. Please check syntax and try again"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def commissions(request):
    if request.method == "POST":
        serializer = CommissionPlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"id": serializer.data["id"]}, status=status.HTTP_201_CREATED)
        return Response({"message": "Bad request. Please check syntax and try again"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def month_commission(request):
    if request.method == "POST":
        try:
            calc = Sales()
            calculated_amount = calc.calc_commission(request.data["sellers_id"], request.data["amount"])
        except:
            return Response({"message": "Bad request. Please check syntax and try again"},
                            status=status.HTTP_400_BAD_REQUEST)
        request.data["commission"] = calculated_amount
        serializer = SalesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"id": serializer.data["id"], "commission": serializer.data["commission"], },
                            status=status.HTTP_201_CREATED)
        return Response({"message": "Bad request. Please check syntax and try again"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def vendedores(request, month):
    if request.method == "GET":
        rs = Sales()
        return Response(rs.return_sellers(month))


@api_view(["POST"])
def check_commission(request):
    if request.method == "POST":
        serializer = CheckCommissionSerializer(data=request.data)
        if serializer.is_valid():
            cc = Sales()
            return Response(cc.check_commission(request.data["sellers_id"], request.data["amount"]),
                            status=status.HTTP_200_OK)
        return Response({"message": "Bad request. Please check syntax and try again"},
                        status=status.HTTP_400_BAD_REQUEST)
