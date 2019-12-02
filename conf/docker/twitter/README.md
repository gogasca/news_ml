# Twitter listener

This Python script collects information from Twitter stream and
pushes Tweets to PubSub.

## Configuration

Install dependencies in `requirements.txt` file
Create a Twitter developer and get Authentication information [here](https://developer.twitter.com/)
 

### Google Cloud information

```
export PROJECT_ID=""
export PUBSUB_TOPIC=""
```

### Twitter authentication

Make sure you create the Twitter information in advanced.

```
export CONSUMER_KEY=""
export CONSUMER_SECRET=""
export ACCESS_TOKEN=""
export ACCESS_TOKEN_SECRET=""
```

### Build container

```
docker build -t twitter-listener . --no-cache
```

### Run container

Authenticate via Google Cloud

```
export GOOGLE_APPLICATION_CREDENTIALS="news-ml.json"
```

Run container

```
docker run -d --name="twitter-listener" --hostname="twitter-listener" 
    -e PROJECT_ID="" 
    -e PUBSUB_TOPIC="" 
    -e CONSUMER_KEY="" 
    -e CONSUMER_SECRET="" 
    -e ACCESS_TOKEN="" 
    -e ACCESS_TOKEN_SECRET="" 
    -v ~/.config:/root/.config twitter-listener
```

Verify tweets are being collected

```
docker logs -f twitter-listener
```