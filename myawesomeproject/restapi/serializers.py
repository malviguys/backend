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
    cost = serializers.DecimalField(max_digits=5, decimal_places=2)

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
        lesson = Lesson.objects.get(id=instance.id)
        lesson.name = validated_data['name']
        teacherData = self.context['request'].data.get('teacher')
        instrumentData = self.context['request'].data.get('instrument')
        # teacher = Teacher.objects.get(id=teacherData['id'])
        # lesson.teacher = teacher
        instrument = Instrument.objects.get(
            id=instrumentData['id'])
        lesson.instrument = instrument
        lesson.date_time = validated_data['date_time']
        lesson.cost = validated_data['cost']
        lesson.duration = validated_data['duration']
        lesson.save()
        return lesson

    class Meta:
        fields = "__all__"
        model = Lesson


class BookingSerializer(serializers.ModelSerializer):
    student = StudentSerializer(many=False, read_only=True)
    lesson = LessonSerializer(many=False, read_only=True)

    def create(self, validated_data):
        studentData = self.context['request'].data.get('student')
        lessonData = self.context['request'].data.get('lesson')
        lesson = Lesson.objects.get(id=lessonData['id'])
        student = Student.objects.get(id=studentData['id'])
        return Booking.objects.create(student=student, lesson=lesson)

    def update(self, instance, validated_data):
        id = instance.id
        booking = Booking.objects.get(id=id)
        lessonData = self.context['request'].data.get('lesson')

        try:
            lesson = Lesson.objects.get(id=lessonData['id'])
            booking.lesson = lesson
            booking.save()
            return booking

        except:
            raise serializers.ValidationError("Lesson not found")

    class Meta:
        fields = "__all__"
        model = Booking
