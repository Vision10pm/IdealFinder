# from random import random
import json, random
import numpy as np
from numpy.random.mtrand import random_sample
from sklearn.cluster import KMeans
# from myidol.models import EmbeddingInfo
# class IdealKmeans(KMeans):
#     def __init__(self, K=10, curr_stage=0):
#         self.stages = [10, 7, 6, 4, 3, 2]
#         super().__init__(n_cluster=self.stages[curr_stage], random_state=42)
#         # s : 각 stage의 cluster 개수
#         y_pred = list(kmeans.labels_)

#         # 각 stage의 clustering 결과를 dataframe에 저장
#         for i in range(len(y_pred)):
#             multi_df[s].iloc[idx[i]] = y_pred[i]

#         # 각 클러스터마다 샘플 보여주기 // sampling 부분
#         samples = [] # 각 클러스터의 sample들을 저장해둔 리스트
#         for i in range(s):
#             samples.append(multi_df[multi_df.loc[:,s]==i].loc[:,s].sample(1).index[0])
#         #사용자 이상형 선택
#         choice = list(map(int,input('가장 선호하는 외모를 선택해 주세요. : ').split(' ')))
        # idx = idx[np.where(np.isin(y_pred,choice)==True)[0]]
#     def get_sample
def kmeans(n_clusters=5, ids=[], embeddings=[]):
    km = KMeans(n_clusters=n_clusters, random_state=42)
    ids = np.array(ids)
    embeddings = np.array(embeddings)
    km.fit(embeddings)
    y_labels = km.labels_
    clusters = []
    cluster_centers = []
    for n in range(n_clusters):
        
        clusters.append(ids[np.where(km.labels_==n)])
        center = km.cluster_centers_[n].reshape(-1)
        # cluster_centers.append(ids[np.where(embeddings == center)])
    # print(cluster_centers)
    return clusters


def get_response(ids=[], embeddings=[], stage=1):
    stages = [8, 6, 4, 2]
    if stage == len(stages)+1:
        return False
    clusters = kmeans(n_clusters=stages[stage-1], ids=ids, embeddings=embeddings)
    return {random.sample(list(cluster), 1)[0]: cluster for cluster in clusters}

# def test():
    # print('test')
    # stage = [10,7,6,4,3,2]
# # stage별로 저장할 DataFrame 생성
# # multi_df = pd.DataFrame(index = [i for i in range(len(female_embeddings))], columns=stage)
# # multi_df.fillna(-1)
# # # 임베딩 값과 데이터 개수 index를 저장해둔 list 
# # embeddigns = female_embeddings
# # idx = np.array([i for i in range(len(female_embeddings))])
#     id_list = [1, 2, 3, 4]
#     for id in id_list:
#         query_set = EmbeddingInfo.objects.get(image_id_id=id).get_embedding()

