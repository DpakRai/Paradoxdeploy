from django.db import models
from django.db.models import Avg
from AI.models import MediaFile
from users.models import UserProfile, Review

class Extension(models.Model):
    user= models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    cover_image = models.FileField(null=True, blank=True,upload_to='images/')
    description = models.TextField(null=True, blank=True)
    average_rating= models.FloatField(null=True, blank=True,default=5)

    download = models.IntegerField(default=0)
    screenshots = models.ManyToManyField(MediaFile,related_name='extension_screenshots')
    reviews = models.ManyToManyField(Review, related_name='extension_reviews', blank=True)
    demo = models.FileField(null=True, blank=True,upload_to='demo/')

    def save(self, *args, **kwargs):
        if self.id is not None:
            self.average_rating=self.reviews.aggregate(Avg('rating')).get('rating__avg')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title