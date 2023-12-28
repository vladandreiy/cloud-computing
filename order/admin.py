from django.contrib import admin

from .models import Order, OrderItem, Payment

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ["user"]