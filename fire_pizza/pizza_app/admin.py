from django.contrib import admin

from .models import Pizza, Order, OrderItem


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('items',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass
