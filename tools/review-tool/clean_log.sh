#!/bin/bash
# Log cleaner: empties log files if last modified more than N days ago
# Usage: run this script weekly via cron or manually

# Define log files and their retention days (format: "path:days")
LOGS=(
  "/home/gsbu/ml/tools/ml_gen.log:7"
  "/home/gsbu/ml/tools/ml_gen_webml.log:7"
  "/home/gsbu/ml/tools/ml_gen_infection.log:7"
  "/filter_tool/debug.log:3"
  "/filter_tool/debug2.log:3"
  "/home/gsbu/ml/tools/review-tool/log/daily.log:7"
  "/home/gsbu/ml/tools/review-tool/log/post.log:7"
  "/home/gsbu/ml/tools/review-tool/log/sync.log:7"
  "./ml/tools/lottie/log/post.log:3"
  "./ml/tools/lottie/log/get_daily.log:3"
  "./ml/tools/review-tool/log/sync.log:3"
  "/home/gsbu/ml/tools/review-tool/filter_tool/run_log.txt:5"
)

clean_logs() {
  for entry in "${LOGS[@]}"; do
    log_file="${entry%%:*}"
    days="${entry##*:}"
    if [ -f "$log_file" ]; then
      # If the file was last modified more than (days-1) days ago, empty it
      if [ "$(find "$log_file" -mtime +$((days-1)) -print)" ]; then
        > "$log_file"
        echo "[$(date +"%Y-%m-%d %H:%M:%S")] Cleaned $log_file (older than $days days)"
      fi
    fi
  done
}

clean_logs

