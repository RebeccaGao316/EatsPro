from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from coreapp.forms import AccountForm, UserForm, RestaurantForm, FoodItemForm
# Create your views here.

#redirect everyone to homepage, add url in urls.py
def home(request):
    return redirect(restaurant_home)

@login_required(login_url = '/restaurant/login/')
def restaurant_home(request):
    #return render(request, 'restaurant/home.html',{})
    return redirect(restaurant_order)

@login_required(login_url = '/restaurant/login/')
def restaurant_account(request):
    if request.method == "POST":
        account_form = AccountForm(request.POST,instance=request.user)
        restaurant_form = RestaurantForm(request.POST,instance=request.user.restaurant)
        if account_form.is_valid()  and restaurant_form.is_valid():
            account_form.save()
            restaurant_form.save()
        
    account_form = AccountForm(instance=request.user)
    restaurant_form = RestaurantForm(instance=request.user.restaurant)

    return render(request, 'restaurant/account.html',{
        "account_form": account_form,
        "restaurant_form": restaurant_form
    })

@login_required(login_url = '/restaurant/login/')
def restaurant_meal(request):
    return render(request, 'restaurant/meal.html',{})

def restaurant_add_item(request):
    food_item_form = FoodItemForm()

    return render(request, 'restaurant/additem.html',{
        "food_item_form": food_item_form
        })


@login_required(login_url = '/restaurant/login/')
def restaurant_order(request):
    return render(request, 'restaurant/order.html',{})

@login_required(login_url = '/restaurant/login/')
def restaurant_report(request):
    return render(request, 'restaurant/report.html',{})

#    path('restaurant/register/',views.restaurant_register, name = 'restaurant_register'),
def restaurant_register(request):
    user_form = UserForm()
    restaurant_form = RestaurantForm()
    
    if request.method == "POST":
        user_form = UserForm(request.POST)
        restaurant_form = RestaurantForm(request.POST,request.FILES)
        
        if user_form.is_valid() and restaurant_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_restaurant = restaurant_form.save(commit=False)
            new_restaurant.user = new_user
            new_restaurant.save()

            login(request, authenticate(
                username = user_form.cleaned_data["username"],
                password = user_form.cleaned_data["password"]
            ))
            return redirect(restaurant_home)

    return render(request, 'restaurant/register.html',{
        "user_form":user_form,
        "restaurant_form":restaurant_form
        })
