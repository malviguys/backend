from django.urls import include, path
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

API_TITLE="Lesson Booking API"
API_DESCRIPTION="Lessons"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),
    path('schema/', get_schema_view(title=API_TITLE)),
    path('api/v1/lessons', include('restapi.urls')),
    path('api/v1/auth', include('dj_rest_auth.urls')),
    path('api/v1/auth/registration', include('dj_rest_auth.registration.urls'))
    
]
