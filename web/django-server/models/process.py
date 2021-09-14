import datetime
import pandas as pd
import numpy as np
from pathlib import Path
from PIL import Image
# from myidol.models import EmbeddingInfo
import os
import sqlite3
MODEL_PATH  = os.path.join(os.path.dirname(__file__))
DATASET_PATH = os.path.join(os.path.dirname(__file__), 'dataset')
DB_PATH = os.path.join(os.path.dirname(MODEL_PATH), 'db.sqlite3')
print(DB_PATH)
datasets_dir = [os.path.join(DATASET_PATH, dir) for dir in os.listdir(DATASET_PATH)]


def imageinfo_to_db(path, target_table, gender=None, preprocess=False, db=DB_PATH):
    db_df = pd.read_csv(path)
    con = sqlite3.connect(db)
    if preprocess:
        db_df['format'] = db_df['file_name'].apply(lambda x: x.split('.')[1])
        db_df['file_name'] = db_df['file_name'].apply(lambda x: x.split('.')[0])
        db_df['gender'] = db_df['format'].apply(lambda x: gender)
        db_df['created_at'] = db_df['gender'].apply(lambda x: datetime.datetime.now().ctime())
        db_df['updated_at'] = db_df['gender'].apply(lambda x: datetime.datetime.now().ctime())
        # db_df.to_csv(f'{gender}_modified.csv')
    print(db_df)
    db_df.to_sql(target_table, con, if_exists='append', index=False)
    con.close()

def cluster_to_db(path, target_table, preprocess=False, db=DB_PATH):
    db_df = pd.read_csv(path)
    con = sqlite3.connect(db)
    if preprocess:
        db_df['cluster'] = db_df.apply(lambda x: str(x['cluster_1']) + str(x['cluster_2']) + str(x['cluster_3']), axis=1)
    db_df = db_df.loc[:, ['image_id_id', 'cluster']]
    print(db_df)
    db_df.to_sql(target_table, con, if_exists='append', index=False)
    con.close()

def embedding_to_db(path, target_table, preprocess=False, db=DB_PATH):
    db_df = pd.read_csv(path)
    con = sqlite3.connect(db)
    if preprocess:
        db_df['image_id_id'] = db_df['image_id_id'].apply(lambda x: int(x))
        db_df['embedding'] = db_df.iloc[:, 1:129].apply(lambda x: str(list(x)), axis=1)
    db_df = db_df.loc[:, ['image_id_id', 'embedding']]
    print(db_df)
    db_df.to_sql(target_table, con, if_exists='append', index=False)
    con.close()

# def update_embedding(path, target_table, preprocess=False, db=DB_PATH):
#     db_df = pd.read_csv(path)
#     con = sqlite3.connect(db)
#     db_df.map(lambda x: EmbeddingInfo.objects.get(image_id_id=x['image_id_id']).update(embedding=x[1:129]))
#     con.close()
