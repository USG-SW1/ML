#!/bin/bash

# 迴圈迭代 3 次，每次印出前一天的日期
#for i in {23..63}; do
#for i in {24..69}; do
#for i in {26..70}; do
#for i in {2..2}; do
for i in {1..1}; do
  # 取前n天的path and date
  # remove last download temp data
  rm ./infection/*.json
  rm ./webml/*.json
  pass_date=$(date +"%Y-%m-%d" -d "-$i days")
  echo "Before $i date ：$pass_date"
  pass_path=$(echo "$pass_date" | sed 's/-/\//g')
  echo "new path ：$pass_path"
  #exit
  # download from S3
  mk_path="../raw-data/webml/$pass_path"
  mkdir -p $mk_path
  #echo "--"$mk_path"--"
  mk_path="../raw-data/infection/${pass_path}"
  mkdir -p $mk_path
  #mkdir -p "../raw_data/infection/"${pass_path}
  ./download_by_date.py "webml" $pass_path $pass_date
  ./download_by_date.py "infection" $pass_path $pass_date
  # normalize
  ./normalize.py "webml" $pass_path $pass_date
  ./normalize.py "infection" $pass_path $pass_date

  #patch to Elasticsearch
  ./patch_data_by_date.py "webml" $pass_path $pass_date
  ./patch_data_by_date.py "infection" $pass_path $pass_date
  #yesterday=$(date +"%Y-%m-%d" -d "-$i days")
  #echo "前 $i 天的日期是：yesterday"
done

exit
