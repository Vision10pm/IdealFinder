import mtcnn
import os
from PIL import Image
import numpy as np

class Ideal_finder:
    def __init__(self, n_cluster=2, dataset_path = "."):
        from sklearn.cluster import KMeans
        self.dataset_path = dataset_path
        self.n_cluster = n_cluster
        self.model = KMeans(n_clusters=n_cluster, random_state=2)
    # 주어진 사진에서 하나의 얼굴 추출
    def extract_face(self, file_name, required_size=(160, 160), save=False):
        from mtcnn.mtcnn import MTCNN
        print(file_name)
        # 파일에서 이미지 불러오기
        image = Image.open(file_name)
        # RGB로 변환, 필요시
        image = image.convert('RGB')
        # 배열로 변환
        pixels = np.asarray(image)
        # 감지기 생성, 기본 가중치 이용
        detector = MTCNN()
        # 이미지에서 얼굴 감
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
            face_path = file_name.split('/')
            jpg = face_path[-1].split('.')[0]+'.jpg'
            face_path[-1] = jpg
            face_path.insert(-2,'face_data')
            face_path = os.path.join(*face_path)
            image.save(face_path)
        face_array = np.asarray(image)
        return face_array

    # 디렉토리 안의 모든 이미지를 불러오고 이미지에서 얼굴 추출
    def load_faces(self, directory):
        faces = list()
        # 얼굴이 아예 검출되지 않은 경우, file_name 확인
        no_face = list()
        # 파일 열거
        for file_name in sorted(os.listdir(directory)):
            # 경로
            path = directory + '/' + file_name
            # 얼굴 추출
            face = self.extract_face(path)
            # 얼굴 사진 따로 저장해서 확인하고 싶으면 save = True로 해서 돌리기
            # face = extract_face(path,(160,160),True)
            if len(face) == 0:
                no_face.append(file_name)
            # 저장
            else:
                faces.append(face)
        # extrac_face할때, 얼굴이 검출되지 않은 경우 []을 리턴했기 때문에 제거하는 과정 
        faces = list(filter(lambda x: len(x)>0, faces))
        return faces, no_face

    # 검출된 얼굴 데이터를 array로 저장 -> 나중에 FaceNet이 이 파일 load해서 입력으로 쓸 수 있도록
    def embed(save=False):
        drive_path = './drive/MyDrive/devcourse_modeling/'
        path = os.path.join(drive_path, 'dataset')
        gender = ['female_fix', 'male_fix']
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
    def preprocessing(self):
        pass

    def fit(self):
        from sklearn.cluster import KMeans
        # cluster 개수 지정
        n = 10
        # k-means++ : 가지고 있는 데이터 포인트 중에서 무작위로 1개를 선택하여 그 녀석을 첫번째 중심점으로 지정
        # 근데 사실 init = 'k-means++'라고 안해줘도 기본값으로 되어있다고 함 
        kmeans = KMeans(init="k-means++", n_clusters=n, random_state=0)
        # female으로 할지 male로 돌릴지 정해주기
        kmeans.fit(female_embeddings)
        y_pred = kmeans.labels_