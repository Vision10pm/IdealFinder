from django.contrib import admin
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import path, include
from myidol.views import home
import ideal.views as root_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('myidol/', include('myidol.urls')),
    path('', lambda x: HttpResponseRedirect('myidol')),
]
