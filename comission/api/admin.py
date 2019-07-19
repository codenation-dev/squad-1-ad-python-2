from django.contrib import admin

from .models import Sellers, Comission_plan, Sales

admin.site.register(Sellers)
admin.site.register(Comission_plan)
admin.site.register(Sales)
