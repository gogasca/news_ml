# News ML

## Introduction

This Python script collects article and news information from News API.
Script collects information from fixed sources and if search is enabled
it will look into all news available in API for a specific time period.
We will also extract entities from News content via Google Cloud NLP.

## API

We created an API which is able to handle requests to collect News.
The API is composed of many modules:

 - Ngnix (Web server and main load balancer, terminates HTTPS)
 - Gunicorn (WSGI)
 - Flask (Python Web App)
 - RabbitMQ (Message Queue)
 - PostgreSQL (Relational Database)

## Example:

Request News from NEWS API:

```
curl -u AC64861838b417b555d1c8868705e4453f:YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o -H "Content-Type: application/json" -X POST -d '{ "provider": "news_api"}' http://0.0.0.0:8081/api/1.0/campaign
```

Request News from NEWS API using a Report:

```
curl -u AC64861838b417b555d1c8868705e4453f:YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o -H "Content-Type: application/json" -X POST -d '{ "provider": "news_api", "report": {"email": "noreply@google.com"}}' http://0.0.0.0:8080/api/1.0/campaign
``` 

Search for news including 'tensorflow' from NEWS API:

```
curl -u AC64861838b417b555d1c8868705e4453f:YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o -H "Content-Type: application/json" -X POST -d '{ "provider": "news_api", "query": "tensorflow, sagemaker, keras, petastorm"}' http://0.0.0.0:8080/api/1.0/campaign
``` 

## Starting API manually

```
gunicorn news_ml:api_app --bind 0.0.0.0:8080 --log-level=DEBUG -w 1
```

## RabbitMQ

```
/usr/local/sbin/rabbitmq-server
```

```
rabbitmqctl add_user news_ml news_ml
rabbitmqctl set_user_tags news_ml administrator
rabbitmqctl set_permissions -p / news_ml ".*" ".*" ".*"
```

## Celery

```
celery worker -n %h -P processes -c 15 --loglevel=DEBUG -Ofair
```

## Loadbalancer

Ngnix acts as our API loadbalancer.

```
    apt-get update
    locale-gen en_US en_US.UTF-8
    apt-get install -y nano vim wget dialog net-tools
    apt-get install -y nginx nginx-common nginx-extras
    vim /etc/nginx/sites-available/default
    vim nginx.conf 
```

## API performance

Use Apache ab tool to measure API performance.

```
ab -n 10 -A username:password https://<API_HOSTNAME>/api/1.0/status
```

## Architecture


```

REST API Server -> News collector -> PostgresSQL
                           RabbitMQ
                           Celery
```    

## Software 

Python based API:

 - Flask
 - Gunicorn
 - Celery 
 - RabbitMQ
 - PostgreSQL
 - Ngnix
 - Google Cloud NLP
 - Ngnix -> Gunicorn -> Flask -> RabbitMQ/Celery/PostgreSQL.
  
## Installation


```
apt-get install python build-essential  -y
apt-get install python-pip python-dev -y
apt-get install libpq-dev python-dev     # Required for psycopg2
apt-get install git -y
apt-get install python-pip
apt-get install libpq-dev
apt-get install rabbitmq-server
pip install --upgrade pip
```



```
pip install nltk
pip install coverage
pip install flower
```

```
python
>>> import nltk
>>> nltk.download("stopwords")
[nltk_data] Downloading package stopwords to /root/nltk_data...
[nltk_data]   Unzipping corpora/stopwords.zip.
True
>>> nltk.download('punkt')
[nltk_data] Downloading package punkt to /root/nltk_data...
[nltk_data]   Unzipping tokenizers/punkt.zip.
```
 
## RabbitMQ

```
/usr/local/sbin/rabbitmq-server
```

```
rabbitmqctl add_user news_ml news_ml
rabbitmqctl set_user_tags news_ml administrator
rabbitmqctl set_permissions -p / news_ml ".*" ".*" ".*"
```

## Celery

```
celery worker -n 1 -P processes -c 15 --loglevel=DEBUG -Ofair
```

## Authentication

```
export C_FORCE_ROOT="true"
export DBHOST=35.202.73.207
export DBPORT=5432
export DBUSERNAME="postgres"
export DBPASSWORD="postgres"
export DBNAME="news"

# NEWS API
export NEWS_API_KEY="1369bd55461b40e0987191f4ebe094d4"

# EMAIL
export MAILGUN_API_KEY="key-81261b57db24a12f91980e8195a07920"
# API
export API_USERNAME="AC64861838b417b555d1c8868705e4453f"
export API_PASSWORD="YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o"
export SECRET_FERNET_KEY="nIPstt3yGcdo16JiA-tPzdXZJZ-zPpB6eQk9rw-EP6Q="
```

## Create API Users

```
curl -H "Content-Type: application/json" 
     -X POST -d '{"username":"noreply@google.com", "password":"54321"}' 
     http://0.0.0.0:8080/api/1.0/users
```

## Token authentication

There is a good chance for Man in the middle attack while requesting data. 
In case of HTTP Basic Authentication, user credentials are sent along with every request which can be breached. 
So we use token based authentication, users request for a token and in the subsequent requests users use the obtained 
token to access data. This token lives for a short span of time, even if the attacker manages to get hold of the token, 
its only valid for short span of time. This way we can add one more layer of security to the REST API.

```
CREATE TABLE api_users
(
    id    serial primary key,
    username        VARCHAR(256) unique not null,
	password_hash   VARCHAR(256) not null,
    created   timestamp(6) WITH TIME ZONE
);
```

## Start services

```
    vim ~/.bashrc
    vim ~/.profile

    export C_FORCE_ROOT="true"

    mkdir -p /etc/supervisor/conf.d
    mkdir /var/log/supervisor/

    cp /usr/local/bin/supervisorctl /usr/bin/
    cp /usr/local/bin/supervisord /usr/bin/
    
```

Start supervisor after reboot:

```
    supervisord -c supervisord.conf
```

Use supervisorctl to check services status

### Upgrades

```
    cd /usr/local/src/news_ml
    git pull

    supervisorctl restart all
    supervisorctl status
```

## Database information

How to generate schema? Please read here:
https://pydigger.com/pypi/sqlacodegen

```
postgresql://username:password@hostname/database
```


## Troubleshooting

Problem: Supervisor not starting services.
Solution: Validate permissions for .sh scripts (Executable)

Problem: Supervisor not starting API service.
Solution: Check gunicorn ```gunicorn --log-file=- news_ml:api_app```

Problem: Supervisor not starting Celery service.
Solution: Validate RabbitMQ is started

Problem: Can't start services.
Solution: Install nltk dependencies from root.

Problem: Can't start services.
Solution: ```sudo -i```, verify ```.bashrc``` and ```.profile```. 

## Questions?

Bugs and issues can be reported at noreply@google.com

