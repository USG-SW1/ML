#!/bin/bash

LOG_FILE="/home/gsbu/ml/tools/ml_gen_infection.log"

ts() { date +"%Y-%m-%d %H:%M:%S"; }

echo "[$(ts)] ml_gen_json_by_date.sh started" >> "$LOG_FILE"

# 迴圈迭代 3 次，每次印出前一天的日期
#for i in {23..63}; do
#for i in {24..69}; do
#for i in {26..70}; do
#for i in {6..6}; do
#for i in {1..1}; do
for i in {2..2}; do
  echo "[$(ts)] loop start: i=$i" >> "$LOG_FILE"

  rm -rf ./infection/ && mkdir ./infection/
  #rm -rf ./webml/ && mkdir ./webml/

  pass_date=$(date +"%Y-%m-%d" -d "-$i days")
  echo "[$(ts)] Before $i date: $pass_date" >> "$LOG_FILE"
  pass_path=$(echo "$pass_date" | sed 's/-/\//g')
  echo "[$(ts)] new path: $pass_path" >> "$LOG_FILE"

  #mk_path="../raw-data/webml/$pass_path"
  #mkdir -p "$mk_path"
  mk_path="../raw-data/infection/${pass_path}"
  mkdir -p "$mk_path"

  #echo "[$(ts)] download webml" >> "$LOG_FILE"
  #./download_by_date.py "webml" "$pass_path" "$pass_date" >> "$LOG_FILE" 2>&1

  echo "[$(ts)] download infection" >> "$LOG_FILE"
  ./download_by_date.py "infection" "$pass_path" "$pass_date" >> "$LOG_FILE" 2>&1

  #echo "[$(ts)] normalize webml" >> "$LOG_FILE"
  #./normalize.py "webml" "$pass_path" "$pass_date" >> "$LOG_FILE" 2>&1

  echo "[$(ts)] normalize infection" >> "$LOG_FILE"
  ./normalize.py "infection" "$pass_path" "$pass_date" >> "$LOG_FILE" 2>&1

  #echo "[$(ts)] patch webml" >> "$LOG_FILE"
  #./patch_data_by_date.py "webml" "$pass_path" "$pass_date" >> "$LOG_FILE" 2>&1

  echo "[$(ts)] patch infection" >> "$LOG_FILE"
  ./patch_data_by_date.py "infection" "$pass_path" "$pass_date" >> "$LOG_FILE" 2>&1

  rm -rf ./infection/ && mkdir ./infection/
  #rm -rf ./webml/ && mkdir ./webml/

  echo "[$(ts)] loop end: i=$i" >> "$LOG_FILE"
done

echo "[$(ts)] ml_gen_json_by_date.sh finished" >> "$LOG_FILE"
exit
