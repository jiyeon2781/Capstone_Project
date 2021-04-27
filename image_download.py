import requests
import json
import urllib
import os
import shutil
import time
start = time.time()
my_path = os.path.dirname(os.path.realpath(__file__)) + '/images/pet_image/'
print(my_path)
info_url = requests.get("DB Information URL")

text = info_url.text
data =json.loads(text)
user = data[0]
print(len(data))

if os.path.exists(my_path):
    shutil.rmtree("./images/pet_image")

if not os.path.exists(my_path):
    os.makedirs(my_path)


for i in range(len(data)):
    image_url = "DB Image URL" + data[i]['img']
    print(image_url)
    image_path = my_path+data[i]['img']
    print(image_path)
    urllib.request.urlretrieve(image_url, image_path)

print(time.time() - start)

