#!/usr/bin/env python3
from elasticsearch import Elasticsearch
import sys

def search_all_documents(index_name, webml_prefix):
    """查詢指定索引中的所有文件

    Args:
        index_name (str): 索引名稱

    Returns:
        dict: 查詢結果
    """
    old_index = index_name
    new_index = "unconfirm_webml_"+webml_prefix
    print(old_index, new_index)
    #return 0

    data = {
            "source":{
                "index": old_index,
                "query": {
                  "bool":{
                    "must":[
                       {
                          "exists": {
                            "field": "user_agent"
                          }
                       },
                       {
                          "range": {
                             "first_seen_time": {
                                "gte": "now-2d",
                                "lte": "now-1d"
                             }
                          }
                       }
                      ],
                      "must_not": [
                        {
                          "match_phrase": {
                            "user_agent": "TheGreenBow-VPNClient/5.0"
                          }
                        },
                        {
                          "match_phrase": {
                            "user_agent": "Mozilla"
                          }
                        },
                        {
                          "match_phrase": {
                            "user_agent": "Go-http-client/1.1"
                          }
                        },
                        {
                          "match_phrase": {
                            "user_agent": "python-requests/2.32.3"
                          }
                        },
                        {
                          "match_phrase": {
                            "user_agent": "python-requests/2.26.0"
                          }
                        },
                        {
                          "match_phrase": {
                            "user_agent": "python-requests"
                          }
                        },
                        {
                          "match_phrase": {
                            "user_agent": "python-httpx"
                          }
                        },
                        {
                          "match_phrase": {
                            "user_agent": "SSLVPN-Client/3.0"
                          }
                        }
                      ]
                  }
                }
                },
             "dest":{"index":new_index}
         }

    es = Elasticsearch(hosts=["http://localhost:9200"])
    #res = es.search(index=old_index, body=data)
    res = es.reindex(body=data)
    #res = es.count(index=old_index, body=data)
    #print(res['count'])

    return res

if __name__ == "__main__":
    #index_name = "test"
    index_name = sys.argv[1]
    webml_prefix = sys.argv[2]
    print(sys.argv[1], webml_prefix)
    result = search_all_documents(index_name, webml_prefix)
    print(result)
