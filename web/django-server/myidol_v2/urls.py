from django.urls import path, include
# from rest_framework import views
import myidol_v2.views as views
urlpatterns = [
    path('', views.home),
    path('process', views.process.as_view()),
    path('result', views.Result.as_view())
    # path('start/<int:stage>/', )
]