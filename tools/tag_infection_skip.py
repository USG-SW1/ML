#!/usr/bin/env python3
from elasticsearch import Elasticsearch
#from elasticsearch import RequestConfig
import sys
from datetime import datetime
import json

def search_all_documents(operation, doc_id, rule):
    """
    Searches all documents in the Elasticsearch index and updates the infection status based on the provided operation.

    Args:
      operation (str): The operation to perform. If '+r', sets the infection status to 'fw_should_skip'. Otherwise, sets it to null.
      doc_id (str): The document ID to search for.
      rule (str): The rule to apply for the search.

    Returns:
      dict: The response from the Elasticsearch update_by_query operation.

    Example:
      >>> res = search_all_documents('+r', '12345', 'some_rule')
      >>> print(res)

    Note:
      The `rule.conf` file should contain paths to rule files, each on a new line. Lines starting with '#' are ignored.
    """
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
    # Read rules from files listed in rule.conf
    rules = []
    with open('./infection_rules/all_rules.conf', 'r') as rule_conf:
      combined_rules = []
      for line in rule_conf:
        line = line.strip()
        if line and not line.startswith('#'):
          with open(line, 'r') as rule_file:
            rule = json.load(rule_file)
            combined_rules.append(rule)

    rules = combined_rules

    data = {
      "query": {
        "bool": {
          "filter": [
            {
              "bool": {
                "should": rules,
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
    print(data)
    sys.exit(1)
    es = Elasticsearch(hosts=["http://localhost:9200"])
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
