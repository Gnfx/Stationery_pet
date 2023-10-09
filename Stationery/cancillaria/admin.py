from django.contrib import admin
from .models import Cancillaria, Supplier, Order, Pos_order, Chegue


class CancillariaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'supplier', 'exist')
    list_display_links = ('pk', 'name')
    search_fields = ('name',)
    list_editable = ('price', 'exist')
    list_filter = ('exist', 'supplier')


admin.site.register(Cancillaria, CancillariaAdmin)


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'agent_firstname', 'agent_name', 'agent_patronymic', 'exist')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'agent_firstname')
    list_editable = ('exist',)
    list_filter = ('exist',)


admin.site.register(Supplier, SupplierAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_create', 'date_finish', 'status', 'price', 'address_delivery')
    list_display_links = ('id',)
    search_fields = ('date_create', 'address_delivery')
    list_editable = ('date_finish', 'status')
    list_filter = ('status',)


admin.site.register(Order, OrderAdmin)


class Pos_orderAdmin(admin.ModelAdmin):
    list_display = ('id', 'cancillaria', 'order', 'count_cancillaria', 'price')
    list_display_links = ('cancillaria', 'order')
    search_fields = ('cancillaria', 'order')


admin.site.register(Pos_order, Pos_orderAdmin)


class ChegueAdmin(admin.ModelAdmin):
    list_display = ('order', 'date_print', 'address_print', 'terminal')
    list_display_links = ('order', 'date_print')
    search_fields = ('order', 'address_print')


admin.site.register(Chegue, ChegueAdmin)
