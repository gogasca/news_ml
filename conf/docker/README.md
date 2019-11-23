# Docker infrastructure

## Requirements

   -Docker
   -Docker compose

Docker build commands

```
docker build -t news_ml/apid .
docker build -t news_ml/rabbitmq-server .
```

Start Docker container

```
git clone https://github.com/gogasca/news_ml.git /tmp/news/
docker run --name apid -itd -p 8081:8081 --env-file=/tmp/env_file.env -v /tmp/news/:/usr/local/src/news_ml/ news_ml/apid
docker ps -a
```

Docker Composer
 
```
docker-compose up -d
docker-compose stop
```