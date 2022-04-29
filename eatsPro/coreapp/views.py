from ast import Or
import imp
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from coreapp.models import FoodItem, Order,OrderInfo
from coreapp.forms import AccountForm, UserForm, RestaurantForm, FoodItemForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from coreapp.models import Restaurant
from coreapp.serializers import RestaurantSerializer,FoodItemSerializer
from django.utils import timezone
from oauth2_provider.models import AccessToken
import json
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
        restaurant_form = RestaurantForm(request.POST,request.FILES, instance=request.user.restaurant)
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
    fooditems = FoodItem.objects.filter(restaurant=request.user.restaurant).order_by("id")
    return render(request, 'restaurant/meal.html',{"fooditems":fooditems})

@login_required(login_url = '/restaurant/login/')
def restaurant_add_item(request):
    if request.method == "POST":
        food_item_form = FoodItemForm(request.POST,request.FILES)
        if food_item_form.is_valid() :
            fooditem = food_item_form.save(commit=False)
            fooditem.restaurant = request.user.restaurant
            fooditem.save()
            return redirect(restaurant_meal)


    food_item_form = FoodItemForm()

    return render(request, 'restaurant/additem.html',{
        "food_item_form": food_item_form
        })

@login_required(login_url = '/restaurant/login/')
def restaurant_edit_item(request,fooditem_id):
    
    if request.method == "POST":
        food_item_form = FoodItemForm(request.POST,request.FILES, instance=FoodItem.objects.get(id=fooditem_id))
        if food_item_form.is_valid() :
            food_item_form.save()
            return redirect(restaurant_meal)
    
    food_item_form = FoodItemForm(instance=FoodItem.objects.get(id=fooditem_id))

    return render(request, 'restaurant/editItem.html',{
        "food_item_form": food_item_form
        })

@login_required(login_url = '/restaurant/login/')
def restaurant_order(request):
    if request.method == "POST":
        order = Order.objects.get(id=request.POST["id"])
        if order.status == Order.PREPARING:
            order.status = Order.READY
            order.save()
        elif order.status == Order.READY:
            order.status = Order.PICKED
            order.save()

    orders = Order.objects.filter(restaurant=request.user.restaurant).order_by("-id")
    return render(request, 'restaurant/order.html',{"orders":orders})

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

#apis for customer!
@csrf_exempt
def customer_get_res_api(request):
    restaurants = RestaurantSerializer(
        Restaurant.objects.all().order_by("id"),
        many=True,
        context={"request":request}
    ).data
    return JsonResponse({"restaurants":restaurants})

@csrf_exempt
def customer_view_item_api(request,restaurant_id):
    #from sqlite3-json
    foodItems = FoodItemSerializer(
        FoodItem.objects.filter(restaurant_id=restaurant_id).order_by("id"),
        many = True,
        context = {"request":request}
    ).data
    return JsonResponse({"foodItems":foodItems})

@csrf_exempt
def customer_make_order_api(request):
    if request.method =="POST":
        token = AccessToken.objects.get(token=request.POST.get("access_token"),expires__gt = timezone.now())
        #not sure
        
        customer = token.user.customer
        '''
        if Order.objects.filter(customer=customer).exclude(status=Order.PICKED):
            return JsonResponse({"status":"failed","error":"existinf"})
        json of order detail will include [{"foodItem_id":1,"quantity":2}] sets(maybe  multiple)
        '''
        order_infos = json.loads(request.POST["order_infos"])
        price=0
        for i in order_infos:
            price = price+FoodItem.objects.get(id=i["foodItem_id"]).price*i["quantity"]
        
        if price>0:
            order = Order.objects.create(customer=customer,
            restaurant_id=request.POST["restaurant_id"],
            price=price,
            status = Order.PREPARING)
        for i in order_infos:
            OrderInfo.objects.create(order=order,foodItem_id=i["foodItem_id"],quantity = i["quantity"],
            subtotal = FoodItem.objects.get(id=i["foodItem_id"]).price*i["quantity"]
            
            )
    return JsonResponse({"status": "success"})

def customer_current_order_api(request):
    return JsonResponse({})
