from django.contrib import admin

from ecommerce.models import Cart, Order, Product

# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)