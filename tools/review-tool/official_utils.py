import json
import os

def get_record_status(selected_idx, df_sorted, log_path, post_log_path):
    # 取得該筆資料的 id 或 _id
    if '_id' in df_sorted.columns:
        record_id = str(df_sorted.loc[selected_idx, '_id'])
    elif 'id' in df_sorted.columns:
        record_id = str(df_sorted.loc[selected_idx, 'id'])
    else:
        record_id = str(selected_idx)

    # 判斷 reviewed 狀態
    review_val = str(df_sorted.loc[selected_idx, 'review']).strip().lower()
    reviewed = review_val in ["yes", "no"]

    posted = False
    # 檢查 post_log 檔案
    if os.path.exists(post_log_path):
        with open(post_log_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    key = str(data.get("_id") or data.get("id"))
                    if key == record_id:
                        posted = True
                        break
                except Exception:
                    continue

    if not reviewed:
        return "not_reviewed"
    elif reviewed and not posted:
        return "reviewed"
    elif reviewed and posted:
        return "posted"
    return "not_reviewed"
import html

def sanitize_plaintext(value):
    value = str(value)
    # 只做 HTML escape，不遮蔽、不截斷
    return html.escape(value)

def sanitize_df_all(df):
    df_copy = df.copy()
    for col in df_copy.columns:
        df_copy[col] = df_copy[col].apply(sanitize_plaintext)
    return df_copy
import pandas as pd

def apply_rule_mapping(df, rule_csv_path):
    import os
    if os.path.exists(rule_csv_path):
        rule_df = pd.read_csv(rule_csv_path)
        # Remove rows where rule is empty or NaN
        rule_df = rule_df[rule_df['rule'].notna() & (rule_df['rule'].astype(str).str.strip() != '')]

        if not rule_df.empty:
            # Create mapping: rule -> web_ml_type
            rule_map = dict(zip(
                rule_df['rule'].astype(str).str.strip(),
                rule_df['web_ml_type'].astype(str).str.strip()
            ))

            # Apply mapping to df
            for idx, row in df.iterrows():
                current_rule = str(row.get('rule', '')).strip()
                if current_rule and current_rule in rule_map:
                    df.at[idx, 'web_ml_type'] = rule_map[current_rule]
    return df

def get_record_status(selected_idx, df_sorted, log_path, post_log_path):
    if '_id' in df_sorted.columns:
        record_id = str(df_sorted.loc[selected_idx, '_id'])
    elif 'id' in df_sorted.columns:
        record_id = str(df_sorted.loc[selected_idx, 'id'])
    else:
        record_id = str(selected_idx)
    review_val = str(df_sorted.loc[selected_idx, 'review']).strip().lower()
    reviewed = review_val in ["yes", "no"]
    posted = False
    if os.path.exists(post_log_path):
        with open(post_log_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    key = str(data.get("_id") or data.get("id"))
                    if key == record_id:
                        posted = True
                        break
                except Exception:
                    continue
    if not reviewed:
        return "not_reviewed"
    elif reviewed and not posted:
        return "reviewed"
    elif reviewed and posted:
        return "posted"
    return "not_reviewed"

def count_reviewed_records(log_path):
    if not os.path.exists(log_path):
        return 0
    latest = {}
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get("action") == "save_review" and data.get("_id"):
                    key = str(data["_id"])
                    latest[key] = data.get("review")
            except Exception:
                continue
    return sum(1 for v in latest.values() if v == "yes")

def get_next_review_idx(log_path):
    max_idx = 0
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if "review_idx" in data:
                        try:
                            idx = int(data["review_idx"])
                            if idx > max_idx:
                                max_idx = idx
                        except Exception:
                            continue
                except Exception:
                    continue
    return str(max_idx + 1)

def find_latest_csv(directory="."):
    files = [f for f in os.listdir(directory) if f.endswith(".csv")]
    if not files:
        return None
    files = sorted(files, key=lambda f: os.path.getmtime(os.path.join(directory, f)), reverse=True)
    return files[0]

def get_latest_review_from_log(record_id, log_path):
    if not os.path.exists(log_path):
        return None, None
    with open(log_path, "r", encoding="utf-8") as f:
        for line in reversed(f.readlines()):
            try:
                data = json.loads(line)
                key = str(data.get("_id") or data.get("id"))
                if key == str(record_id) and data.get("action") == "save_review":
                    return data.get("web_ml_type", ""), data.get("review", "")
            except Exception:
                continue
    return None, None

def get_solved_per_severity(df, log_path, all_severity):
    id_to_sev = {}
    if '_id' in df.columns:
        for _, row in df.iterrows():
            id_to_sev[str(row['_id'])] = int(row['severity'])
    elif 'id' in df.columns:
        for _, row in df.iterrows():
            id_to_sev[str(row['id'])] = int(row['severity'])
    else:
        for idx, row in df.iterrows():
            id_to_sev[str(idx)] = int(row['severity'])
    solved_ids = set()
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    key = str(data.get("_id") or data.get("id"))
                    if data.get("action") == "save_review" and data.get("review") == "yes":
                        solved_ids.add(key)
                except Exception:
                    continue
    sev_total = df['severity'].value_counts().reindex(all_severity, fill_value=0)
    sev_solved = {}
    for _id in solved_ids:
        sev = id_to_sev.get(_id)
        if sev is not None:
            sev_solved[sev] = sev_solved.get(sev, 0) + 1
    return sev_total, sev_solved
import pandas as pd
import html
import os
import json
import configparser

def autofill_web_ml_type(df, rule_df):
    rule_map = dict(zip(rule_df['rule'].astype(str).str.strip(), rule_df['web_ml_type'].astype(str)))
    for idx, row in df.iterrows():
        if pd.isna(row['web_ml_type']) or str(row['web_ml_type']).lower() in ["nan", ""]:
            rule_val = str(row['rule']).strip()
            if rule_val and rule_val in rule_map:
                df.at[idx, 'web_ml_type'] = rule_map[rule_val]
    return df

def highlight_missing_webml(row):
    if (pd.isna(row['web_ml_type']) or str(row['web_ml_type']).lower() in ["nan", ""]) and str(row['review']).strip().lower() == "yes":
        return ['background-color: #FF6961'] * len(row)
    else:
        return [''] * len(row)

def apply_rule_mapping(df, rule_csv_path):
    if os.path.exists(rule_csv_path):
        rule_df = pd.read_csv(rule_csv_path)
        rule_df = rule_df[rule_df['rule'].notna() & (rule_df['rule'].astype(str).str.strip() != '')]
        if not rule_df.empty:
            rule_map = dict(zip(
                rule_df['rule'].astype(str).str.strip(),
                rule_df['web_ml_type'].astype(str).str.strip()
            ))
            for idx, row in df.iterrows():
                current_rule = str(row.get('rule', '')).strip()
                if current_rule and current_rule in rule_map:
                    df.at[idx, 'web_ml_type'] = rule_map[current_rule]
    return df

def is_normal_cookie(text):
    if "ajs_anonymous_id=" in text and "_streamlit_xsrf=" in text:
        return True
    return False

def sanitize_plaintext(value):
    value = str(value)
    return html.escape(value)

def sanitize_df_all(df):
    df_copy = df.copy()
    for col in df_copy.columns:
        df_copy[col] = df_copy[col].apply(sanitize_plaintext)
    return df_copy

def load_reviewer(config_path, config_section):
    config = configparser.ConfigParser()
    if os.path.exists(config_path):
        config.read(config_path, encoding="utf-8")
        if config_section in config and "name" in config[config_section]:
            return config[config_section]["name"]
    return ""

def save_reviewer(name, config_path, config_section):
    config = configparser.ConfigParser()
    if os.path.exists(config_path):
        config.read(config_path, encoding="utf-8")
    if config_section not in config:
        config[config_section] = {}
    config[config_section]["name"] = name.strip()
    with open(config_path, "w", encoding="utf-8") as f:
        config.write(f)

def log_reviewer_action(data, log_path):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

def get_existing_review_idx(record_id, log_path):
    if not os.path.exists(log_path):
        return None
    with open(log_path, "r", encoding="utf-8") as f:
        for line in reversed(f.readlines()):
            try:
                data = json.loads(line)
                if str(data.get("id")) == str(record_id) and "review_idx" in data:
                    return data["review_idx"]
            except Exception:
                continue
    return None
