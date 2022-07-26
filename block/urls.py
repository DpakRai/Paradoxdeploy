from django.urls import path,include
from block  import views
from rest_framework import routers
app_name = 'Block'
router = routers.DefaultRouter()

router.register('',views.BlockView)


urlpatterns = [
    path('', include(router.urls)),
    path('review/<int:id>/', views.BlockReview.as_view()),
]