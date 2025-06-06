from django.contrib import admin
from .models import Property, City, PropertyType
# Register your models here.
admin.site.register(Property)
admin.site.register(City)
admin.site.register(PropertyType)