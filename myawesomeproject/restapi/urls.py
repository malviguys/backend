from django.urls import path
from restapi.views import *
from rest_framework import routers

urlpatterns = []

router = routers.SimpleRouter()
router.register(r'lessons', LessonStudentViewSet,basename='lessons-by-students')
urlpatterns += router.urls