import pickle

import efficientnet.keras as efn
import numpy as np
import tensorflow
from keras.api._v2.keras.applications.efficientnet import preprocess_input
from keras.api._v2.keras.layers import GlobalMaxPooling2D
from keras.api._v2.keras.preprocessing import image
from numpy.linalg import norm
from sklearn.neighbors import NearestNeighbors

feature_list = pickle.load(open('base/static/model/embeddings.pkl', 'rb'))
filenames = pickle.load(open('base/static/model/filenames.pkl', 'rb'))

model = efn.EfficientNetB7(weights='imagenet', include_top=False,
                           input_shape=(224, 224, 3))
model.trainable = False

model = tensorflow.keras.Sequential([model, GlobalMaxPooling2D()])


def extract_features(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    result = model.predict(preprocessed_img).flatten()
    normalized_result = result / norm(result)
    return normalized_result


def recommend(features, feature_list):
    neighbors = NearestNeighbors(n_neighbors=6, algorithm='brute',
                                 metric='euclidean')
    neighbors.fit(feature_list)
    distances, indices = neighbors.kneighbors([features])
    return indices


def ai_interface(input_file):
    image_name_list = []
    features = extract_features(input_file, model)
    indices = recommend(features, feature_list)
    for file in indices[0]:
        temp_img = (filenames[file])

        image_name_list.append(temp_img.replace(r"\\", "/"))
    return image_name_list
