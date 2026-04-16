#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <day>"
    exit 1
fi

DAY=$1

# Change to the correct directory
cd /home/gsbu/ml/tools/review-tool/filter_tool || { echo "Failed to cd to /home/gsbu/ml/tools/review-tool/filter_tool"; exit 1; }

# Start timing
START=$(date +%s)

# Step 1: Run filter_json_matches.py scan_es on Elasticsearch
echo "Running filter_json_matches.py scan_es..."
echo "DAY=$DAY"
STEP1_START=$(date +%s)
OUTPUT=$(python3 filter_fix.py scan_es webml "$DAY" 1)
STEP1_END=$(date +%s)
STEP1_TIME=$((STEP1_END - STEP1_START))
MATCHES=$(echo "$OUTPUT" | grep "Total matches:" | sed 's/Total matches: //')
PROCESSED_ENTRIES=$(echo "$OUTPUT" | grep "Entries processed (after filters):" | sed 's/Entries processed (after filters): //')
TOTAL_ITEMS=$(echo "$OUTPUT" | grep "Total items from ES:" | sed 's/Total items from ES: //')
BLACKLIST_MATCHES=$(echo "$OUTPUT" | grep "Blacklist:" | sed 's/Blacklist: //' | sed 's/ matches//')
WHITELIST_GA_MATCHES=$(echo "$OUTPUT" | grep "Whitelist (_ga):" | sed 's/Whitelist (_ga): //' | sed 's/ matches//')
TEMP_FILE="/home/gsbu/ml/tools/review-tool/filter_tool/log/matches_${DAY}_1.json"
echo "TEMP_FILE='$TEMP_FILE'"
echo "TEMP_FILE='$TEMP_FILE'"
echo "$OUTPUT"
echo "Step 1 completed in $STEP1_TIME seconds. Total items: $TOTAL_ITEMS, processed $PROCESSED_ENTRIES entries, found $MATCHES matches ($BLACKLIST_MATCHES from blacklist, $WHITELIST_GA_MATCHES from whitelist _ga)."


# Step 2: Run ai_malicious.py with the temp file (with timeout)
echo "Running ai_malicious.py..."
STEP2_START=$(date +%s)
OUTPUT2=$(timeout 3600 python3 ai_debug.py "$TEMP_FILE")
STEP2_END=$(date +%s)
STEP2_TIME=$((STEP2_END - STEP2_START))
MATCHES_AI=$(echo "$OUTPUT2" | grep "Loaded" | sed 's/Loaded //' | sed 's/ matches for analysis//')
echo "$OUTPUT2"
echo "Step 2 completed in $STEP2_TIME seconds. Analyzed $MATCHES_AI matches."

# Step 3: Run update.py with the temp file and index
echo "Running update.py..."
STEP3_START=$(date +%s)
OUTPUT3=$(python3 update_v2.py "$TEMP_FILE" webml)
STEP3_END=$(date +%s)
STEP3_TIME=$((STEP3_END - STEP3_START))
echo "$OUTPUT3"
echo "Step 3 completed in $STEP3_TIME seconds."

# Step 4: Send Teams notification
echo "Sending Teams notification..."
STEP4_START=$(date +%s)
python3 filter_teams.py "$TEMP_FILE"
STEP4_END=$(date +%s)
STEP4_TIME=$((STEP4_END - STEP4_START))
echo "Step 4 completed in $STEP4_TIME seconds."

# End timing
END=$(date +%s)
TOTAL_TIME=$((END - START))

echo ""
echo "=== Time Consumption Statistics ==="
echo "Step 1 (Filter scan): $STEP1_TIME seconds - Total items: $TOTAL_ITEMS, processed $PROCESSED_ENTRIES, found $MATCHES matches ($BLACKLIST_MATCHES from blacklist, $WHITELIST_GA_MATCHES from whitelist _ga)"
echo "Step 2 (AI Analysis): $STEP2_TIME seconds - Analyzed $MATCHES_AI matches"
echo "Step 3 (Update): $STEP3_TIME seconds"
echo "Step 4 (Teams Notification): $STEP4_TIME seconds"
echo "Total time: $TOTAL_TIME seconds"
