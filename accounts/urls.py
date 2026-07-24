from django.urls import path
from .import views

urlpatterns =[
    path("customer/application/",views.customer_application,name="customer_application"),
    path("customer/application/submitted/",views.application_submitted,name="application_submitted")
]