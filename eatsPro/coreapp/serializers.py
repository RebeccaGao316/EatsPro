from rest_framework import serializers
from coreapp.models import Restaurant, FoodItem
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