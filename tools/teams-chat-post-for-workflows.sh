#!/bin/bash
# Help.
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  echo 'Usage: teams-chat-post.sh "<title>" "<message>"'
  exit 0
fi
# Webhook or Token.
WEBHOOK_URL="https://prod-05.southeastasia.logic.azure.com:443/workflows/b186cddc8e474b779ef14a6c39001ea0/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=KZejQdmvqtwLLFhEJ1sJ3_mI5r-pAjtRA8DhZXbWD24"
if [[ "${WEBHOOK_URL}" == "" ]]; then
  echo "No webhook_url specified."
  exit 1
fi

# Color.
COLOR="Default"
if [[ "${COLOR}" == "" ]]; then
  echo "No color specified."
  exit 1
fi

# Title .
TITLE=$1
if [[ "${TITLE}" == "" ]]; then
  echo "No title specified."
  exit 1
fi
shift


# Text.
TEXT=$1
if [[ "${TEXT}" == "" ]]; then
  echo "No text specified."
  exit 1
fi

# Escape char: `'`, `"`, `\` .
MESSAGE=$(echo ${TEXT} | sed "s/'/\'/g" | sed 's/"/\"/g; s/\\/\\\\/g')

# Adaptive Cards of TextBlock - https://adaptivecards.io/explorer/TextBlock.html
JSON="{
  \"type\": \"message\",
  \"attachments\": [
    {
      \"contentType\": \"application/vnd.microsoft.card.adaptive\",
      \"contentUrl\": null,
      \"content\": {
        \"$schema\": \"http://adaptivecards.io/schemas/adaptive-card.json\",
        \"type\": \"AdaptiveCard\",
        \"version\": \"1.2\",
        \"body\": [
          {
            \"type\":   \"TextBlock\",
            \"text\":   \"${TITLE}\",
            \"color\":  \"${COLOR}\",
            \"weight\": \"bolder\",
            \"size\":   \"large\",
            \"wrap\":   true
          },
          {
            \"type\":   \"TextBlock\",
            \"text\":   \"${MESSAGE}\",
            \"color\":  \"${COLOR}\",
            \"size\":   \"default\",
            \"wrap\":   true
          }
        ]
      }
    }
  ]
}"

# Post to Microsoft Teams via curl.
curl \
  --header "Content-Type: application/json" \
  --request POST \
  --data "${JSON}" \
  "${WEBHOOK_URL}"
