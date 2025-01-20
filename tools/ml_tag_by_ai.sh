#!/bin/bash

# 迴圈迭代 3 次，每次印出前一天的日期
#for i in {23..63}; do 
#for i in {24..69}; do
#for i in {26..70}; do
#for i in {2..2}; do
for i in {2..2}; do
  # 取前n天的path and date	
  # remove last download temp data
  pass_date=$(date +"%Y-%m-%d" -d "-$i days")
  echo "Before $i date ：$pass_date"
  pass_path=$(echo "$pass_date" | sed 's/-/\//g')
  echo "new path ：$pass_path"
  #exit
  ./teams-chat-post-for-workflows.sh "AI analysis." "Result: going."
  ./tag_by_ai_comment.py webml $pass_date $i
  while [ ! -f "ai_start_scan" ]; do
    sleep 1
    ./tag_by_ai_comment.py webml $pass_date $i
  done 
  ./teams-chat-post-for-workflows.sh "AI analysis." "Result: done."
  
done

exit
