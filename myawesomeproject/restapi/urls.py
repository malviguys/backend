from rest_framework import routers
from restapi.views import LessonView, BookedView, StudentView, TeacherView

urlpatterns = []

router = routers.SimpleRouter()
router.register(r'lessons', LessonView, 'lessons')
router.register(r'booking', BookedView, 'booking')
router.register(r'student', StudentView, 'student')
router.register(r'teacher', TeacherView, 'teacher')
urlpatterns += router.urls