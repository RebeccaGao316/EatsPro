from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

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
