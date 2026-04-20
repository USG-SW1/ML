#!/usr/bin/env python3

import requests
import json
import sys
from datetime import datetime,timedelta

# Elasticsearch 的 host 和 port
es_host = "http://localhost:9200"


current_date = datetime.now() - timedelta(days=1)
year = current_date.year
month = current_date.month
day = current_date.day

def patch_by_date(ml_type, pass_path, pass_date):
    '''
    if day < 10:
        download_webml_json_file = f"{str(year) + '-' + str(month) + '-' + '0' + str(day) + '_webml.json'}"
        download_infection_json_file = f"{str(year) + '-' + str(month) + '-' + '0' + str(day) + '_infection.json'}"
    else:
        download_webml_json_file = f"{str(year) + '-' + str(month) + '-' + str(day) + '_webml.json'}"
        download_infection_json_file = f"{str(year) + '-' + str(month) + '-' + str(day) + '_infection.json'}"
    '''
    download_json_file = f"{pass_date + '_' + ml_type + '.json'}"
    print(download_json_file)

    #sys.exit(1)
    # 要傳送的資料
    #data = {
    #    "message": "Hello, Elasticsearch from Python!",
    #    "@timestamp": datetime.now().isoformat()
    #}

    # 讀取 JSON 檔案
    #index_name = "webml"
    index_name = ml_type
    with open(download_json_file, 'r') as f:
    #with open('2024-11-28_webml.json', 'r') as f:
        # 建構 Bulk API 請求
        bulk_data = []
        count = 0
        for line in f:
            data = json.loads(line)
            action = {
            "index": {
                "_index": index_name
                }
            }
            bulk_data.append(action)
            bulk_data.append(data)
            url = f"{es_host}/{index_name}/_doc"
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, json=data)
            count = count + 1
            if response.status_code != 201:
                print(f"Error adding document: {response.text}")
            else:
                if (count + 1) % 30 == 0:  # 每30次印一點
                  print(ml_type + " index add item sucess, th-" + str(count) + "record")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python normalize.py <webml|infection> <path> <day>")
        sys.exit(1)

    ml_type = sys.argv[1]
    pass_path = sys.argv[2]
    pass_date = sys.argv[3]
    #output_file = sys.argv[2]
    print("type : " + ml_type)
    print("path : " + pass_path)
    print("date : " + pass_date)
    #sys.exit()
    patch_by_date(ml_type, pass_path, pass_date)
