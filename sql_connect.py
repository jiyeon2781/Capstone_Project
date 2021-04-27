import MySQLdb
import requests
import json
import urllib
import os
import shutil
import time

while True:
    conn = MySQLdb.connect(host = '**.**.**.**', port=59762, user = 'root', password='****', database='potato', charset='utf8') 
    cursor = conn.cursor()
    sql = "select capture_image from CaptureImage"
    cursor.execute(sql)
    datas = cursor.fetchall()
    if len(datas) == 1:
        info_url = requests.get("DB Information URL(Json Format)")
        text = info_url.text
        data =json.loads(text)
        capture_image_name = data[0]['capture_image']
        image_url = "DB Image URL" + capture_image_name
        urllib.request.urlretrieve(image_url, capture_image_name)
        os.system('python image_download.py')
        os.system('python search.py')
        delete_sql = 'delete from CaptureImage'
        cursor.execute(delete_sql)
        conn.commit()
    else:
        print("Waitning for image...")
        continue 

	
