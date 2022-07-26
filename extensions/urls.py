from rest_framework import routers
from django.urls import path
from extensions  import views
from django.urls.conf import include


app_name = 'Extensions'
router = routers.DefaultRouter()

router.register('',views.ExtensionView)


urlpatterns = [
    path('', include(router.urls)),
    path('review/<int:id>/', views.ExtensionReview.as_view()),
]