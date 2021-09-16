import datetime
import pandas as pd
import numpy as np
from pathlib import Path
from PIL import Image
from myidol.models import EmbeddingInfo, ImageInfo
from mtcnn.mtcnn import MTCNN
import os, random, joblib, json
import sqlite3
import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2
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

def extract_face(image, required_size=(160, 160), save=False):
    # RGB로 변환, 필요시
    # image = image.convert('RGB')
    # 배열로 변환
    # pixels = np.array(image)
    # 감지기 생성, 기본 가중치 이용
    detector = MTCNN()
    # 이미지에서 얼굴 감지
    results = detector.detect_faces(image)
    # 첫 번째 얼굴에서 경계 상자 추출
    # detect_faces의 결과물 : box, cofidence, keypoints(left_eye, right_eye, nose, mouth_left, mouth_right)
    # 사진 크기가 너무 작아서 detect가 안되는 경우가 있음 -> 우선 그런 영상들을 제외하고 진행
    if len(results)==0:
        return np.asarray([])
    x1, y1, width, height = results[0]['box']
    
    # 버그 수정
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    # 얼굴 추출
    face = image[y1:y2, x1:x2]
    # 모델 사이즈로 픽셀 재조정
    # Image.fromarray() : 배열 객체를 입력으로 받아 배열 객체에서 만든 이미지 객체를 반환
    image = Image.fromarray(face)
    image = image.resize(required_size)

    return image

def get_face_embedding(user_img=None, width=None, height=None):
    face_pixels = np.asarray(user_img)
    face_pixels = face_pixels.reshape(height, width, 3).astype(np.uint8)
    face_pixels = np.array(extract_face(face_pixels))
    # 픽셀 값의 척도
    # 채널 간 픽셀값 표준화(전역에 걸쳐)
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    samples = np.expand_dims(face_pixels, axis=0)
    # 임베딩을 갖기 위한 예측 생성
    modelFile = '/home/june/projects/kdt-server/IdealFinder/web/django-server/modeling/facenet_keras.h5'
    model = load_model(filepath=modelFile)
    user_embedding = model.predict(samples)
    return user_embedding


def get_embedding_diff(user_img, width, height, image_id):
    user_embedding = get_face_embedding(user_img, width, height)
    ideal_embedding = json.loads(EmbeddingInfo.objects.select_related().get(image_id_id=image_id).embedding)
    return get_score(user_embedding, ideal_embedding)

def get_similar_face(user_img, width, height):
    user_embedding = get_face_embedding(user_img, width, height)
    all_embedding = list(EmbeddingInfo.objects.select_related().all())
    print(len(all_embedding))
    print(all_embedding[0].image_id)

    all_embedding.sort(key=lambda x: np.linalg.norm(list(map(int, json.loads(x.embedding)))-user_embedding))
    print(all_embedding[:5])
    return list(map(lambda x: f'/static/img/{x.image_id.gender}/{x.image_id.get_file_name()}', all_embedding[:5]))

def get_score(a, b):
    return int(((np.dot(a, b) / (np.linalg.norm(a) * (np.linalg.norm(b))))+1)*50)