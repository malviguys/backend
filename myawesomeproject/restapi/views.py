from django.http import response
from rest_framework import viewsets, status
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from restapi.models import Lesson, Booking, Teacher, Student
from restapi.permissions import *
from restapi.serializers import *
from django.contrib.auth.models import User


class LessonView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyLesson]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def create(self, request, *args, **kwargs):
        print("="*30 + " CREATE LESSON " + "="*50)
        try:
            teacher = Teacher.objects.get(user=request.user)
            print("Teacher ", teacher)
            print("request.data['teacher']", request.data['teacher'])
            user = Teacher.objects.get(id=request.data['teacher'])
            print("User ", user)
            if teacher != user:
                print("Teacher is not the same as the logged in user")
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)
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
