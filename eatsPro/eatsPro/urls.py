"""eatsPro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from coreapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #homepage
    path('',views.home, name = 'home'),
    path('restaurant/',views.restaurant_home, name = 'restaurant_home'),
    path('restaurant/login/',auth_views.LoginView.as_view(template_name = 'restaurant/login.html'),name = 'restaurant_login'),
    path('restaurant/logout/',auth_views.LogoutView.as_view(next_page = '/'),name = 'restaurant_logout'),
    path('restaurant/register/',views.restaurant_register, name = 'restaurant_register'),
    #account part
    path('restaurant/account/',views.restaurant_account, name = 'restaurant_account'),
    #meal part
    path('restaurant/meal/',views.restaurant_meal, name = 'restaurant_meal'),
    path('restaurant/meal/add/',views.restaurant_add_item, name = 'restaurant_add_item'),

    path('restaurant/order/',views.restaurant_order, name = 'restaurant_order'),
    path('restaurant/report/',views.restaurant_report, name = 'restaurant_report'),




    #provide a API for restraurant manager to register on facebook api
    # in django oauth token in /admin: alist of user
    #convert-token/revoke-token
    path('api/facebook/', include('rest_framework_social_oauth2.urls'))
]
