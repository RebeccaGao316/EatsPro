from django.contrib import admin
from coreapp.models import FoodItem, Restaurant,Customer,Staff,Order,OrderInfo

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Customer)
admin.site.register(Staff)
admin.site.register(FoodItem)
admin.site.register(Order)
admin.site.register(OrderInfo)