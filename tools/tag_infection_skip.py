#!/usr/bin/env python3
from elasticsearch import Elasticsearch
#from elasticsearch import RequestConfig
import sys
from datetime import datetime

def search_all_documents(operation, doc_id, rule):
    #old_index = "webml"
    pipeline = "infection-pipeline"
    if operation == '+r':
        ctx_ml_string = "ctx._source.infection_status = 'fw_should_skip'"
    else:
        ctx_ml_string = "ctx._source.infection_status = null "
    #sys.exit(1)
    rule_1 = {
            "bool": {
            "should": [
                {
                "match_phrase": {
                    "message": "The illegal process=\"/etc/ips/rate_based.pyc\"(/compress/usr/bin/python3.8), has been triggered, cmdline=\"/usr/bin/python /etc/ips/rate_based.pyc\""
                    }
                }
            ],
            "minimum_should_match": 1
            }
        }

    # print(rules)
    # sys.exit(1)
    data={
        "query": {
          "bool": {
            "filter": [
              {
                "bool": {
                  "should": [
                      rule_1,
                    {
                      "bool": {
                        "should": [
                          {
                            "match_phrase": {
                              "message": "The illegal process=\"/etc/ips/system_protection_port_check.pyc\"(/compress/usr/bin/python3.8), has been triggered, cmdline=\"python /etc/ips/system_protection_port_check.pyc\""
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
                  "time": {
                    "format": "strict_date_optional_time",
                    "gte": "now-3d/d",
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
    index_name = "infection"
    res = es.update_by_query(
        index=index_name,
        body=data
    )

    return res

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: tag_infection_skip.py <+r|-r> <id> <rule>")
        sys.exit(1)

    operation = sys.argv[1]
    doc_id = sys.argv[2]
    rule = sys.argv[3]

    if operation not in ["+r", "-r"]:
        print("Error: <+r|-r> must be either '+r' or '-r'")
        sys.exit(1)

    if not doc_id.isalnum() or len(doc_id) != 20:
        print("Error: <id> must be 20 alphanumeric characters")
        sys.exit(1)

    if not all(x.isdigit() for x in rule.split(',')) or len(rule) > 4096:
        print("Error: <rule> must be a comma-separated list of integers with a maximum length of 4096 characters")
        sys.exit(1)

    index_name = sys.argv[1]
    result = search_all_documents(operation, doc_id, rule)
    print(result)
