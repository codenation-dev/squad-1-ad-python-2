from django.contrib import admin

from .models import Sellers, Commission_plan, Sales

admin.site.register(Sellers)
admin.site.register(Commission_plan)
admin.site.register(Sales)
