from django.db import models

from users.models import UserProfile

class subscriptions(models.Model):
    user_id= models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    sub_name = models.CharField(max_length=100)
    sub_type = models.CharField(max_length=100)