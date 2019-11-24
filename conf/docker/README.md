# Docker infrastructure

## Requirements

   -Docker
   -Docker compose

Create a Cloud Compute Engine Instance

```
apt-get update
apt-get install docker.io -y

mkdir -p /usr/local/src/containers/apid/volumes/log/
git clone https://github.com/gogasca/news_ml.git //usr/local/src/
```

Docker build commands

```
docker build -t news_ml/apid .
docker build -t news_ml/loadbalancer .
```

Start API Docker container

```
git clone https://github.com/gogasca/news_ml.git /usr/local/src/
```

Start Docker containers
```
docker network create newsml_network # For intra-Docker communication
docker run -d --name="rabbitmq" --hostname="rabbitmq" --network=newsml_network -e RABBITMQ_ERLANG_COOKIE="secret string" -e RABBITMQ_NODENAME="rabbitmq" -e RABBITMQ_DEFAULT_USER=news_ml -e RABBITMQ_DEFAULT_PASS=news_ml --publish="4369:4369" --publish="5671:5671" --publish="5672:5672" --publish="15671:15671" --publish="15672:15672" --publish="25672:25672" rabbitmq:3-management 
docker run -d --name "apid" --hostname="apid1" --network=newsml_network -itd -p 8081:8081 --env-file=/usr/local/src/containers/secrets.env -v /usr/local/src/news_ml/:/usr/local/src/news_ml/ -v /usr/local/src/news_ml/log/:/usr/local/src/news_ml/log/ news_ml/apid
```

Docker Composer (Optional)
 
```
docker-compose up -d
docker-compose stop
```

RabbitMQ Docker container

```

```