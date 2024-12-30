#!/usr/bin/env python3
from elasticsearch import Elasticsearch
#from elasticsearch import RequestConfig
import sys
from datetime import datetime

def search_all_documents(index_name, operation, doc_id, number):
    """查詢指定索引中的所有文件

    Args:
        index_name (str): 索引名稱
        operation (str): 操作類型
        doc_id (str): 文件ID
        number (str): 數字

    Returns:
        dict: 查詢結果
    """
    #old_index = "webml"
    pipeline = "webml_pipeline"

    if operation == "+r":
      review_str = True
    else:
      review_str = False

    if number == "1":
      web_ml_type = "Attacked"
    elif number == "2":
      web_ml_type = "False_Alert"
    elif number == "3":
      web_ml_type = "TBD"
    else:
      #web_ml_type = ""
      web_ml_type = "Reset"

    last_modify_time = datetime.now().isoformat()
    if web_ml_type == "Reset":
      ctx_ml_string=f"ctx._source.web_ml_type = null "
    else:
      ctx_ml_string=f"ctx._source.web_ml_type = '{web_ml_type}'"

    #ctx_ml_string=f"ctx._source.web_ml_type = '{web_ml_type}'"
    print(ctx_ml_string)
    data={
        "query": {
          "bool": {
            "filter": [
              {
                "bool": {
                  "should": [
                    {
                      "bool": {
                        "should": [
                          {
                            "match_phrase": {
                              "user_agent": "() { _; } >_[$($())] { echo Content-Type: text/plain ; echo ; echo \"bash_cve_2014_6278 Output : $((96+59))\"; }"
                            }
                          }
                        ],
                        "minimum_should_match": 1
                      }
                    },
                    {
                      "bool": {
                        "should": [
                          {
                            "match_phrase": {
                              "user_agent": "Expanse, a Palo Alto Networks company, searches across the global IPv4 space multiple times per day to identify customers&#39; presences on the Internet. If you would like to be excluded from our scans, please send IP addresses/domains to: scaninfo@paloaltonetworks.com"
                            }
                          }
                        ],
                        "minimum_should_match": 1
                      }
                    },
                    {
                      "bool": {
                        "should": [
                          {
                            "match_phrase": {
                              "user_agent": "FAST-WebCrawler/3.8 (crawler at trd dot overture dot com; http://www.alltheweb.com/help/webmaster/crawler)"
                            }
                          }
                        ],
                        "minimum_should_match": 1
                      }
                    },
                    {
                      "bool": {
                        "should": [
                          {
                            "match_phrase": {
                              "user_agent": "Hello World"
                            }
                          }
                        ],
                        "minimum_should_match": 1
                      }
                    },
                    {
                      "bool": {
                        "should": [
                          {
                            "match_phrase": {
                              "user_agent": "() { ignored; }; echo Content-Type: text/plain ; echo ; echo \"bash_cve_2014_6271_rce Output : $((8+58))\""
                            }
                          }
                        ],
                        "minimum_should_match": 1
                      }
                    },
                    {
                      "bool": {
                        "should": [
                          {
                            "match_phrase": {
                              "user_agent": "${jndi:iiop"
                            }
                          }
                        ],
                        "minimum_should_match": 1
                      }
                    },
                    {
                      "bool": {
                        "should": [
                          {
                            "match_phrase": {
                              "user_agent": "${jndi:ldap"
                            }
                          }
                        ],
                        "minimum_should_match": 1
                      }
                    },
                    {
                      "bool": {
                        "should": [
                          {
                            "match_phrase": {
                              "user_agent": "() { _; } >_[$($())] { echo Content-Type: text/plain ; echo ; echo \"bash_cve_2014_6278 Output : $((96+59))\"; }"
                            }
                          }
                        ],
                        "minimum_should_match": 1
                      }
                    },
                    {
                      "bool": {
                        "should": [
                          {
                            "match_phrase": {
                              "user_agent": "() { _; } >_[$($())] { echo Content-Type: text/plain ; echo ; echo \"bash_cve_2014_6278 Output : $((52+42))\"; }"
                            }
                          }
                        ],
                        "minimum_should_match": 1
                      }
                    },
                    {
                      "bool": {
                        "should": [
                          {
                            "match_phrase": {
                              "user_agent": "${jndi:nis"
                            }
                          }
                        ],
                        "minimum_should_match": 1
                      }
                    },
                    {
                      "bool": {
                        "should": [
                          {
                            "match_phrase": {
                              "user_agent": "${jndi:corba"
                            }
                          }
                        ],
                        "minimum_should_match": 1
                      }
                    },
                    {
                      "bool": {
                        "should": [
                          {
                            "match_phrase": {
                              "user_agent": "${jndi:nds"
                            }
                          }
                        ],
                        "minimum_should_match": 1
                      }
                    },
                    {
                      "bool": {
                        "should": [
                          {
                            "match_phrase": {
                              "user_agent": "${jndi:ldaps"
                            }
                          }
                        ],
                        "minimum_should_match": 1
                      }
                    },
                    {
                      "bool": {
                        "should": [
                          {
                            "match_phrase": {
                              "user_agent": "CVE-2023-20198"
                            }
                          }
                        ],
                        "minimum_should_match": 1
                      }
                    },
                    {
                      "bool": {
                        "should": [
                          {
                            "match_phrase": {
                              "user_agent": "<script>alert(Qualys)</script>"
                            }
                          }
                        ],
                        "minimum_should_match": 1
                      }
                    },
                    {
                      "bool": {
                        "should": [
                          {
                            "match_phrase": {
                              "user_agent": "() { ignored; }; echo Content-Type: text/plain ; echo  ; echo ; /usr/bin/id"
                            }
                          }
                        ],
                        "minimum_should_match": 1
                      }
                    },
                    {
                      "bool": {
                        "should": [
                          {
                            "match_phrase": {
                              "user_agent": "() { ignored; }; echo Content-Type: text/plain ; echo ; echo \"bash_cve_2014_6271_rce Output : $((46+22))\""
                            }
                          }
                        ],
                        "minimum_should_match": 1
                      }
                    },
                    {
                      "bool": {
                        "should": [
                          {
                            "match_phrase": {
                              "user_agent": "kmdjdheyytgebfghehhenegsdfsdf"
                            }
                          }
                        ],
                        "minimum_should_match": 1
                      }
                    }
                  ],
                  "minimum_should_match": 1
                }
              },
              {
                "range": {
                  "first_seen_time": {
                    "format": "strict_date_optional_time",
                    "gte": "now-2d/d",
                    "lte": "now"
                  }
                }
              }
            ]
          }
            },
              "script": {
                  "source": ctx_ml_string
                }
        }



    es = Elasticsearch(hosts=["http://localhost:9200"])
    #es = Elasticsearch(hosts=["http://localhost:9200"], request_config=RequestConfig(connect_timeout=160,socket_timeout=900))
    #res = es.search(index=old_index, body=)
    #res = es.reindex(body=)
    #res = es.count(index=old_index, body=)
    #res = es.index(index=old_index, body=)
    #print(res['count'])

    #res = es.update_by_(
    #res = es.update_by_query(
    #res = es.index(
    #res = es.update(
    res = es.update_by_query(
        index=index_name,
        body=data
    )

    return res

if __name__ == "__main__":
    if len(sys.argv) != 2:
        if len(sys.argv) != 5:
            print("Usage: python tag_review.py <index_name> <+r|-r> <id> [1...4]")
            sys.exit(1)

        index_name = sys.argv[1]
        operation = sys.argv[2]
        doc_id = sys.argv[3]
        number = sys.argv[4]

        if not isinstance(index_name, str):
            print("Error: <index_name> must be a string")
            sys.exit(1)

        if operation not in ["+r", "-r"]:
            print("Error: <+r|-r> must be either '+r' or '-r'")
            sys.exit(1)

        if not doc_id.isalnum() or len(doc_id) != 20:
            print("Error: <id> must be 20 alphanumeric characters")
            sys.exit(1)

        if number not in ["1", "2", "3", "4"]:
            print("Error: [1...4] must be a number between 1 and 4")
            sys.exit(1)

    index_name = sys.argv[1]
    result = search_all_documents(index_name, operation, doc_id, number)
    print(result)
