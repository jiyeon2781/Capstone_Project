import MySQLdb
import requests
import json
import urllib
import os
import shutil
import time

while True:
    conn = MySQLdb.connect(host = '**.**.**.**', port=7777, user = 'root', password='*******', database='potato', charset='utf8')
    cursor = conn.cursor() 
    sql = "select name from CaptureImage"
    cursor.execute(sql)
    datas = cursor.fetchall() #정보 받아오기
    if len(datas) == 1:
        start = time.time()
        info_url = requests.get("DB Information URL(Json Format)")
        text = info_url.text
        data =json.loads(text)
        capture_image_name = data[0]['name']
        image_url = ""DB Image URL" + capture_image_name
        urllib.request.urlretrieve(image_url, capture_image_name)
        os.system('python image_download.py')
        os.system('python search.py')
        result_file = open('./result.txt', 'rb')
        rank = 1
        val = []
        while True:
            line = result_file.readline()
            if not line: break
            val.append((rank, str(line).split('\\')[0][2:]))
            rank += 1
        delete_sql = 'delete from CaptureImage'
        delete_result_sql = 'delete from ResultImage'
        insert_result_sql = 'insert into ResultImage (rank, name) values (%s, %s)'
        cursor.execute(delete_sql)
        cursor.execute(delete_result_sql)
        cursor.executemany(insert_result_sql, val)
        conn.commit()
        print("Total Time :",time.time() - start)
    else:
        print("Waiting for image...")
        continue

	
