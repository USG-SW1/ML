import sys
import pandas as pd
from elasticsearch import Elasticsearch
import datetime
import os

# Usage: python compare_counts.py <index_name> <start_date> <days_num> <csv_path>
# Example: python compare_counts.py webml 2023-12-07 +1 webml_2023-12-07_1.csv

if len(sys.argv) != 5:
    print("Usage: python compare_counts.py <index_name> <start_date> <days_num> <csv_path>")
    sys.exit(1)

index_name = sys.argv[1]
start_date = sys.argv[2]
days_num = sys.argv[3]
csv_path = sys.argv[4]

# Parse date range
start_dt = datetime.datetime.fromisoformat(start_date)
if days_num.startswith('+'):
    days_int = int(days_num[1:])
    end_dt = start_dt + datetime.timedelta(days=days_int)
elif days_num.startswith('-'):
    days_int = int(days_num[1:])
    end_dt = start_dt
    start_dt = start_dt - datetime.timedelta(days=days_int)
else:
    days_int = int(days_num)
    end_dt = start_dt + datetime.timedelta(days=days_int)

# Query ES for count
es = Elasticsearch(["http://localhost:9200"])
query = {
    "query": {
        "range": {
            "first_seen_time": {
                "gte": start_dt.isoformat(),
                "lte": end_dt.isoformat()
            }
        }
    }
}
try:
    es_count = es.count(index=index_name, body=query)["count"]
except Exception as e:
    print("Error querying Elasticsearch:", e)
    es_count = None

# Query ES for count with non-empty ai_comment and severity
query_with_fields = {
    "query": {
        "bool": {
            "must": [
                {"range": {"first_seen_time": {"gte": start_dt.isoformat(), "lte": end_dt.isoformat()}}},
                {"exists": {"field": "ai_comment"}},
                {"exists": {"field": "severity"}}
            ]
        }
    }
}
try:
    es_count_with_fields = es.count(index=index_name, body=query_with_fields)["count"]
except Exception as e:
    print("Error querying Elasticsearch for ai_comment and severity:", e)
    es_count_with_fields = None

# Count rows in CSV
try:
    df = pd.read_csv(csv_path)
    csv_count = len(df)
except Exception as e:
    print("Error reading CSV:", e)
    csv_count = None

# Compare local CSV _id values with ES _id values for the same range
if '_id' in df.columns:
    csv_ids = set(df['_id'].astype(str))
    # Fetch all ES _id values for the same range
    es_ids = set()
    search_query = {
        "size": 1000,
        "_source": ["_id"],
        "query": {
            "bool": {
                "must": [
                    {"range": {"first_seen_time": {"gte": start_dt.isoformat(), "lte": end_dt.isoformat()}}}
                ]
            }
        }
    }
    try:
        res = es.search(index=index_name, body=search_query, scroll='2m')
        scroll_id = res.get('_scroll_id')
        hits = res['hits']['hits']
        while hits:
            for h in hits:
                es_ids.add(str(h['_id']))
            res = es.scroll(scroll_id=scroll_id, scroll='2m')
            scroll_id = res.get('_scroll_id')
            hits = res['hits']['hits']
        if scroll_id:
            es.clear_scroll(scroll_id=scroll_id)
    except Exception as e:
        print("Error fetching ES _id values:", e)

    missing_in_csv = es_ids - csv_ids
    missing_in_es = csv_ids - es_ids
    common_ids = es_ids & csv_ids

    print(f"\nCount of ES docs in range: {len(es_ids)}")
    print(f"Count of CSV docs: {len(csv_ids)}")
    print(f"Count of common docs (by _id): {len(common_ids)}")
    print(f"Count missing in CSV: {len(missing_in_csv)}")
    print(f"Count missing in ES: {len(missing_in_es)}")
    print("Sample missing in CSV (up to 10):", list(missing_in_csv)[:10])
    print("Sample missing in ES (up to 10):", list(missing_in_es)[:10])

