import sqlite3
import process
import os
from pathlib import Path
import random

dataset_path = os.path.join(os.path.dirname(__file__), 'dataset')
gender = ['male', 'female']
# print(os.listdir('))


def init_db():
    for g in gender:
        try:
            process.imageinfo_to_db(os.path.join(dataset_path, g+'.csv'), 'myidol_imageinfo', gender=g)
        except Exception as e:
            print(e)
            pass

process.cluster_to_db(os.path.join(dataset_path, 'female_cluster.csv'), 'myidol_clusterinfo', preprocess=True)


# if __name__ == "__main__":
#     init_db()
