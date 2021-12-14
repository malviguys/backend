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
class LessonView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyLesson]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def create(self, request, *args, **kwargs):
        print("="*30 + " CREATE LESSON " + "="*50)
        try:
            teacher = Teacher.objects.get(user=request.user)
            print("Teacher ", teacher, "User ", teacher.user.id)
            print("request.data['teacher']", request.data['teacher'])
            print("request.data['teacher']['user']", request.data['teacher']['user'])
            user = Teacher.objects.get(user=request.data['teacher']['user'])
            print("User ", user)
            if teacher != user:
                print("Teacher is not the same as the logged in user")
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
        return Booking.objects.filter(student=self.request.user.id)

    def create(self, request):
        serializer = BookingSerializer(
            data={"student": request.user.id, "lesson": request.data.get("lesson")})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
