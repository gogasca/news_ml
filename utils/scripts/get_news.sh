#!/bin/bash

# Purpose:  Connects to API and using POST method request information for different data providers.


echo "Collecting news..."
echo "Reading ENV variables"
source ~root/.profile

# Log file information.
DATE=`date '+%Y-%m-%d %H:%M:%S'`
LOG='/var/log/news_ml_client.log'

EMAIL_NOTIFICATIONS='gogasca@google.com'

# API Requests.
SOURCES='techcrunch'
NEWS_API='{ "provider": "news_api", "report": {"email": "'${EMAIL_NOTIFICATIONS}'"}}'
QUERY_NEWS='{ "provider": "news_api", "query": "tensorflow, sagemaker, keras, petastorm, kubeflow"}'
RANKER='{ "report": {"email": "'${EMAIL_NOTIFICATIONS}'"} }'

# API URL.
CAMPAIGN_URL="http://0.0.0.0:8081/api/1.0/campaign"
RANK_URL="http://0.0.0.0:8081/api/1.0/rank"

function echo_log {
    echo $DATE" $1" >> $LOG
}

function collect_news () {
    # Generate random number
    local REQUEST_IDENTIFIER=`head -200 /dev/urandom | cksum | awk '{print $1}'`
    local JSON_REQUEST=$1
    echo_log "($REQUEST_IDENTIFIER) Collecting information...${JSON_REQUEST}"
    curl -k -u ${API_USERNAME}:${API_PASSWORD} -H "Content-Type: application/json" --data "${JSON_REQUEST}" ${CAMPAIGN_URL} -v >> $LOG
    echo_log "($REQUEST_IDENTIFIER) Sleeping..."
    sleep 60;
    echo_log "($REQUEST_IDENTIFIER) Request completed"
}

function rank_news () {
    # Ranks existing news.
    local REQUEST_IDENTIFIER=`head -200 /dev/urandom | cksum | awk '{print $1}'`
    local JSON_REQUEST=$1
    echo_log "($REQUEST_IDENTIFIER) Ranking news information...${JSON_REQUEST}"
    curl -k -u ${API_USERNAME}:${API_PASSWORD} -H "Content-Type: application/json" --data "${JSON_REQUEST}" ${RANK_URL} -v >> $LOG
    echo_log "($REQUEST_IDENTIFIER) Sleeping..."
    sleep 60;
    echo_log "($REQUEST_IDENTIFIER) Request completed"
}


# Generate Daily report.
collect_news "$QUERY_NEWS"
# Rank news.
# rank_news "$RANKER"