from asyncio import create_task
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from cloudinary.models import CloudinaryField
import os
from twilio.rest import Client

# Create your models here.
# restaurant class
class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name= 'restaurant')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    logo = CloudinaryField('NYU_LOGO')
    def __str__(self):
        return self.name


#customer/staff/falculty/user
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name= 'customer')
    name = models.CharField(max_length=255)
    net_id = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)

    profile_picture = models.CharField(max_length=255)
    def __str__(self):
        return self.user.get_full_name()

#manager, staff in restraurant
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name= 'staff')
    name = models.CharField(max_length=255)
    net_id = models.CharField(max_length=255)
    
    def __str__(self):
        return self.user.get_full_name()

class FoodItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete= models.CASCADE, related_name= 'restaurant')
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    image = CloudinaryField('foodImage')
    price = models.FloatField(default=0.0)
    def __str__(self):
        return self.name

class Order(models.Model):
    PREPARING = 1
    READY = 2
    PICKED = 3
    STATUS = ((PREPARING,"Preparing"),(READY,"Ready"),(PICKED,"Picked"),)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    price = models.FloatField()
    status =  models.IntegerField(choices=STATUS)
    create_time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return str(self.id)
    def sendMessage(self,*args, **kwargs):
        if self.status == Order.READY:
            account_sid = 'AC91199b7fb549ffd141615b511a1ca2c5'
            auth_token = '853b3c99395490090874f7b2dce6c7b0'
            client = Client(account_sid, auth_token)
            message = client.messages \
                            .create(
                                body="The Order is ready.",
                                from_='+13253356937',
                                to=self.customer.phone
                            )



class OrderInfo(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT, related_name='order_infos')
    foodItem = models.ForeignKey(FoodItem,on_delete=models.PROTECT)
    quantity  = models.IntegerField()
    subtotal = models.FloatField()

    def __str__(self):
        return str(self.id)
 