from django.shortcuts import render,redirect
from .forms import CustomerApplicationForm


def register(request):

    if request.method == "POST":

        form = CustomerApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("register")
        
        
    else:
        form = CustomerApplicationForm()


    return render(request,"accounts/register.html",{"form":form})