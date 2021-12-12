from rest_framework import routers
from restapi.views import LessonView, BookedView

urlpatterns = []

router = routers.SimpleRouter()
router.register(r'lessons', LessonView, 'lessons')
router.register(r'booking', BookedView, 'booking')
urlpatterns += router.urls