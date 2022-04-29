from django.http import JsonResponse
from coreapp.models import Restaurant
from coreapp.serializers import RestaurantSerializer
#haven't decide whether in apis/views
def customer_get_res_api(request):

    restaurants = RestaurantSerializer(
        Restaurant.objects.all().order_by("id"),
        many=True
    ).data
    return JsonResponse({"restaurants":restaurants})