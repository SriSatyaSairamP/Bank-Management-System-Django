from django.shortcuts import render,redirect
from .forms import CustomerApplicationForm
from .models import CustomerApplication,ApplicationHistory


def customer_application(request):

    if request.method == "POST":

        form = CustomerApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.status = "PENDING"
            application.save()

            ApplicationHistory.objects.create(
                application = application,
                action = ApplicationHistory.Action.CREATED,
                remarks = "Application submitted by customer"
            )
            return redirect("application_submitted")
        
        
    else:
        form = CustomerApplicationForm()


    return render(request,"accounts/customer_application.html",{"form":form})


def application_submitted(request):

    return render(request,"accounts/application_submitted.html")