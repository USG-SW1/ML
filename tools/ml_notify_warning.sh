#!/bin/bash

## Get search imjournal coredump count
count=$(./get_imjournal_dump_count.py)

#echo $count

## Check if count more then 300
if [[ $count -gt 300 ]]; then
        ./teams-chat-post-for-workflows.sh "Infection warning!" "imjournal coredump count: $count !"
else
        echo "Under control."
fi


#./teams-chat-post-for-workflows.sh "S3 download webml and infection" "Result: done!"
