from django.db import models
from django.contrib.auth.models import User
from . import constants

class UserDetailsModel(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    account_no = models.IntegerField(unique=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=constants.GENDER_TYPES)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    post_code = models.IntegerField()
    country = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return str(self.account_no)