# Find 10 random docs in ES not present in CSV
import random
if es_count_with_fields and csv_count is not None and csv_count < es_count_with_fields:
    # Get IDs from CSV
    csv_ids = set()
    if '_id' in df.columns:
        csv_ids = set(df['_id'].astype(str))
    else:
        print("Warning: CSV does not have '_id' column, cannot compare IDs.")

    # Search ES for docs in range with non-empty ai_comment and severity
    search_query = {
        "size": 1000,
        "_source": ["_id", "first_seen_time", "ai_comment", "severity"],
        "query": {
            "bool": {
                "must": [
                    {"range": {"first_seen_time": {"gte": start_dt.isoformat(), "lte": end_dt.isoformat()}}},
                    {"exists": {"field": "ai_comment"}},
                    {"exists": {"field": "severity"}}
                ]
            }
        }
    }
    try:
        res = es.search(index=index_name, body=search_query)
        hits = res['hits']['hits']
        not_in_csv = [h for h in hits if str(h['_id']) not in csv_ids]
        print(f"\nRandom 10 docs in ES not in CSV:")
        for h in random.sample(not_in_csv, min(10, len(not_in_csv))):
            print({
                '_id': h['_id'],
                'first_seen_time': h['_source'].get('first_seen_time'),
                'ai_comment': h['_source'].get('ai_comment'),
                'severity': h['_source'].get('severity')
            })
    except Exception as e:
        print("Error searching for missing docs:", e)

print(f"Elasticsearch count for {index_name} from {start_dt} to {end_dt}: {es_count}")
print(f"Local CSV row count ({csv_path}): {csv_count}")
if es_count is not None and csv_count is not None:
    print(f"Difference: {es_count - csv_count}")

print(f"Elasticsearch count with non-empty ai_comment and severity: {es_count_with_fields}")
if es_count_with_fields is not None and csv_count is not None:
    print(f"Difference (with fields - CSV): {es_count_with_fields - csv_count}")

# Pick a sample from local CSV to compare with a missing ES doc

# Compare the document with _id 'rogi5ZoB6ySueK60fcFh' in both ES and CSV

# Compare a normal (present in both) and a missing (present in ES, missing in CSV) document by _id
normal_id = 'rogi5ZoB6ySueK60fcFh'  # present in both
missing_id = None
if '_id' in df.columns:
    # Find a missing _id (present in ES, missing in CSV)
    if 'missing_in_csv' in locals() and missing_in_csv:
        missing_id = list(missing_in_csv)[0]
    # Print normal document
    csv_match = df[df['_id'].astype(str) == normal_id]
    if not csv_match.empty:
        print(f"\nLocal CSV row with _id {normal_id}:")
        print(csv_match.iloc[0].to_dict())
    else:
        print(f"No row with _id {normal_id} found in local CSV.")
    # Fetch and print normal document from ES
    search_query = {
        "size": 1,
        "query": {
            "bool": {
                "must": [
                    {"term": {"_id": normal_id}}
                ]
            }
        }
    }
    try:
        res = es.search(index=index_name, body=search_query)
        hits = res['hits']['hits']
        if hits:
            print(f"\nES document with _id {normal_id}:")
            print(hits[0]['_source'])
        else:
            print(f"No document with _id {normal_id} found in ES.")
    except Exception as e:
        print(f"Error fetching document with _id {normal_id} from ES:", e)
    # Fetch and print missing document from ES
    if missing_id:
        search_query = {
            "size": 1,
            "query": {
                "bool": {
                    "must": [
                        {"term": {"_id": missing_id}}
                    ]
                }
            }
        }
        try:
            res = es.search(index=index_name, body=search_query)
            hits = res['hits']['hits']
            if hits:
                print(f"\nES document with missing _id {missing_id} (not in CSV):")
                print(hits[0]['_source'])
            else:
                print(f"No document with _id {missing_id} found in ES.")
        except Exception as e:
            print(f"Error fetching document with _id {missing_id} from ES:", e)
