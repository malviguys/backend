"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework.documentation import include_docs_urls, get_schema_view

API_TITLE = 'MusiLesson API'
API_DESCRIPTION = 'A web API for creating and booking music lessons.'

urlpatterns = [
    path('admin-hOFbRRSOiz/', admin.site.urls),
    path('docs/', include_docs_urls(title = API_TITLE, description = API_DESCRIPTION)),
    path('schema/', get_schema_view(title = API_TITLE)),
    # path('api/v1/lessons/', include('')),
    # path('api/v1/auth/', include('')),
    # path('api/v1/auth/registration/', include('')),
]
