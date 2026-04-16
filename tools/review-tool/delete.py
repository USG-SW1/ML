import json
import sys
import datetime
from elasticsearch import Elasticsearch

# Elasticsearch host
es_host = "http://localhost:9200"
# es_host = "http://192.168.109.59:9200"

def delete_es_data_by_date_and_condition(index_name, target_date):
    """
    Delete Elasticsearch documents for a specific date where ai_comment is empty.

    Args:
        index_name (str): Elasticsearch index name
        target_date (str): Date in YYYY-MM-DD format
    """
    es = Elasticsearch([es_host])

    # Calculate date range (full day)
    start_date = datetime.datetime.fromisoformat(target_date)
    end_date = start_date + datetime.timedelta(days=1)

    # Query to find documents with empty ai_comment
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "first_seen_time": {
                                "gte": start_date.isoformat(),
                                "lt": end_date.isoformat()
                            }
                        }
                    },
                    {
                        "bool": {
                            "should": [
                                {"bool": {"must_not": {"exists": {"field": "ai-comment"}}}},
                                {"term": {"ai-comment": ""}}
                            ]
                        }
                    }
                ]
            }
        }
    }

    print(f"Deleting documents from index '{index_name}' for date '{target_date}' where ai_comment is empty")
    print(f"Query: {json.dumps(query, indent=2)}")

    try:
        response = es.delete_by_query(
            index=index_name,
            body=query,
            wait_for_completion=True
        )
        deleted = response.get('deleted', 0)
        print(f"Deleted {deleted} documents")
    except Exception as e:
        print(f"Error deleting documents: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python delete.py <index_name> <date in YYYY-MM-DD format>")
        sys.exit(1)

    index_name = sys.argv[1]
    target_date = sys.argv[2]

    try:
        datetime.datetime.fromisoformat(target_date)
    except ValueError:
        print("Error: date must be in ISO 8601 format (YYYY-MM-DD)")
        sys.exit(1)

    print(f"Index: {index_name}")
    print(f"Date: {target_date}")
    delete_es_data_by_date_and_condition(index_name, target_date)

