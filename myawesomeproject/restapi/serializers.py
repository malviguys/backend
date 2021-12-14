from rest_framework import serializers
from restapi.models import Lesson, Booking, Student, Teacher, Instrument
from zoneinfo import ZoneInfo

# TODO inserire le foregnkey nei serializzatori


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = "__all__"


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     print("="*30 + " CREATE TEACHER " + "="*50)
    #     return Teacher.objects.create(**validated_data)

    class Meta:
        fields = "__all__"
        model = Teacher


class LessonSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    teacher = TeacherSerializer(many=False, read_only=True)
    instrument = InstrumentSerializer(many=False, read_only=True)
    date_time = serializers.DateTimeField(
        default_timezone=ZoneInfo("Europe/Rome"))
    duration = serializers.DurationField()
    cost = serializers.DecimalField(max_digits=6, decimal_places=2)

    def create(self, validated_data):
        teacherData = self.context['request'].data.get('teacher')
        instrumentData = self.context['request'].data.get('instrument')
        teacher = Teacher.objects.get(id=teacherData['id'])
        instrument = Instrument.objects.get(
            id=instrumentData['id'])
        lesson = Lesson.objects.create(name=validated_data['name'], teacher=teacher, instrument=instrument,
                                       date_time=validated_data['date_time'], duration=validated_data['duration'], cost=validated_data['cost'])
        return lesson

    def update(self, instance, validated_data):
        print(instance)
        teacherData = self.context['request'].data.get('teacher')
        instrumentData = self.context['request'].data.get('instrument')
        teacher = Teacher.objects.get(id=teacherData['id'])
        instrument = Instrument.objects.get(
            id=instrumentData['id'])
        lesson = Lesson.objects.create(name=validated_data['name'], teacher=teacher, instrument=instrument,
                                       date_time=validated_data['date_time'], duration=validated_data['duration'], cost=validated_data['cost'])
        return lesson

    class Meta:
        fields = "__all__"
        model = Lesson


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Booking
