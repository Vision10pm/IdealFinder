import sqlite3
import process
import os
from pathlib import Path
import random

dataset_path = os.path.join(os.path.dirname(__file__), 'dataset')
gender = ['male', 'female']

def init_db():
    for g in gender:
        try:
            # process.imageinfo_to_db(os.path.join(dataset_path, g+'.csv'), 'myidol_imageinfo', gender=g, preprocess=True)
            # process.cluster_to_db(os.path.join(dataset_path, f'{g}_cluster.csv'), 'myidol_clusterinfo', preprocess=True)
            process.embedding_to_db(os.path.join(dataset_path, f'{g}_embeddings.csv'), 'myidol_embeddinginfo', preprocess=True)
            # process.update_embedding(os.path.join(dataset_path, f'{g}_embeddings.csv'), 'myidol_embeddinginfo', preprocess=True)
        except Exception as e:
            print(e)
            pass

if __name__ == "__main__":
    init_db()
