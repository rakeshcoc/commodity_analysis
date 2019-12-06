from django.contrib import admin
from .models import commodity_data,distance_table
# Register your models here.
admin.site.register(commodity_data)
admin.site.register(distance_table)