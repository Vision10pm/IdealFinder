from django.urls import path, include
# from rest_framework import views
import myidol_v2.views as views
urlpatterns = [
    path('', views.Home.as_view()),
    path('process', views.process.as_view()),
    path('result', views.Result.as_view()),
    path('similarity', views.Similarity.as_view()),
    
    # path('start/<int:stage>/', )
]