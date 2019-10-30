# News ML

## Introduction

This Python application collects article and news information from News 
API. App collects information from fixed sources and if search is enabled
it will look into all news available in API for a specific time period.
We will also extract entities from News content via Google Cloud NLP.

## Quick start

You can use sample Python script (mini/app.py) 
which collects News and stores them into a CSV file using News API Key 
which can be obtained [here](https://www.newsapi.org).

## API Server

We created an [API](https://medium.com/ymedialabs-innovation/deploy-flask-app-with-nginx-using-gunicorn-and-supervisor-d7a93aa07c18) which is able to handle requests to collect News.
The API [stack](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-14-04)
is composed of the following modules:
  
 - [Ngnix](https://www.nginx.com/) (Web server and main load balancer, terminates HTTPS) (Optional)
 - [Gunicorn](http://flask.pocoo.org/docs/1.0/deploying/wsgi-standalone/) (WSGI)
 - [Flask](http://flask.pocoo.org/) (Python Web App)
 - [RabbitMQ](https://www.rabbitmq.com/) (Message Queue)
 - [PostgreSQL](https://www.postgresql.org/) (Relational Database)

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


### Requirements

Install a Compute Engine instance
Recommended OS: Ubuntu 16:

```
sudo apt-get install python build-essential  -y
sudo apt-get install python-pip python-dev -y
sudo apt-get install libpq-dev python-dev -y   # Required for psycopg2
sudo apt-get install git -y
sudo apt-get install python-pip -y
sudo apt-get install libpq-dev -y
sudo apt-get install rabbitmq-server -y
```

Clone repo

```
cd /usr/local/src
git clone https://github.com/gogasca/news_ml.git
```

Install dependencies

```
pip install -r requirements.txt
```

Install NLTK dependencies

```
python
>>>import nltk
>>>nltk.download("stopwords")
[nltk_data] Downloading package stopwords to /root/nltk_data...
[nltk_data]   Unzipping corpora/stopwords.zip.
True
>>>nltk.download('punkt')
[nltk_data] Downloading package punkt to /root/nltk_data...
[nltk_data]   Unzipping tokenizers/punkt.zip.
```

## Database information

You need to create a new Database based on PostgreSQL:
Check the database example:

```
Check news_ml/conf/database for extracted schema.
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

Update these parameters accordingly in the following files:

```
vim ~/.bashrc
vim ~/.profile
```

Change the following variables based on your settings:

```
export DBHOST=127.0.0.1
export DBPORT=5432
export DBUSERNAME="postgres"
export DBPASSWORD="postgres"
export DBNAME="newsml"

# NEWS API
export NEWS_API_KEY=""

# Key for Email support from mailgun.com
export MAILGUN_API_KEY="key-"

# System API information. 
export API_USERNAME="AC64861838b417b555d1c8868705e4453f" 
export API_PASSWORD="YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o" 

# Key used for encrypting user information.
export SECRET_FERNET_KEY="" # Change this
```

Note: To generate SECRET_FERNET_KEY can be generated as follows:

```
>>> from cryptography.fernet import Fernet
>>> key = Fernet.generate_key()
>>> f = Fernet(key)
>>> token = f.encrypt(b"YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o")
>>> token
```
Use token value


## RabbitMQ

```
Edit /etc/hosts or your DNS server with rabbitmq hostname.
This needs to match the /conf/celeryconfig.py File

BROKER_URL = 'amqp://news_ml:news_ml@rabbitmq:5672'
```

Start RabbitMQ

```
/usr/local/sbin/rabbitmq-server
```

```
rabbitmqctl add_user news_ml news_ml
rabbitmqctl set_user_tags news_ml administrator
rabbitmqctl set_permissions -p / news_ml ".*" ".*" ".*"
```

## Celery (manually)

```
celery worker -n %h -P processes -c 15 --loglevel=DEBUG -Ofair
```

## Start API (manually)

Depending on the path where you clone the repo you may need to edit the file.

```
GUNICORN_LOGFILE=/usr/local/src/news_ml/log/gunicorn.log
API_PORT=8081
NUM_WORKERS=1
TIMEOUT=60
WORKER_CONNECTIONS=1000
BACKLOG=500
LOG_LEVEL=DEBUG

cd news_ml/api/version1_0
gunicorn news_ml:api_app --bind 0.0.0.0:$API_PORT --log-level=$LOG_LEVEL --log-file=$GUNICORN_LOGFILE --workers $NUM_WORKERS --worker-connections=$WORKER_CONNECTIONS --backlog=$BACKLOG --timeout $TIMEOUT &
```


## Supported API endpoints

```
/api/1.0/status
/api/1.0/campaign
/api/1.0/clustering
/api/1.0/person
/api/1.0/news
/api/1.0/rank
```

## Example:

Check API status

```
curl -u AC64861838b417b555d1c8868705e4453f:YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o http://0.0.0.0:8081/api/1.0/status
```

Request News from NEWS API:

```
curl -u AC64861838b417b555d1c8868705e4453f:YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o -H "Content-Type: application/json" -X POST -d '{ "provider": "news_api"}' http://0.0.0.0:8081/api/1.0/campaign
```

Request News from NEWS API using a Report:

```
curl -u AC64861838b417b555d1c8868705e4453f:YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o -H "Content-Type: application/json" -X POST -d '{ "provider": "news_api", "report": {"email": "noreply@google.com"}}' http://0.0.0.0:8081/api/1.0/campaign
``` 

Search for news including 'tensorflow' from NEWS API:

```
curl -u AC64861838b417b555d1c8868705e4453f:YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o -H "Content-Type: application/json" -X POST -d '{ "provider": "news_api", "query": "tensorflow, sagemaker, keras, petastorm"}' http://0.0.0.0:8081/api/1.0/campaign
``` 

Read for existing news:

```
curl -u AC64861838b417b555d1c8868705e4453f:YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o -H "Content-Type: application/json" http://0.0.0.0:8081/api/1.0/news
``` 

Read for news from amazon.com:

```
curl -u AC64861838b417b555d1c8868705e4453f:YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o -H "Content-Type: application/json" http://0.0.0.0:8081/api/1.0/news?source=amazon.com
```


## Manage services via supervisor (optional)

Add the following ENV ```export C_FORCE_ROOT="true"``` to the following files:


```
vim ~/.bashrc
vim ~/.profile
```


```
mkdir -p /etc/supervisor/conf.d
mkdir /var/log/supervisor/

cp /usr/local/bin/supervisorctl /usr/bin/
cp /usr/local/bin/supervisord /usr/bin/
cp /usr/local/src/news_ml/conf/supervisor/celeryd.conf /etc/supervisor/conf.d
cp /usr/local/src/news_ml/conf/supervisor/supervisord.conf /etc/supervisor/
    
```

Start supervisor after reboot:

```
cd /etc/supervisor/
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

## Loadbalancer (Optional)

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


## Database information

How to generate schema? Please read here:
https://pydigger.com/pypi/sqlacodegen

```
postgresql://username:password@hostname/database
```

```
CREATE TABLE api_users
(
    id              serial primary key,
    username        VARCHAR(256) unique not null,
	password_hash   VARCHAR(256) not null,
    created         timestamp(6) WITH TIME ZONE
);
```



## Ranking algorithm

```
    def rank(self):
        """Assign score based on source.
        Sources defined in settings file.

        :return:
        """
    
        try:
            self._ranking_source = settings.ranking_sources.index(self._source)
        except ValueError:
            self._ranking_source = settings.unknown_source_score

        try:
            self._ranking_provider = settings.ranking_providers.index(self._provider)
        except ValueError:
            self._ranking_provider = settings.unknown_provider_score

        # Articles which are read first are prioritized. Divide 100 by weight to prioritize higher values
        self.score += 20 // self._ranking_source
        self.score += 30 // self._ranking_provider
        self.score += self.order + random.randrange(0, 10)
        
```

## Cronjob

You can use a cronjob to generate a report every 6 hours. Example:

```
crontab -e
0 */6 * * * /usr/local/src/news_ml/utils/scripts/get_news.sh 
```

## Troubleshooting

Problem: Supervisor not starting services.

Solution: Validate permissions for .sh scripts (Executable)

--

Problem: Supervisor not starting API service.

Solution: Check gunicorn ```gunicorn --log-file=- news_ml:api_app```

--

Problem: Supervisor not starting Celery service.

Solution: Validate RabbitMQ is started

--

Problem: Can't start services.

Solution: Install nltk dependencies from root.

--

Problem: Can't start services.

Solution: ```sudo -i```, verify ```.bashrc``` and ```.profile```. 


## Questions?

Bugs and issues can be reported at gogasca [at] google [dot] com

