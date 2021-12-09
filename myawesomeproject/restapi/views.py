from typing import Mapping
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action, permission_classes
from restapi.models import Lesson, Booking
from restapi.serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from restapi.permissions import *


class LessonView(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly, IsLessonEditor, IsAuthenticated]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class BookedView(viewsets.ModelViewSet):
    # permission_classes=[AllowAny]
    permission_classes = [IsBookingOwner]
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

