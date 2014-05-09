from django.contrib import admin
from django.db.models import get_model

Order = get_model('order', 'Order')
OrderNote = get_model('order', 'OrderNote')
CommunicationEvent = get_model('order', 'CommunicationEvent')
BillingAddress = get_model('order', 'BillingAddress')
ShippingAddress = get_model('order', 'ShippingAddress')
Line = get_model('order', 'Line')
ShippingEvent = get_model('order', 'ShippingEvent')
ShippingEventType = get_model('order', 'ShippingEventType')
PaymentEvent = get_model('order', 'PaymentEvent')
PaymentEventType = get_model('order', 'PaymentEventType')
PaymentEventQuantity = get_model('order', 'PaymentEventQuantity')


class LineInline(admin.TabularInline):
    model = Line
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    raw_id_fields = ['user', 'billing_address', 'shipping_address', ]
    list_display = ('number', 'total_incl_tax', 'site', 'user',
                    'billing_address', 'date_placed')
    readonly_fields = ('number', 'total_incl_tax', 'total_excl_tax',
                       'shipping_incl_tax', 'shipping_excl_tax')
    inlines = [LineInline]

class LineAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'stockrecord', 'quantity')


class ShippingEventTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    exclude = ('code',)


class PaymentEventQuantityInline(admin.TabularInline):
    model = PaymentEventQuantity
    extra = 0


class PaymentEventAdmin(admin.ModelAdmin):
    list_display = ('order', 'event_type', 'amount', 'num_affected_lines',
                    'date_created')
    inlines = [PaymentEventQuantityInline]

class PaymentEventTypeAdmin(admin.ModelAdmin):
   exclude = ('code',)


admin.site.register(Order, OrderAdmin)
admin.site.register(ShippingAddress)
admin.site.register(Line, LineAdmin)
admin.site.register(ShippingEvent)
admin.site.register(ShippingEventType, ShippingEventTypeAdmin)
admin.site.register(PaymentEvent, PaymentEventAdmin)
admin.site.register(PaymentEventType, PaymentEventTypeAdmin)
admin.site.register(CommunicationEvent)

