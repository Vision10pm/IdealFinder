# from random import random
import json, random
import numpy as np
from numpy.random.mtrand import random_sample
from sklearn.cluster import KMeans

def kmeans(n_clusters=5, ids=[], embeddings=[]):
    km = KMeans(n_clusters=n_clusters, random_state=42)
    ids = np.array(ids)
    embeddings = np.array(embeddings)
    km.fit(embeddings)
    y_labels = km.labels_
    clusters = []
    for n in range(n_clusters):
        clusters.append([ids[np.where(y_labels==n)], embeddings[np.where(y_labels==n)]])
    return clusters


def get_response(ids=[], embeddings=[], stage=1, choices=[]):
    stages = [8, 6, 4, 2, 1]
    if stage == len(stages)+1:
        return False
    clusters = kmeans(n_clusters=stages[stage-1], ids=ids, embeddings=embeddings)
    response = {}
    response['cluster_info'] = {}
    for i, c in enumerate(clusters):
        cluster_ids, cluster_embeddings = c[0], c[1]
        c = list(zip(cluster_ids, cluster_embeddings))
        if stage == len(stages):
            sampled = choices
            print(sampled)
        else:
            sampled = random.sample(c,1)
        nearest = [n[0] for n in get_near_five(center=sampled, cluster=c)]
        response['cluster_info'][i] = {'sample': [s[0] for s in sampled], 'nearest': nearest, 'ids': cluster_ids}
    response['result'] = True if stage == len(stages) else False
    return response

def euclidean_dist(inst1, inst2):
    return np.linalg.norm(inst1-inst2)

def get_near_five(center=[], cluster=[]):
    embeddings = np.array([np.array(c[1]) for c in center])
    average_embed = embeddings.sum(axis=0) / len(center)
    cluster.sort(key=lambda x: euclidean_dist(average_embed, x[1]))
    return cluster[:min(len(cluster), 6)]

