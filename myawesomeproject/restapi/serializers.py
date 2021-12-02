from rest_framework import serializers
from restapi.models import Lesson

class LessonSerializer(serializers.ModelSerializer):
  class Meta:
    fields = ("id", "name","teacher","instrument","students","date_time","duration","cost")
    model = Lesson
    