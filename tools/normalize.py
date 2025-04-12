#!/usr/bin/env python3
#from datetime import datetime,timedelta
import os
import json
import pandas as pd
import sys
import datetime
import ollama


ioutput_log = "output.log"

def epoch_to_iso8601(epoch_string):
  """將epoch字串轉換為ISO 8601格式

  Args:
    epoch_string: epoch值的字串

  Returns:
    str: ISO 8601格式的日期時間字串
  """

  # 將字串轉換為整數
  epoch_int = int(epoch_string)

  # 將epoch值轉換為datetime物件
  dt = datetime.datetime.fromtimestamp(epoch_int)

  # 將datetime物件格式化為ISO 8601格式
  iso_time = dt.isoformat()
  #print("iso: " + iso_time)
  return iso_time

def custom_function(x):
    str_epoch = f"{epoch_to_iso8601(x)}"
    # 在這裡可以進行更複雜的計算或判斷
    return str_epoch

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
        "Output format as following, Attack risk level: <level> then return print Detail comment. DONOT print code."
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
        "And provide Detail comment. (DONOT print safe rule of 1~8) "
    )
    return "", ""

    #p= f"prompt + '\n' + features"
    #print(prompt + '\n' + features)
    #os.exit()
    stream = ollama.chat(
        model='qwen2.5-coder:32b',
        messages=[{'role': 'user', 'content': prompt + '\n' + features}],
        options={"temperature":0, "num_ctx":4096},
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
    #print(comment)
    #print(severity)
    # 模擬AI的回應
    #comment = 'This is a simulated AI response.'
    # 根據提示詞進行一些簡單的判斷

    return severity, comment

def process_json_files(input_directory, pass_path, pass_date):
    all_data = pd.DataFrame()
    print("index: -" + input_directory + "-")
    print("raw path: -" + pass_path + "-")
    output_file = "../raw-data/" + input_directory + "/" + pass_path

    for filename in os.listdir("../raw-data/" + input_directory + "/" + pass_path):
        print(filename)
        if filename[0] != 'S' or '-' not in filename:
            sn = 'NULL'
        else:
            sn = filename.split('-')[0]
        print("sn: " + sn)

        if filename.endswith('.json') and filename != os.path.basename(output_file):
            filepath = os.path.join(output_file, filename)
            with open(filepath) as f:
                d = json.load(f)

            # 讀取 JSON 資料並轉換為 DataFrame
            df = pd.json_normalize(d, ["payload", "data"], "category")

            # 將 firmware, model, mode 資料寫入 DataFrame 中
            df['firmware'] = d['payload']['device']['firmware']
            df['model'] = d['payload']['device']['model']
            df['mode'] = d['payload']['device']['mode']

            if input_directory == 'webml':
                # 將 feature_raw 資料依據 "=" 拆分成不同欄位並新增至 DataFrame 中
                df['first_seen_time'] = df['first_seen_time'].astype(str)
                df['first_seen_time'] = df['first_seen_time'].apply(custom_function)

                for index, row in df.iterrows():
                    features = row['feature_raw'].split('\n')
                    for feature in features:
                        if '=' in feature:
                            key, value = feature.split('=', 1)
                            df.at[index, key] = value

                for index, row in df.iterrows():
                    features = row['feature_raw'].split('\n\n', 1)
                    if len(features) > 1:
                        feature_string = features[1]
                        print("\n\n" + "sn: " + sn)
                        severity, comment = query_ai_qwen(feature_string)
                        df.at[index, 'severity'] = None if severity  == 'NULL' else severity
                        df.at[index, 'ai_comment'] = None if comment == 'NULL' else comment

            if input_directory in ["infection", "beta-infection"]:
                firmware_version = df['firmware']
                if firmware_version.any() and firmware_version.str.contains(r'\(').any():
                    major_version = firmware_version.str.extract(r'(\d\.\d{2})')[0]
                    df['major_version'] = major_version
                if df['target'].str.endswith('.core.zip').any():
                    df['daemon'] = df['target'].apply(lambda x: x.split('-')[-1].replace('.core.zip', '') if x.endswith('.core.zip') else None)
                    #if df['daemon'].notna().any():
                    #    print(df['target'].values)

            df['sn'] = None if sn == 'NULL' else sn
            all_data = pd.concat([all_data, df], ignore_index=True)

    output_filename = f"{pass_date + '_' + 'webml'}.json"
    print(output_filename)
    all_data.to_json(pass_date + "_" + input_directory + ".json", orient='records', lines=True)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: normalize.py <webml|infection> <path> <day> \nex. webml 2025/01/24 2025-01-24")
        sys.exit(1)

    ml_type = sys.argv[1]
    pass_path = sys.argv[2]
    pass_date = sys.argv[3]
    #output_file = sys.argv[2]
    print("type : " + ml_type)
    print("path : " + pass_path)
    print("date : " + pass_date)
    #sys.exit()
    #process_json_files(input_directory, output_file)
    process_json_files(ml_type, pass_path, pass_date)
