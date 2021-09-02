from django.shortcuts import redirect, render
# import ideal.settings as setting
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

def home_redirect(request):
    return redirect('myidol')