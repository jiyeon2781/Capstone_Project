import os
import numpy as np
from numpy.linalg import norm
import PIL
import time
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
import math
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
start = time.time()
img_size = 224
model_resnet = ResNet50(weights='imagenet', include_top=False,input_shape=(img_size, img_size, 3),pooling='max')

batch_size = 64
root_dir = './images'
img_generator = ImageDataGenerator(preprocessing_function = preprocess_input)
data_generator = img_generator.flow_from_directory(root_dir, target_size = (img_size,img_size), batch_size = batch_size, class_mode = None, shuffle=False)

num_images = data_generator.samples
num_epochs = int(math.ceil(num_images / batch_size))

feature_list = model_resnet.predict_generator(data_generator, num_epochs)

print("Num images   = ", len(data_generator.classes))
print("Shape of feature_list = ", feature_list.shape)

filenames = [root_dir + '/' + s for s in data_generator.filenames]

neighbors = NearestNeighbors(n_neighbors=5, algorithm='ball_tree', metric='euclidean')
neighbors.fit(feature_list)

test_file = "./cap_img01.jpg"

input_shape = (img_size, img_size, 3)
img = image.load_img(test_file, target_size=(input_shape[0], input_shape[1]))
img_array = image.img_to_array(img)
expanded_img_array = np.expand_dims(img_array, axis=0)
preprocessed_img = preprocess_input(expanded_img_array)
test_img_features = model_resnet.predict(preprocessed_img, batch_size=1)

_, indices = neighbors.kneighbors(test_img_features)

f = open("./result.txt", 'w')

def similar_images(indices):
    num = 1    
    for index in indices:
        if num<=len(indices) :
            print(filenames[index].split("/")[6])
            f.write(filenames[index].split("/")[6]+"\n")
    f.close()
print("Searct Time : ",time.time() - start)

print('Predict Result')
similar_images(indices[0])
