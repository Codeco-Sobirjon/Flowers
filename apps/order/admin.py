from django.contrib import admin
from .models import TypeRecipient, StatusDeliver, PlacingOrder, OrderFlowers
from parler.admin import TranslatableAdmin


class OrderFlowersInline(admin.TabularInline):
    model = OrderFlowers
    extra = 1
    verbose_name = "Цветок"
    verbose_name_plural = "Цветки"


class PlacingOrderAdmin(admin.ModelAdmin):
    list_display = ('author', 'full_name', 'recipient', 'status_deliver', 'total', 'cashback', 'deliver_price')
    search_fields = ('author__username', 'full_name', 'recipient__title', 'status_deliver__title')
    list_filter = ('recipient', 'status_deliver')
    inlines = [OrderFlowersInline]
    verbose_name = "Заказанная продукция"
    verbose_name_plural = "Заказанная продукция"


class TypeRecipientAdmin(TranslatableAdmin):
    list_display = ('title',)
    search_fields = ('translations__title',)


class StatusDeliverAdmin(TranslatableAdmin):
    list_display = ('title',)
    search_fields = ('translations__title',)


admin.site.register(TypeRecipient, TypeRecipientAdmin)
admin.site.register(StatusDeliver, StatusDeliverAdmin)
admin.site.register(PlacingOrder, PlacingOrderAdmin)
