import pytest
from django.core.exceptions import *
from django.db.utils import *
from mixer.backend.django import mixer
from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import connection
from .init import *


class TestModels:
    
    def test_lesson_name_not_empty(self, db):
        lesson = mixer.blend('restapi.Lesson', name='',
                             date_time=datetime(
                                 2022, 1, 31, 12, tzinfo=ZoneInfo("Europe/Rome")))
        with pytest.raises(ValidationError) as err:
            lesson.full_clean()
        assert 'This field cannot be blank.' in str(err)
    
    def test_lesson_name_not_capitalized(self, db):
        lesson = mixer.blend('restapi.Lesson', name='sasdasdas dong name', date_time=datetime(
            2022, 10, 31, 12, tzinfo=ZoneInfo("Europe/Rome")))
        with pytest.raises(ValidationError) as err:
            lesson.full_clean()
        assert 'Name must be capitalized' in str(err)

    def test_lesson_title_of_length_51_rises_exception(self, db):
        lesson = mixer.blend('restapi.Lesson', name='A' * 51,
                             date_time=datetime(2022, 10, 31, 12, tzinfo=ZoneInfo("Europe/Rome")))
        with pytest.raises(ValidationError) as err:
            lesson.full_clean()
        assert 'Name must be less than 50 char' in str(err)

    def test_lesson_date_time_in_past_raises_exception(self, db):
        lesson = mixer.blend('restapi.Lesson', name='A',
                             date_time=datetime(2000, 10, 31, 12, tzinfo=ZoneInfo("Europe/Rome")))
        with pytest.raises(ValidationError) as err:
            lesson.full_clean()
        assert 'Lesson date_time cannot be in the past' in str(err)

    def test_lesson_date_time_in_future_raises_exception(self, db):
        lesson = mixer.blend('restapi.Lesson', name='A',
                             date_time=datetime(2022, 10, 31, 12, tzinfo=ZoneInfo("Europe/Rome")))
        with pytest.raises(ValidationError) as err:
            lesson.full_clean()
        assert 'Lesson date must not be < now + 3months' in str(err)

    def test_lesson_duration_too_short_raises_exception(self, db):
        lesson = mixer.blend('restapi.Lesson', name='A',
                             date_time=datetime(
                                 2022, 10, 31, 12, tzinfo=ZoneInfo("Europe/Rome")),
                             duration=timedelta(minutes=14))
        with pytest.raises(ValidationError) as err:
            lesson.full_clean()
        assert 'Lesson duration must not be > 15min' in str(err)

    def test_lesson_duration_too_long_raises_exception(self, db):
        lesson = mixer.blend('restapi.Lesson', name='A',
                             date_time=datetime(
                                 2022, 10, 31, 12, tzinfo=ZoneInfo("Europe/Rome")),
                             duration=timedelta(minutes=121))
        with pytest.raises(ValidationError) as err:
            lesson.full_clean()
        assert 'Lesson duration must not be < 2h' in str(err)

    def test_lesson_cost_too_low_raises_exception(self, db):
        lesson = mixer.blend('restapi.Lesson', name='A',
                             date_time=datetime(
                                 2022, 1, 31, 12, tzinfo=ZoneInfo("Europe/Rome")),
                             cost=-1)
        with pytest.raises(ValidationError) as err:
            lesson.full_clean()
        assert 'Lesson cost must be positive value' in str(err)

    def test_lesson_cost_too_high_raises_exception(self, db):
        lesson = mixer.blend('restapi.Lesson', name='A',
                             date_time=datetime(
                                 2022, 1, 31, 12, tzinfo=ZoneInfo("Europe/Rome")),
                             cost=300)
        with pytest.raises(ValidationError) as err:
            lesson.full_clean()
        assert 'The maximum cost for lesson is 256$' in str(err)

    # def test_booking_lesson_not_found_raises_exception(self, db):
    #     booking = mixer.blend('restapi.Booking', lesson_id=100)
    #     with pytest.raises(IntegrityError) as err:
    #         connection.check_constraints()
    #     assert 'lesson instance with id 100 does not exist.' in str(err)

    # def test_booking_student_not_found_raises_exception(self, db):
    #     booking = mixer.blend('restapi.Booking', student_id=100)
    #     with pytest.raises(IntegrityError) as err:
    #         connection.check_constraints()
    #     assert 'student instance with id 100 does not exist.' in str(err)
    
    def test_instrument_name_not_capitalized(self, db):
        instrument = mixer.blend('restapi.Instrument', name='sasdasdas dong name')
        with pytest.raises(ValidationError) as err:
            instrument.full_clean()
        assert 'Name must be capitalized' in str(err)
    
    def test_teacher_name_not_capitalized(self, db):
        teacher = mixer.blend('restapi.Teacher', name='sasdasdas dong name')
        with pytest.raises(ValidationError) as err:
            teacher.full_clean()
        assert 'Name must be capitalized' in str(err)
    
    def test_student_name_not_capitalized(self, db):
        student = mixer.blend('restapi.Student', name='sasdasdas dong name')
        with pytest.raises(ValidationError) as err:
            student.full_clean()
        assert 'Name must be capitalized' in str(err)
    
    def test_lesson_string_output(self, db):
        name='A'
        instument=mixer.blend('restapi.Instrument', name='sasdasdas dong name')
        teacher=mixer.blend('restapi.Teacher', name='sasdasdas dong name')
        date_time=datetime(2022, 10, 31, 12, tzinfo=ZoneInfo("Europe/Rome"))
        duration=timedelta(minutes=120)
        cost=100
        lesson = mixer.blend('restapi.Lesson', name=name, instrument=instument, teacher=teacher, date_time=date_time, duration=duration, cost=cost)
        assert str(lesson) == f"NAME: {name} | INSTRUMENT: {instument} | TEACHER: {teacher} | DATE: {date_time} | DURATION: {duration} | COST: {cost}"
    
    def test_booking_string_output(self, db):
        stutend=mixer.blend('restapi.Student', name='sasdasdas dong name')
        lesson=mixer.blend('restapi.Lesson', name='A', date_time=datetime(2022, 10, 31, 12, tzinfo=ZoneInfo("Europe/Rome")), duration=timedelta(minutes=120), cost=100)
        booking = mixer.blend('restapi.Booking', student=stutend, lesson=lesson)
        assert str(booking) == f"STUDENT: {stutend} | LESSON: {lesson}"