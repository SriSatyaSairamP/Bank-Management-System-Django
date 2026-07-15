from django.contrib import admin
from .models import Bank,Branch,CustomerApplication

admin.site.register(Bank)
admin.site.register(Branch)
admin.site.register(CustomerApplication)