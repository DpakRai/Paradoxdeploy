from django.db import models

from users.models import UserProfile

# Create your models here.
class payments(models.Model):
    user_id= models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    payment_name = models.CharField(max_length=100)
    payment_type = models.CharField(max_length=100)
    payment_amount= models.PositiveIntegerField()

