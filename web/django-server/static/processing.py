import mtcnn
import os
from PIL import Image
import matplotlib.pyplot as plt
from mtcnn.mtcnn import MTCNN
import numpy as np

# 주어진 사진에서 하나의 얼굴 추출
def extract_face(filename, required_size=(160, 160), save=False):
    print(filename)
    # 파일에서 이미지 불러오기
    image = Image.open(filename)
    # RGB로 변환, 필요시
    image = image.convert('RGB')
    # 배열로 변환
    pixels = np.asarray(image)
    # 감지기 생성, 기본 가중치 이용
    detector = MTCNN()
    # 이미지에서 얼굴 감지
    results = detector.detect_faces(pixels)
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
    face = pixels[y1:y2, x1:x2]
    # 모델 사이즈로 픽셀 재조정
    # Image.fromarray() : 배열 객체를 입력으로 받아 배열 객체에서 만든 이미지 객체를 반환
    image = Image.fromarray(face)
    image = image.resize(required_size)
    # face data 저장
    if save == True:
        face_path = filename.split('/')
        jpg = face_path[-1].split('.')[0]+'.jpg'
        face_path[-1] = jpg
        face_path.insert(-2,'face_data')
        face_path = os.path.join(*face_path)
        image.save(face_path)
    face_array = np.asarray(image)
    return face_array

# 디렉토리 안의 모든 이미지를 불러오고 이미지에서 얼굴 추출
def load_faces(directory):
    faces = list()
    # 얼굴이 아예 검출되지 않은 경우, filename 확인
    no_face = list()
    # 파일 열거
    for filename in sorted(os.listdir(directory)):
        # 경로
        path = directory + '/' + filename
        # 얼굴 추출
        face = extract_face(path)
        # 얼굴 사진 따로 저장해서 확인하고 싶으면 save = True로 해서 돌리기
        # face = extract_face(path,(160,160),True)
        if len(face) == 0:
            no_face.append(filename)
        # 저장
        else:
            faces.append(face)
    # extrac_face할때, 얼굴이 검출되지 않은 경우 []을 리턴했기 때문에 제거하는 과정 
    faces = list(filter(lambda x: len(x)>0, faces))
    return faces, no_face

# 검출된 얼굴 데이터를 array로 저장 -> 나중에 FaceNet이 이 파일 load해서 입력으로 쓸 수 있도록
drive_path = './drive/MyDrive/devcourse_modeling/'
path = os.path.join(drive_path, 'dataset')
gender = ['female', 'male']
for g in gender:
    dataset_path = os.path.join(path, g)
    faces, no_face = load_faces(dataset_path)
    print('검출되지 않은 image 파일 :', no_face)
    print('{} dataset에서 검출된 face 개수 : {}'.format(g, len(faces)))
    faces = np.asarray(faces)
    np.savez_compressed(os.path.join(path,g+'_faces.npz'),faces)

# 입력으로 들어온 model과 face data로 embedding 구하기
# 각 성별 전체 얼굴 데이터 모두 embedding으로 변환하여 반환
def get_embeddings(model, faces_data):
    embeddings = list()
    for face_pixels in faces_data:
        # 픽셀 값의 척도
        face_pixels = face_pixels.astype('int32')
        # 채널 간 픽셀값 표준화(전역에 걸쳐)
        mean, std = face_pixels.mean(), face_pixels.std()
        face_pixels = (face_pixels - mean) / std
        samples = np.expand_dims(face_pixels, axis=0)
        # 임베딩을 갖기 위한 예측 생성
        embedding = model.predict(samples)
        embeddings.append(embedding[0])
    embeddings = np.asarray(embeddings)
    return embeddings

# Warning 뜨는데 사실 아직 안 찾아봤어요... 

from keras.models import load_model

# facenet 모델 불러오기
model = load_model(filepath=os.path.join(drive_path, 'facenet_keras.h5'))
print(model.inputs)
# 얼굴 데이터 불러오기
female_data = np.load(os.path.join(drive_path, 'female_faces.npz'))['arr_0']
# embedding 받아오기
female_embeddings = get_embeddings(model,female_data)
print(female_embeddings.shape)

'''
male_data = np.load(os.path.join(drive_path, 'dataset', 'male_faces.npz'))['arr_0']
male_embeddings = get_embeddings(model,male_data)
print(male_embeddings.shape)
'''

from sklearn.cluster import KMeans
# cluster 개수 지정
n = 10
# k-means++ : 가지고 있는 데이터 포인트 중에서 무작위로 1개를 선택하여 그 녀석을 첫번째 중심점으로 지정
# 근데 사실 init = 'k-means++'라고 안해줘도 기본값으로 되어있다고 함 
kmeans = KMeans(init="k-means++", n_clusters=n, random_state=0)
# female으로 할지 male로 돌릴지 정해주기
kmeans.fit(female_embeddings)
y_pred = kmeans.labels_

def viz_img(y_pred):
    n = 10
    fig = plt.figure(figsize=(50,50))
    box_index = 1
    for cluster in range(n):
        result = np.where(y_pred == cluster)
        for i in np.random.choice(result[0].tolist(), n, replace=False):
            ax = fig.add_subplot(n, n, box_index)
            plt.imshow(female_data[i])
            plt.gray()
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            box_index += 1
    plt.show()
    
viz_img(y_pred)