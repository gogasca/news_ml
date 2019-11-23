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
docker build -t news_ml/rabbitmq-server .
```

Start Docker container

```
git clone https://github.com/gogasca/news_ml.git /usr/local/src/
docker run --name apid -itd -p 8081:8081 --env-file=/usr/local/src/containers/secrets.env -v /usr/local/src/news_ml/:/usr/local/src/news_ml/ news_ml/apid
docker ps -a
```

Docker Composer
 
```
docker-compose up -d
docker-compose stop
```