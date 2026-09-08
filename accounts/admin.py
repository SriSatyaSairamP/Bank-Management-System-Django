from django.contrib import admin,messages
from django.core.exceptions import ValidationError
from .models import Bank,Branch,CustomerApplication,Customer,ApplicationHistory


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

    search_fields=(
        "application_id",
        "full_name",
        "mobile_number"
    )

    list_filter =(
        "status",
        "branch"
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "application_id",
        "created_at",
        "updated_at"
    )


    def save_model(self, request, obj, form, change):

        if not change:

            obj.created_by = request.user
            super().save_model(request,obj,form,change)

            ApplicationHistory.objects.create(
                application = obj,
                action = ApplicationHistory.Action.CREATED,
                performed_by = request.user,
                remarks = "Customer application created by bank staff."
                )
            return

        if obj.created_by == request.user:
            raise ValidationError(
                "Cannot review by the Maker."
            )

        super().save_model(request,obj,form,change)

        action = None

        if obj.status == "PENDING":
            action = ApplicationHistory.Action.PENDING     

        elif obj.status == "APPROVED":
            action = ApplicationHistory.Action.APPROVED
               
        elif obj.status == "REJECTED":
            action = ApplicationHistory.Action.REJECTED


        ApplicationHistory.objects.create(
            application=obj,
            action=action,
            performed_by = request.user,
            remarks= obj.remarks
        )

   

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=(
        "customer_id",
        "application",
        "branch"
    )

@admin.register(ApplicationHistory)
class ApplicationHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "application",
        "action",
        "performed_by",
        "created_at"
    )

    list_filter=(
        "action",
        "performed_by"

    )

    search_fields =(
        "application__application_id",
        "performed_by__username"
        
    )

    ordering =( "-created_at",)

    readonly_fields =(
        "application",
        "action",
        "performed_by",
        "remarks",
        "created_at"

    )

    def has_add_permission(self,request):
        return False

    def has_change_permission(self,request,obj=None):
        return False

    def has_delete_permission(self,request,obj=None):
        return False
