#!/bin/bash

last_two_days=$(date +"%Y-%m-%d" -d "-2 days")
./get_webml_attacked_unconfirm_reindex.py webml $last_two_days
echo "Yesterday's date is: $last_two_days"
./teams-chat-post-for-workflows.sh "webml attacked unconfirm! Reindex for RD review." "Result: new index unconfirm_webml_$last_two_days done!"
