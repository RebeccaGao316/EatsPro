from turtle import back
from urllib import request
from coreapp.models import Restaurant,Customer,Staff



        
def register_by_groups(backend, user, response, *args, **kwargs):
  request = backend.strategy.request_data()

  if backend.name == 'facebook':
    profile_picture = 'https://graph.facebook.com/%s/picture?type=large' % response['id']

    if request['user_type'] == "staff":
      Staff.objects.get_or_create(user_id=user.id)
    elif request['user_type'] == "customer":
      Customer.objects.get_or_create(user_id=user.id, profile_picture=profile_picture)


      
  