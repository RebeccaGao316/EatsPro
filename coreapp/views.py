from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from coreapp.forms import UserForm,RestaurantForm
# Create your views here.
def home(request):
    return redirect(restaurant_home)

@login_required(login_url = '/restaurant/login/')
def restaurant_home(request):
    return render(request,"restaurant/home.html",{})

def restaurant_register(request):
    user_form = UserForm();
    restaurant_form = RestaurantForm()
    return render(request,"restaurant/register.html",{
        "user_form": user_form,
        "restaurant_form": restaurant_form
    })
