from json.encoder import JSONEncoder
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myidol.response import ProcessResponse, AppResponse, ResultReponse
from .models import ClusterInfo, ImageInfo
from .module import get_cluster
import random

# Create your views here.
def home(request):
    home_response = AppResponse()
    home_response.page = 'myidol'
    return render(request, 'myidol/myidol.html', context=home_response.__dict__)

class process(APIView):
    def get(self, request):
        my_response = ProcessResponse()
        gender = request.GET.get('gender')
        choices = request.GET.get('choices', '')
        my_response.gender = gender
        my_response.candidate = []
        my_response.prev_choices = choices
        stage_n_cluster = [6, 5, 5]
        curr_cluster = ClusterInfo.objects.select_related().filter(image_id__gender=gender, cluster__startswith=choices)
        if len(choices) == len(stage_n_cluster)-1 or len(curr_cluster) == 1:
            my_response.chain_page = my_response.next_point
        for i in range(stage_n_cluster[len(choices)]):
            try:
                next_choice = choices + str(i)
                i_cluster = curr_cluster.filter(cluster__startswith=next_choice)
                curr_cand = i_cluster[random.randint(0, len(i_cluster)-1)]
                file_name = curr_cand.image_id.get_file_name()
                name = curr_cand.image_id.name
                my_response.candidate.append({'choices': next_choice, 'file_name': file_name, 'name': name})
            except Exception as e:
                print(e)
        return render(request, 'myidol/process.html', context=my_response.__dict__)

class Result(APIView):
    def get(self, request):
        ret_response = ResultReponse()
        gender = request.GET.get('gender')
        choices = request.GET.get('choices')
        ret_response.gender = gender
        ret_response.ideals = {}
        curr_cluster = ClusterInfo.objects.select_related().filter(image_id__gender=gender, cluster__startswith=choices)
        sampled = random.sample(range(len(curr_cluster)), min(len(curr_cluster), 5))
        for i in range(len(sampled)):
            ret_response.ideals[i+1] = curr_cluster[sampled[i]].image_id
        return render(request, 'myidol/result.html', context=ret_response.__dict__)