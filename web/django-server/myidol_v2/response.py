from abc import *
import os, random
from myidol.models import ClusterInfo, ImageInfo

class App:
    def __init__(self):
        self.app = 'myidol_v2'
        self.api = 'myidol_v2'

# class AbstractResponse(App, metaclass=ABCMeta):
#     api = 'api'
#     template = 'template_name'
#     css = 'css_name'
#     chain_page = 'myidol'
#     next_point = 'process'

class Response(App):
    def __init__(self):
        super().__init__()
        self.set_api()
    def get_template(self):
        return os.path.join(self.api)
    def set_api(self):
        self.api = self.api

class ImageResponse(Response):
    def __init__(self):
        super().__init__()
        self.images_li = []
        self.images_dict = {}
        self.cluster_info_li = []
        self.cluster_info_dict = {}

    def get_images(self, gender='', choices=''):
        stage_n_cluster = [6, 5, 5]
        if gender == '':
            curr_cluster = ClusterInfo.objects.select_related().filter(cluster__startswith=choices)
        else:
            curr_cluster = ClusterInfo.objects.select_related().filter(image_id__gender=gender, cluster__startswith=choices)
        if len(choices) == len(stage_n_cluster)-1 or len(curr_cluster) == 1:
            self.chain_page = self.next_point
        for i in range(stage_n_cluster[len(choices)]):
            try:
                next_choice = self.choices + str(i)
                i_cluster = curr_cluster.filter(cluster__startswith=next_choice)
                curr_cand = i_cluster[random.randint(0, len(i_cluster)-1)]
                print(curr_cand)
                self.cluster_info_li.append(curr_cand)
            except Exception as e:
                print(e)
    def post_images(self, gender='male', params=None):
        # print(params)
        i = 0
        for k, v in params.items():
            print(v)
            self.cluster_info_dict[i] = {'image_info': ImageInfo.objects.get(id=k), 'data': list(v)}
            i += 1
    
class Image:
    def __init__(self):
        super().__init__()
        self.next_choice = ''
        self.file_name = ''
        self.name = ''

class HomeResponse(ImageResponse):
    def __init__(self):
        super().__init__()
        self.api = ''
        self.css = 'index'
        self.template = ''
        self.chain_page = 'process'
        self.next_point = 'process'
        self.gender = ''
        self.choices = ''
        self.get_images(gender=self.gender, choices=self.choices)

class ProcessResponse(ImageResponse):
    def __init__(self, **kwagrs):
        super().__init__()
        self.css = 'process'
        self.chain_page = 'process'
        self.next_point = 'result'
        self.stage = 1
        for k,v in kwagrs.items():
            setattr(self, k, v)

        if self.params == False:
            self.chain_page = self.next_point
            self.tamplate = 'result'
        else:
            self.get_images(self.gender, self.choices)
            self.post_images(self.gender, params=self.params)

class ResultReponse(ImageResponse):
    def __init__(self, **kwargs):
        super().__init__()
        self.css = 'result'
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.get_result()
    def get_result(self):
        curr_cluster = ClusterInfo.objects.select_related().filter(image_id__gender=self.gender, cluster__startswith=self.choices)
        sampled = random.sample(range(len(curr_cluster)), min(len(curr_cluster), 5))
        for i in range(len(sampled)):
            self.images_dict[i+1] = curr_cluster[sampled[i]].image_id