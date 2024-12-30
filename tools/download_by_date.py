#!/usr/bin/env python3

from datetime import datetime,timedelta
import subprocess
import os
import sys
import zipfile
import glob

url_infection = "s3://sds-zsdn-zyxel-com/infection/"
url_webml = "s3://sds-zsdn-zyxel-com/webml/"
# 取得當前日期和時間
# current_date = datetime.now()
current_date = datetime.now() - timedelta(days=1)

# 取得年、月、日
year = current_date.year
month = current_date.month
# 處理前一天的資料
day = current_date.day

# 印出結果
print("Year:", year)
print("Month:", month)
print("Day:", day)
#print("Day:", day)

def download_from_S3(ml_type, pass_path, pass_date):
    print("Downloading... please wait!")
    print(ml_type, pass_path, pass_date)
    #mkdir_webml_path_day = f"mkdir -p /home/gsbu/ml/raw-data/webml{'/' + str(year) + '/' + str(month) + '/' + str(day)}"
    #os.system(mkdir_webml_path_day)
    #mkdir_infection_path_day = f"mkdir -p /home/gsbu/ml/raw-data/infection{'/' + str(year) + '/' + str(month) + '/' + str(day)}"
    #os.system(mkdir_infection_path_day)
    #print(mkdir_infection_path_day)
    #os._exit(0)
    # Output紀錄檔
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"{pass_date}_output.log"
    #os._exit(0)
    with open(output_filename, "w") as output_file:
       #result = subprocess.run(["echo", str(year)], stdout=output_file, text=True)
       ml_path = f"./{ml_type}/"
       if ml_type == "infection":
           result = subprocess.run(["aws", "s3", "sync", url_infection + pass_path, ml_path], stdout=output_file, text=True)
       if ml_type == "webml":
           result = subprocess.run(["aws", "s3", "sync", url_webml + pass_path, ml_path], stdout=output_file, text=True)
           print(url_webml + pass_date, ml_path)
    # 壓縮後的 ZIP 檔案名稱
    #zip_filename = 'infection.zip'
    zip_filename = f"{pass_date}_{ml_type}.zip"
    # 搜尋 ./infection/ 目錄及其子目錄中的所有 .json 檔案
    json_files = glob.glob('/home/gsbu/ml/tools/' + ml_type + '/*.json', recursive=True)
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍歷所有找到的 .json 檔案
        os.chdir("/home/gsbu/ml/tools/" + ml_type)
        for file in json_files:
            # 使用相對路徑保留原始資料夾結構
            arcname = os.path.relpath(file, './')
            zipf.write(file, arcname=arcname)

    os.chdir("/home/gsbu/ml/tools")
    unzip_path_day = f"unzip {zip_filename} -d /home/gsbu/ml/raw-data/{ml_type}/{pass_path}"
    os.system(unzip_path_day)
    print("Output has been written to " + output_filename)

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
    download_from_S3(ml_type, pass_path, pass_date)
