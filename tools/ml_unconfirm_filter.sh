#!/bin/bash

last_two_days=$(date +"%Y-%m-%d" -d "-2 days")
#./tag_reset_web_ml_type.py webml -r "fake0pMBM6OrTtSf1ipe" 4
./tag_by_filter_false_alert.py webml -r "fake0pMBM6OrTtSf1ipe" 2
./tag_by_filter_attacked.py webml -r "fake0pMBM6OrTtSf1ipe" 1
echo "Yesterday's date is: $last_two_days"
./teams-chat-post-for-workflows.sh "webml false alert unconfirm filter!" "Result: done!"
