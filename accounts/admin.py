from django.contrib import admin
from .models import Bank,Branch,CustomerApplication,Customer

admin.site.register(Bank)
admin.site.register(Branch)
admin.site.register(CustomerApplication)
admin.site.register(Customer)