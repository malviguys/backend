from typing import Mapping
from django.http import response
from rest_framework import viewsets, status
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from restapi.models import Lesson, Booking, Teacher, Student
from restapi.permissions import *
from restapi.serializers import *
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.core.files.storage import default_storage
from rest_framework.renderers import JSONRenderer
import json
class LessonView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyLesson]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def create(self, request, *args, **kwargs):
        print("="*30 + " CREATE LESSON " + "="*50)
        try:
            teacher = Teacher.objects.get(user=request.user)
            user = Teacher.objects.get(user=request.data['teacher']['user'])
            if teacher != user:
                return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "You do not have permission to perform this action."})
        except:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "You do not have permission to perform this action."})
        return super().create(request, *args, **kwargs)


class BookedView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyBooking]
    serializer_class = BookingSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Booking.objects.all()
        user = Student.objects.get(user=self.request.user)
        return Booking.objects.filter(student=user)

    def create(self, request, *args, **kwargs):
        print("="*30 + " CREATE BOOKING " + "="*50)
        try:
            student = Student.objects.get(user=request.user)
            user = Student.objects.get(user=request.data['student']['user'])
            if student != user:
                return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "You do not have permission to perform this action."})
        except:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "You do not have permission to perform this action."})
        return super().create(request, *args, **kwargs)


class StudentView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    
    def retrieve(self, request, pk=None):
        try:
            user=User.objects.get(id=pk)
            student = Student.objects.get(user=user)
            serializato = StudentSerializer(student)
            json = JSONRenderer().render(serializato.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Student Not Found"})
        return Response(status=status.HTTP_200_OK,data=json)

class TeacherView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()
    
    def retrieve(self, request, pk=None):
        try:
            user=User.objects.get(id=pk)
            teacher = Teacher.objects.get(user=user)
            serializato = TeacherSerializer(teacher)
            json = JSONRenderer().render(serializato.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Teacher Not Found"})
        return Response(status=status.HTTP_200_OK,data=json)