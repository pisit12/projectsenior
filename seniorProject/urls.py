"""seniorProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_swagger.views import get_swagger_view

from weather import views_csv

urlpatterns_api = [
    path('weather/', include('weather.urls')),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', get_swagger_view(title='API', patterns=urlpatterns_api)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # <-- And here
    # path('export/',views_csv.export, name='export')
    # path('listnamestation/', include('weather.urls')),
]

urlpatterns += urlpatterns_api
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# path('reportstation/', include('weather.urls')),
    # path('weatherdata/', include('weather.urls')),
    # path('search/', include('weather.urls'))