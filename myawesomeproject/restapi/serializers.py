from rest_framework import serializers
from restapi.models import Lesson

class LessonSerializer(serializers.ModelSerializer):
  class Meta:
    fields = "__all__"
    model = Lesson
    