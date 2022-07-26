from rest_framework import routers
from django.urls import path
from AI import views
from django.urls.conf import include


app_name = 'AI'
router = routers.DefaultRouter()

router.register('',views.BaseDeviceView,)
router.register('media',views.GetMediaView,)


urlpatterns = [
    path('', include((router.urls, 'ai'),namespace='ai')),
    path('review/<int:id>/', views.AIReview.as_view()),
    path('publish/<int:id>/', views.PublishAI.as_view()),
]