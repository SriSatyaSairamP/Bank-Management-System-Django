from django import forms
from .models import CustomerApplication

class CustomerApplicationForm(forms.ModelForm):
    class Meta:
        model = CustomerApplication

        exclude =[
            "application_id",
            "branch",
            "status",
            "remarks",
            "created_by",
            "created_at",
            "updated_at",
        ]
 