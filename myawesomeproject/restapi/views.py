from django.db.models.query import QuerySet
from rest_framework import generics, viewsets
from rest_framework.decorators import action, permission_classes
from restapi.models import Lesson
from restapi.serializers import LessonSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from restapi.permissions import *
class LessonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LessonSerializer
    def get_queryset(self):
        return super().get_queryset().filter(student=self.request.user)

class LessonEditorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsLessonEditor]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    
class LessonStudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer
    
    def get_queryset(self):
        return Lesson.objects.filter(self.request.user in Lesson.objects.student)   