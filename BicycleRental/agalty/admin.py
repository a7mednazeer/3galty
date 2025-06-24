from django.contrib import admin
from .models import CheckoutRide, Register, SearchByStations, StartRide

# Register your models here.

admin.site.register(Register)
admin.site.register(SearchByStations)
admin.site.register(StartRide)
admin.site.register(CheckoutRide)
admin.site.site_header = '3galty | Dashboard'
admin.site.site_title = '3galty'
