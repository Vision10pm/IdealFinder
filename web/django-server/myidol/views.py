from json.encoder import JSONEncoder
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myidol.response import ProcessResponse, HomeResponse, ResultReponse
from .models import ClusterInfo, ImageInfo
from .module import get_cluster
import random

# Create your views here.
def home(request):
    choices = request.GET.get('choices', '')
    gender = request.GET.get('gender', '')
    home_response = HomeResponse()
    print(home_response.__dict__)
    return render(request, 'myidol/index.html', context=home_response.__dict__)

class process(APIView):
    def get(self, request):
        choices = request.GET.get('choices', '')
        gender = request.GET.get('gender')
        pro_response = ProcessResponse(gender=gender, choices=choices)
        print(pro_response.__dict__)
        return render(request, 'myidol/process.html', context=pro_response.__dict__)

class Result(APIView):
    def get(self, request):
        gender = request.GET.get('gender')
        choices = request.GET.get('choices')
        ret_response = ResultReponse(gender=gender, choices=choices)
        print(ret_response.__dict__)
        return render(request, 'myidol/result.html', context=ret_response.__dict__)