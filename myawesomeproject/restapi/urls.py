from django.urls import path
from restapi.views import LessonViewSet
from rest_framework import routers

urlpatterns = []

router = routers.SimpleRouter()
router.register(r'lessons', LessonViewSet)
urlpatterns += router.urls