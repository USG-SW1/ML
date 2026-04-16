import sys
import datetime
import pandas as pd
from elasticsearch import Elasticsearch
import configparser
import os
import re

es_host = "http://localhost:9200"
script_dir = os.path.dirname(os.path.abspath(__file__))  # /lottie
config_path = os.path.join(script_dir, "reviewer.config")
config_section = "export"

def make_export_id(index_name, target_day, days_num, csv_filename, export_dir="."):
    # 產生 base id
    base = f"{index_name}_{target_day}_{days_num}"
    base = re.sub(r'[^\w\-]', '_', base)  # 避免特殊字元
    # 檢查現有檔案，決定版本號
    pattern = re.compile(rf"^{re.escape(base)}(_(\d+))?$")
    existing = [f for f in os.listdir(export_dir) if pattern.match(os.path.splitext(f)[0])]
    if not existing:
        return base
    # 找最大版本號
    max_ver = 0
    for f in existing:
        m = pattern.match(os.path.splitext(f)[0])
        if m and m.group(2):
            max_ver = max(max_ver, int(m.group(2)))
        elif m:
            max_ver = max(max_ver, 0)
    return f"{base}_{max_ver+1}"

def save_to_reviewer_config(index_name, target_day, days_num, csv_filename, export_id):
    config = configparser.ConfigParser()
    if os.path.exists(config_path):
        config.read(config_path, encoding="utf-8")
    if config_section not in config:
        config[config_section] = {}
    config[config_section]["index_name"] = index_name
    # config[config_section]["target_day"] = target_day
    config[config_section]["days_num"] = days_num
    # config[config_section]["csv_filename"] = csv_filename
    # config[config_section]["export_id"] = export_id
    with open(config_path, "w", encoding="utf-8") as f:
        config.write(f)

def export_elasticsearch_to_csv(index_name, target_day, days_num, csv_filename):
    es = Elasticsearch([es_host])

    # Always use the provided csv_filename in the log directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # If csv_filename includes a directory, use as-is; else prepend 'log/'
    if os.path.dirname(csv_filename):
        csv_fullpath = os.path.join(script_dir, csv_filename)
        export_dir = os.path.dirname(csv_fullpath)
    else:
        export_dir = os.path.join(script_dir, "log")
        os.makedirs(export_dir, exist_ok=True)
        csv_fullpath = os.path.join(export_dir, csv_filename)
    os.makedirs(export_dir, exist_ok=True)
    log_basename = f"{os.path.splitext(os.path.basename(csv_filename))[0]}.log"
    log_fullpath = os.path.join(export_dir, log_basename)

    # Use a static export_id for logging (can be the base filename)
    export_id = os.path.splitext(csv_filename)[0]

    # 儲存參數到 reviewer.config
    save_to_reviewer_config(index_name, target_day, days_num, csv_filename, export_id)

    # 計算查詢的日期範圍
    start_date = datetime.datetime.fromisoformat(target_day)
    if days_num.startswith('+'):
        days_num_int = int(days_num[1:])
        end_date = start_date + datetime.timedelta(days=days_num_int)
    elif days_num.startswith('-'):
        days_num_int = int(days_num[1:])
        end_date = start_date
        start_date = start_date - datetime.timedelta(days=days_num_int)
    else:
        days_num_int = int(days_num)
        end_date = start_date + datetime.timedelta(days=days_num_int)

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

    response = es.search(index=index_name, body=query, scroll='20m')
    scroll_id = response['_scroll_id']
    hits = response['hits']['hits']
    all_docs = []

    while len(hits) > 0:
        for hit in hits:
            doc = hit['_source']
            doc['_id'] = hit['_id']
            all_docs.append(doc)
        response = es.scroll(scroll_id=scroll_id, scroll='20m')
        scroll_id = response['_scroll_id']
        hits = response['hits']['hits']

    es.clear_scroll(scroll_id=scroll_id)

    print(f"[DEBUG] Total documents fetched from ES: {len(all_docs)}")
    print(f"[DEBUG] First 10 _id values fetched: {[doc['_id'] for doc in all_docs[:10]]}")

    # If CSV exists, compare content and only download new or changed rows
    new_docs = []
    updated_docs = []
    unchanged_docs = []
    existing_count = 0
    if os.path.exists(csv_fullpath):
        try:
            existing_df = pd.read_csv(csv_fullpath)
            if '_id' in existing_df.columns:
                existing_count = len(existing_df)
                existing_map = {str(row['_id']): row for _, row in existing_df.iterrows()}
                for doc in all_docs:
                    doc_id = str(doc['_id'])
                    if doc_id in existing_map:
                        # Compare all fields except local_id, export_id
                        compare_fields = [k for k in doc.keys() if k not in ('local_id', 'export_id')]
                        is_same = True
                        for k in compare_fields:
                            v1 = doc.get(k)
                            v2 = existing_map[doc_id].get(k)
                            if pd.isna(v1) and pd.isna(v2):
                                continue
                            if v1 != v2:
                                is_same = False
                                break
                        if is_same:
                            unchanged_docs.append(doc)
                        else:
                            updated_docs.append(doc)
                    else:
                        new_docs.append(doc)
            else:
                new_docs = all_docs
        except Exception as e:
            print(f"[DEBUG] Could not read existing CSV for deduplication: {e}")
            new_docs = all_docs
    else:
        new_docs = all_docs

    print(f"[SUMMARY] Existing CSV rows before: {existing_count}")
    print(f"[SUMMARY] New docs to download: {len(new_docs)}")
    print(f"[SUMMARY] Updated docs to download: {len(updated_docs)}")
    print(f"[SUMMARY] Unchanged docs (already in CSV): {len(unchanged_docs)}")
    print(f"[SUMMARY] Total documents fetched from ES: {len(all_docs)}")

    # Prepare DataFrame for new and updated docs
    df = pd.DataFrame(new_docs + updated_docs)
    if not df.empty:
        # 過濾掉 review == "yes" 的資料
        if 'review' in df.columns:
            df = df[df['review'] != 'yes']
        df.insert(0, 'local_id', range(existing_count + 1, existing_count + 1 + len(df)))
        df['export_id'] = export_id
        # Append to CSV (always append to the specified file)
        df.to_csv(csv_fullpath, mode='a', header=not os.path.exists(csv_fullpath), index=False, encoding='utf-8-sig')
        print(f"已匯出 {len(df)} 筆新/更新資料到 {csv_fullpath}，export_id: {export_id}")
        # 也寫 log
        with open(log_fullpath, "a", encoding="utf-8") as logf:
            logf.write(f"export_id: {export_id}, count: {len(df)}, file: {csv_fullpath}, time: {datetime.datetime.now().isoformat()}\n")
        # Debug: print last 5 rows of the CSV to confirm append
        try:
            result_df = pd.read_csv(csv_fullpath)
            print("[DEBUG] Last 5 rows of CSV after export:")
            print(result_df.tail(5))
        except Exception as e:
            print(f"[DEBUG] Could not read CSV after export: {e}")
    else:
        print("[DEBUG] No new or updated data to write after deduplication.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python export_es_to_csv.py <index_name> <day> <+d|-d> <csv_filename>")
        sys.exit(1)
    _, index_name, target_day, days_num, csv_filename = sys.argv
    export_elasticsearch_to_csv(index_name, target_day, days_num, csv_filename)
