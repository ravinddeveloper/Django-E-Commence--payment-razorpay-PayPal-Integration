from django.contrib import admin

from .models import product,cart,address,order,delivery_status,category,newsletter
# Register your models here.

admin.site.register(product)
admin.site.register(category)
admin.site.register(cart)
admin.site.register(address)
admin.site.register(order)
admin.site.register(delivery_status)
admin.site.register(newsletter)
