from telnetlib import STATUS
from rest_framework import serializers
from coreapp.models import Customer, Restaurant, FoodItem,Order,OrderInfo
'''
    restaurant = models.ForeignKey(Restaurant, on_delete= models.CASCADE, related_name= 'restaurant')
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    image = CloudinaryField('foodImage')
    price = models.FloatField(default=0.0)
'''

class FoodItemSerializer(serializers.ModelSerializer):
  image = serializers.SerializerMethodField()

  def get_image(self, restaurant):
    request = self.context.get('request')
    image_url = restaurant.image.url
    return request.build_absolute_uri(image_url)

  class Meta:
    model = FoodItem
    fields = ("id", "name", "description", "image", "price")

class RestaurantSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    def get_logo(self,restaurant):
        request = self.context.get('request')
        imageurl = restaurant.logo.url
        return request.build_absolute_uri(imageurl)
    class Meta:
        model = Restaurant
        fields = ("id","name","phone","address","logo")

class OrderCustomerSerializer(serializers.ModelSerializer):
  name = serializers.ReadOnlyField(source="user.get_full_name")
  class Meta:
    model = Customer
    fields = ("id","name","profile_picture")

class OrderFoodItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = FoodItem
    fields = ("id","name","price")

class OrderRestaurantSerializer(serializers.ModelSerializer):
  class Meta:
    model = Restaurant
    fields = ("id", "name", "phone", "address")
  
class OrderInfoSerializer(serializers.ModelSerializer):
  foodItem = OrderFoodItemSerializer()
  class Meta:
    model = OrderInfo
    fields = ("id","foodItem","quantity","subtotal")

class OrderSerializer(serializers.ModelSerializer):
  customer = OrderCustomerSerializer()
  restaurant = OrderRestaurantSerializer()
  order_infos = OrderInfoSerializer(many =True)
  status = serializers.ReadOnlyField(source="get_status_display")
  class Meta:
    model = Order
    fields = ("id","customer","restaurant","order_infos","price","status")

class OrderStatusSerializer(serializers.ModelSerializer):
  status = serializers.ReadOnlyField(source="get_status_display")
  class Meta:
    model = Order
    fields = ("id","status")