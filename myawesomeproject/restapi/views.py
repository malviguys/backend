from rest_framework import generics, viewsets

from restapi.models import Lesson
from restapi.serializers import LessonSerializer


# class LessonList(generics.ListCreateAPIView):
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer


# class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer



