from json.encoder import JSONEncoder
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myidol_v2.response import ProcessResponse, HomeResponse, ResultReponse
from myidol.models import ImageInfo, EmbeddingInfo
from myidol_v2.modules import kmeans, get_response
import random, json, datetime, os, time
import myidol_v2.modules

# Create your views here.
def home(request):
    choices = request.GET.get('choices', '')
    gender = request.GET.get('gender', '')
    home_response = HomeResponse()
    print(home_response.__dict__)
    return render(request, 'myidol_v2/index.html', context=home_response.__dict__)

class process(APIView):
    def get(self, request):
        choices = request.GET.get('choices', '')
        gender = request.GET.get('gender')
        query_set = ImageInfo.objects.filter(gender = gender)
        embedding_info = EmbeddingInfo.objects.select_related().filter(image_id_id__gender = gender)
        ids, embeddings = [], []
        for embedding in embedding_info:
            ids.append(embedding.image_id_id)
            embeddings.append(json.loads(embedding.embedding))
        kmean_result = myidol_v2.modules.get_response(ids=ids, embeddings=embeddings)
        pro_response = ProcessResponse(request=request, gender=gender, params = kmean_result, choices='', stage=1)
        return render(request, 'myidol_v2/process.html', context=pro_response.__dict__)

    def post(self, request):
        reqeust_time = datetime.datetime.now()
        gender = request._request.GET.get("gender")
        json_body = json.loads(request.body)
        prev_stage = int(json_body.get('stage', 1))
        print('prev stage:', json_body.get('stage'))
        curr_selected_sample = []
        selected_ids = []
        selected_embeddings = []
        for k, v in json_body.get('selected').items():
            try:
                selected_ids.extend(list(map(int, v[1:-1].split(", "))))
                curr_selected_sample.append((int(k), json.loads(EmbeddingInfo.objects.get(image_id_id = int(k)).embedding)))
            except Exception as e:
                print(e)
        for id in selected_ids:
            selected_embeddings.append(json.loads(EmbeddingInfo.objects.get(image_id_id=id).embedding))
        kmean_result = myidol_v2.modules.get_response(ids=selected_ids, embeddings=selected_embeddings, stage=prev_stage+1, choices=curr_selected_sample)
        pro_response = ProcessResponse(request=request, gender=gender, params = kmean_result, choices='', stage=prev_stage+1)
        response_time = datetime.datetime.now()
        time.sleep(5-(response_time-reqeust_time).seconds)
        return pro_response.json_reponse()
        if pro_response.params.get('result'):
            return render(request, 'myidol_v2/result.html', context=pro_response.__dict__)
        else:
            return render(request, 'myidol_v2/process_response.html', context=pro_response.__dict__)


class Result(APIView):
    def get(self, request):
        gender = request.GET.get('gender')
        choices = request.GET.get('choices')
        ret_response = ResultReponse(gender=gender, choices=choices)
        print(ret_response.__dict__)
        return render(request, 'myidol_v2/result.html', context=ret_response.__dict__)