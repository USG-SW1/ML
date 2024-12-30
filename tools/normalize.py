#!/usr/bin/env python3
#from datetime import datetime,timedelta
import os
import json
import pandas as pd
import sys
import datetime

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

def process_json_files(input_directory, pass_path, pass_date):
    all_data = pd.DataFrame()
    print("-"+input_directory+"-")
    print("-"+pass_path+"-")
    output_file = "../raw-data/" + input_directory + "/" + pass_path
    #for filename in os.listdir("../raw_data/" + pass_path):
    for filename in os.listdir("../raw-data/" + input_directory + "/" + pass_path):
        print(filename)
        #sys.exit(1)
        #if filename.endswith('.json'):
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
                  #for index2, row2 in df.iterrows():
                  #df['first_seen_time'] = df['first_seen_time'].astype(str)
                  #str_epoch = f"{df['first_seen_time']}"
                  #print("aaaa " + str_epoch)
                  #print("bbb " + df['first_seen_time'])
                  #df['first_seen_time'] = epoch_to_iso8601(str_epoch)
                  #first_seen_times = row['first_seen_time'].split('\n')
                  #print(first_seen_times)
              #for index, row in df.iterrows():
                  #first_seen_times = row['first_seen_time'].split('\n')
                  #print(df[index,'first_seen_time'])
                  #first_seen_times = row['first_seen_time']
                  #for first_seen_time in first_seen_times:
                  #    print("value: " + first_seen_time)
                  #    print("ccc")

                  #print("aaaa")
                  #print(df['first_seen_time'])
                  #str_epoch = f"{df['first_seen_time']}"
                  #print(epoch_to_iso8601(str_epoch))
                  #df['first_seen_time'] = df['first_seen_time'].astype(str)
                  #df['first_seen_time'] = str_epoch
                  #df['first_seen_time'] = "1970-01-02T03:11:40"
                  #print(df['first_seen_time'])
                  #epoch_to_iso8601(172000)

            # 將當前 DataFrame 合併到 all_data 中
            all_data = pd.concat([all_data, df], ignore_index=True)


    # 取得當前日期和時間
    # current_date = datetime.now()
    #current_date = datetime.now() - timedelta(days=1)

    # 取得年、月、日
    #year = current_date.year
    #month = current_date.month
    # 處理前一天資料
    #day = current_date.day
    #if day < 10:
    #    output_filename = f"{str(year) + '-' + str(month) + '-' + '0' + str(day) + '_' + 'webml'}.json"
    #else:
    #    output_filename = f"{str(year) + '-' + str(month) + '-' + str(day) + '_' + 'webml'}.json"

    output_filename = f"{pass_date + '_' + 'webml'}.json"
    print(output_filename)
    # 將合併後的 DataFrame 寫入 output.json 中
    #all_data.to_json(output_filename, orient='records', lines=True)
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
