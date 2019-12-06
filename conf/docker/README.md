# Docker infrastructure

## Requirements

   - Docker
   - Docker compose

Create a Cloud Compute Engine Instance

```
apt-get update
apt-get install docker.io -y

mkdir -p /usr/local/src/containers/apid/volumes/log/apid1 (Optional)
git clone https://github.com/gogasca/news_ml.git /usr/local/src/
```

## Docker build commands

Build API container

```
cd /usr/local/src/news_ml/conf/docker/apid
docker build -t news_ml/apid .
```

Build Load balancer container

```
cd /usr/local/src/news_ml/conf/docker/loadbalancer
docker build -t news_ml/loadbalancer .
```

Create a network for communication between containers

```
docker network create newsml_network # For intra-Docker communication
```


## Start Docker containers

Start API
```
docker run -d --name "apid1" --hostname="apid1" --network=newsml_network -itd --env-file=/usr/local/src/containers/secrets.env -v /usr/local/src/news_ml/:/usr/local/src/news_ml/ -v /usr/local/src/news_ml/log/:/usr/local/src/news_ml/log/ news_ml/apid
```
Start RabbitMQ

```
docker run -d --name="rabbitmq" --hostname="rabbitmq" --network=newsml_network -e RABBITMQ_ERLANG_COOKIE="secret string" -e RABBITMQ_NODENAME="rabbitmq" -e RABBITMQ_DEFAULT_USER=news_ml -e RABBITMQ_DEFAULT_PASS=news_ml --publish="4369:4369" --publish="5671:5671" --publish="5672:5672" --publish="15671:15671" --publish="15672:15672" --publish="25672:25672" rabbitmq:3-management 
```

Start Load Balancer

```
docker run -d --name="loadbalancer" --hostname="loadbalancer" --network=newsml_network --publish="8443:8443"  news_ml/loadbalancer
```

SQL proxy

```
docker run -d \
  --name="cloud_sql_proxy" \
  --network=newsml_network \
  -v /usr/local/src/news_ml/conf/credentials/key.json:/config \
  -p 127.0.0.1:5432:5432 \
  gcr.io/cloudsql-docker/gce-proxy:1.16 /cloud_sql_proxy \
  -instances=<INSTANCE_CONNECTION_NAME>=tcp:0.0.0.0:5432 -credential_file=/config
```
Reference [here](https://cloud.google.com/sql/docs/mysql/connect-docker)

Validate connection:

```
docker logs -f <container name>
docker ps -a
```

Check you get a valid response
```
curl -k -u AC64861838b417b555d1c8868705e4453f:YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o -H "Content-Type: application/json" https://0.0.0.0:8443/api/1.0/ 
```

Open firewall in Compute Engine instance

Docker Composer (Optional)
 
```
docker-compose up -d
docker-compose stop
```