from django.db import models
from AI.models import MediaFile
from django.db.models import Avg

from users.models import Review, UserProfile

# Create your models here.
class Block(models.Model):
    user= models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    cover_image = models.FileField(null=True, blank=True,upload_to='images/')
    average_rating= models.FloatField(null=True, blank=True,default=5)
    description_block = models.CharField(max_length=100, null=True, blank=True)
    screenshots = models.ManyToManyField(MediaFile,related_name='block_screenshots')
    reviews= models.ManyToManyField(Review,related_name='block_reviews',blank=True)

    demo = models.FileField(null=True, blank=True,upload_to='demo/')

    def __str__(self):
        if self.title:
            return self.title
        return self.description_block

    def save(self, *args, **kwargs):
        if self.id is not None:
            self.average_rating=self.reviews.aggregate(Avg('rating')).get('rating__avg')
        return super().save(*args, **kwargs)