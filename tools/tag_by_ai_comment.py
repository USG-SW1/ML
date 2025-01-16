!/usr/bin/env python3
#from datetime import datetime,timedelta
import os
import json
import pandas as pd
import sys
import datetime
import ollama
from elasticsearch import Elasticsearch

# Elasticsearch 的 host 和 port
es_host = "http://localhost:9200"

def update_elasticsearch_index(index_name, target_day, days_num):
    """
    根據指定的日期，從Elasticsearch中取出資料，經過自訂的判斷，更新field name為 ‘ai-comment’ 的內容

    Args:
        index_name (str): Elasticsearch的index名稱
        target_day (str): 查詢的起始日期
        days_num (int): 查詢的天數，可以是正數或負數
    """
    es = Elasticsearch([es_host])

    # 計算查詢的日期範圍
    start_date = datetime.datetime.fromisoformat(target_day)
    if days_num.startswith('+'):
        days_num = int(days_num[1:])
        end_date = start_date + datetime.timedelta(days=days_num)
    elif days_num.startswith('-'):
        days_num = int(days_num[1:])
        end_date = start_date
        start_date = start_date - datetime.timedelta(days=days_num)
    else:
        days_num = int(days_num)
        end_date = start_date + datetime.timedelta(days=days_num)

    # 查詢Elasticsearch中的資料
    query = {
        "query": {
            "range": {
                "first_seen_time": {
                    "gte": start_date.isoformat(),
                    "lte": end_date.isoformat()
                }
            }
        }
    }

    #response = es.search(index=index_name, body=query, scroll='2m', size=100)
    response = es.search(index=index_name, body=query, scroll='10m')
    scroll_id = response['_scroll_id']
    hits = response['hits']['hits']
    print("hits = " + str(len(hits)))
    updated = False
    while len(hits) > 0:
        for hit in hits:
            doc_id = hit['_id']
            source = hit['_source']
            features = source.get('feature_raw', '')
            ai_comment = source.get('ai_comment', '')
            print('ai_comment len=' , len(ai_comment))
            print('update _id =' + doc_id)
            if len(ai_comment) < 12:
                if features:
                    severity, comment = query_ai_qwen(features)
                    es.update(
                        index=index_name,
                        id=doc_id,
                        body={
                            "doc": {
                                "ai_comment": comment,
                                "severity": severity
                            }
                        }
                    )
                    updated = True
        response = es.scroll(scroll_id=scroll_id, scroll='3m')
        scroll_id = response['_scroll_id']
        hits = response['hits']['hits']

    es.clear_scroll(scroll_id=scroll_id)
    return updated

def query_ai_qwen(features):
    """
    根據輸入的提示詞，返回兩個字串，第一個是嚴重性，第二個是AI的評論

    Args:
        prompt (str): 提示詞

    Returns:
        tuple: (severity, comment)
    """
    """
    prompt = (
        "Here is a http content. Analysis it and provide an attacked levels. "
        "normal: it's a normal content. low: It is an abnormal content, but "
        "it's not an attacked. medium: it's an attacked and just have a try. "
        "high: it's an attacked, suggest admin verify the behavior "
        "on http server. The answer format, Attack risk level: <normal or low or medium or high>. "
        "And simple comment. No need any code."
    )

    prompt = (
        "Here is a http content. Analysis it and provide an attacked levels. "
        "1 to 10 points, 1 is low risk and 9 is high risk. "
        "Give 10 directly, if it hits at least one attacked feature. "
        "The answer format, Attack risk level: <point>.  And simple comment. No need any code. "
    )

    prompt = (
        "Here is a http content. Analysis it and provide an attacked levels. "
        "1 to 10 points, 1 is low risk and 10 is high risk. "
        "The answer format, Attack risk level: <point>.  And simple comment. No need any code. "
    )
    """

    prompt = (
        "Evaluate the given HTTP content for signs of: "
        "1. SQL injection "
        "2. Cross-site scripting (XSS) "
        "3. Remote code execution (RCE) "
        "4. Command injection "
        "5. Malware delivery "
        "6. Data exfiltration "
        "7. Denial-of-service (DoS) attacks "
        "8. Reverse shell establishment Rate the overall threat level on a scale of 1 to 10. "
        "Output format as following, Attack risk level: <level> (DONT contain  **) "
        "And provide Detail comment. (DONOT print 1~8 rule by rule which did not hit.) "
    )

    #p= f"prompt + '\n' + features"
    #print(prompt + '\n' + features)
    #os.exit()
    stream = ollama.chat(
        model='qwen2.5-coder:32b',
        messages=[{'role': 'user', 'content': prompt + '\n' + features}],
        stream=True
        )

    # 取得AI的回應
    severity = 'unknown'
    comment = ''
    for response in stream:
        #print(response['message']['content'], end='', flush=True)
        response_content = response['message']['content']
        #if 'Attack risk level:' in response_content:
        #    severity = response_content.split('Attack risk level:')[1].split('.')[0].strip()
        comment = comment + response_content
        #print(response_content)
        print(response['message']['content'], end='', flush=True)
        #print("aaaaaaa\n")
    if 'Attack risk level:' in comment:
       severity = comment.split('Attack risk level:')[1].split('\n')[0].strip()
       severity = ''.join(filter(str.isdigit, severity[:2]))
    print(comment)
    print(severity)
    # 模擬AI的回應
    #comment = 'This is a simulated AI response.'
    # 根據提示詞進行一些簡單的判斷

    return severity, comment

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: ai_comment_update.py <index name> <day> <+d|-d>")
        sys.exit(1)

    index_name = sys.argv[1]
    target_day = sys.argv[2]
    days_num = sys.argv[3]

    # Check if target_day is in ISO 8601 format
    try:
        datetime.datetime.fromisoformat(target_day)
    except ValueError:
        print("Error: target_day must be in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
        sys.exit(1)

    # Validate days_num is an integer and can be negative or positive
    try:
        days_num = int(days_num)
    except ValueError:
        print("Error: days_num must be an integer (positive or negative)")
        sys.exit(1)

    print("Index Name : " + index_name)
    print("Star query day : " + target_day)
    print("number  : " + str(days_num))

    retries = 0
    max_retries = 10
    updated = update_elasticsearch_index(index_name, target_day, str(days_num))

    while updated and retries < max_retries:
        print(f"Update successful, retrying... ({retries + 1}/{max_retries})")
        updated = update_elasticsearch_index(index_name, target_day, str(days_num))
        retries += 1

    if retries == max_retries:
        print("Reached maximum retries.")
    else:
        print("Update completed.")      
