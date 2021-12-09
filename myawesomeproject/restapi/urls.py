from django.urls import path
from restapi.views import *
from rest_framework import routers

urlpatterns = []

router = routers.SimpleRouter()
router.register(r'lessons', LessonView,basename='lesson')
router.register(r'booking', StudentBookedList,basename='booking')
urlpatterns += router.urls