#!/bin/bash

# Purpose:  Connects to API and using POST method request information for different data providers.
# Add Environment variables: API_USERNAME and API_PASSWORD

echo "Collecting news..."
echo "Reading ENV variables"
source ~root/.profile

# Log file information.
DATE=$(date '+%Y-%m-%d %H:%M:%S')
LOG='/var/log/news_ml_client.log'

EMAIL_NOTIFICATIONS='support@newsml.io'

# API Requests.
SOURCES='techcrunch'
NEWS_API='{ "provider": "news_api", "report": {"email": "'${EMAIL_NOTIFICATIONS}'"}}'
QUERY_NEWS='{ "provider": "news_api", "query": "tensorflow, sagemaker, keras, petastorm, kubeflow", "report": {"email": "'${EMAIL_NOTIFICATIONS}'"} }'
RANKER='{ "report": {"email": "'${EMAIL_NOTIFICATIONS}'"} }'
CLUSTER='{ "clusters": 8, "report": {"email": "'${EMAIL_NOTIFICATIONS}'"} }'

# API URL.
CAMPAIGN_URL="http://0.0.0.0:8081/api/1.0/campaign"
RANK_URL="http://0.0.0.0:8081/api/1.0/rank"
CLUSTER_URL="http://0.0.0.0:8081/api/1.0/clustering"

function echo_log() {
  echo $DATE" $1" >>$LOG
}

function collect_news() {
  # Generate random number
  local REQUEST_IDENTIFIER=$(head -200 /dev/urandom | cksum | awk '{print $1}')
  local JSON_REQUEST=$1
  echo_log "($REQUEST_IDENTIFIER) Collecting information...${JSON_REQUEST}"
  curl -k -u ${API_USERNAME}:${API_PASSWORD} -H "Content-Type: application/json" --data "${JSON_REQUEST}" ${CAMPAIGN_URL} -v >>$LOG
  echo_log "($REQUEST_IDENTIFIER) Sleeping..."
  sleep 60
  echo_log "($REQUEST_IDENTIFIER) Request completed"
}

function rank_news() {
  # Ranks existing news.
  local REQUEST_IDENTIFIER=$(head -200 /dev/urandom | cksum | awk '{print $1}')
  local JSON_REQUEST=$1
  echo_log "($REQUEST_IDENTIFIER) Ranking news information...${JSON_REQUEST}"
  curl -k -u ${API_USERNAME}:${API_PASSWORD} -H "Content-Type: application/json" --data "${JSON_REQUEST}" ${RANK_URL} -v >>$LOG
  echo_log "($REQUEST_IDENTIFIER) Sleeping..."
  sleep 60
  echo_log "($REQUEST_IDENTIFIER) Request completed"
}

function cluster_news() {
  # Ranks existing news.
  local REQUEST_IDENTIFIER=$(head -200 /dev/urandom | cksum | awk '{print $1}')
  local JSON_REQUEST=$1
  echo_log "($REQUEST_IDENTIFIER) Clustering news information...${JSON_REQUEST}"
  curl -k -u ${API_USERNAME}:${API_PASSWORD} -H "Content-Type: application/json" --data "${JSON_REQUEST}" ${CLUSTER_URL} -v >>$LOG
  echo_log "($REQUEST_IDENTIFIER) CURL Request sent"
  echo_log "($REQUEST_IDENTIFIER) Sleeping..."
  sleep 60
}

# Generate Daily report.
collect_news "$QUERY_NEWS"
# Rank news.
rank_news "$RANKER"
# Cluster news.
cluster_news "$CLUSTER"
