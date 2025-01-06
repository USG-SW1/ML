#!/usr/bin/env python3
#from datetime import datetime,timedelta
import os
import json
import pandas as pd
import sys
import datetime
import ollama

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
    prompt = (
        "Here is a http content. Analysis it and provide an attacked levels. "
        "normal: it's a normal content. low: It is an abnormal content, but "
        "it's not an attacked. medium: it's an attacked and just have a try. "
        "high: it's an attacked, suggest admin verify the behavior "
        "on http server. The answer format, Attack risk level: <normal or low or medium or high>. "
        "And simple comment. No need any code."
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
    #comment = 'This is a simulated AI response.'
    # 根據提示詞進行一些簡單的判斷

    return severity, comment

def process_json_files(input_directory, pass_path, pass_date):
    all_data = pd.DataFrame()
    print("-" + input_directory + "-")
    print("-" + pass_path + "-")
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
                        severity, comment = query_ai_qwen(feature_string)
                        df.at[index, 'severity'] = severity
                        df.at[index, 'ai_comment'] = None if comment == 'NULL' else comment

            df['sn'] = None if sn == 'NULL' else sn
            all_data = pd.concat([all_data, df], ignore_index=True)

    output_filename = f"{pass_date + '_' + 'webml'}.json"
    print(output_filename)
    all_data.to_json(pass_date + "_" + input_directory + ".json", orient='records', lines=True)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python normalize.py <webml|infection> <day> <path>")
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
