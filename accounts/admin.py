from django.contrib import admin
from .models import Bank,Branch,CustomerApplication,Customer


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ("bank_name","bank_code","is_active")

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("branch_name","bank","branch_code","ifsc_code","is_active")

@admin.register(CustomerApplication)
class CustomerApplicationAdmin(admin.ModelAdmin):
    list_display=(
        "application_id",
        "full_name",
        "status",
        "branch",
        "created_at"
    )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=(
        "customer_id",
        "application",
        "branch"
    )