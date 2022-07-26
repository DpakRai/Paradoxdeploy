from datetime import timezone
from enum import Enum
from django.db import models
from django.db.models import Avg
from users.models import Review, UserProfile

class DeviceType(Enum):
    android = 1
    ios = 2
    
class MediaFile(models.Model):
    title = models.TextField(null=True, blank=True)
    file = models.FileField(null=True, blank=True,upload_to='screenshots/')

    def __str__(self):
        if self.title:
            return self.title
        return str(self.id)


class BaseDevice(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    type = models.IntegerField(
        choices=((_.value, _.name) for _ in DeviceType), default=1
    )
    title = models.CharField(max_length=100, null=True, blank=True)
    average_rating= models.FloatField(null=True, blank=True,default=5)
    cover_image = models.FileField(null=True, blank=True,upload_to='images/')
    
    screenshots = models.ManyToManyField(MediaFile,related_name='device_screenshots')
    reviews= models.ManyToManyField(Review,related_name='device_reviews', blank=True)
    summary = models.CharField(max_length=10,blank=True,null=True)

    category = models.CharField(max_length=15,blank=True, null=True)
    demo = models.FileField(null=True, blank=True,upload_to='demo/')
    domo_type = models.CharField(max_length=15,blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)

    def publish(self):
        self.published_date = timezone.now()
        self.is_published = True
        self.save()

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if self.id is not None:
            self.average_rating=self.reviews.aggregate(Avg('rating')).get('rating__avg')
        return super().save(*args, **kwargs)
