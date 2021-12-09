from rest_framework import serializers
from restapi.models import Lesson, Booking


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Lesson


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Booking
