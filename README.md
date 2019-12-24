# News ML

## Introduction

This application collects news information from News 
API. App collects information from fixed sources, if search feature is
used API will look into all news in API for a specific time period that
match search pattern.
App extract entities from News content via Google Cloud NLP and 
perform sentiment analysis.

## Quickstart

You can use [this](mini/app.py) sample Python script  
which collects News and stores them into a CSV file using News API Key 
which can be obtained [here](https://www.newsapi.org).

## Architecture

I created an [API](https://medium.com/ymedialabs-innovation/deploy-flask-app-with-nginx-using-gunicorn-and-supervisor-d7a93aa07c18) which is able to handle requests to collect News.
The API [stack](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-14-04)
is composed of the following modules:
  
 - [Ngnix](https://www.nginx.com/) (Web server and main load balancer, terminates HTTPS) (Optional)
 - [Gunicorn](http://flask.pocoo.org/docs/1.0/deploying/wsgi-standalone/) (WSGI)
 - [Flask](http://flask.pocoo.org/) (Python Web App)
 - [RabbitMQ](https://www.rabbitmq.com/) (Message Queue)
 - [PostgreSQL](https://www.postgresql.org/) (Relational Database)
 
```
REST API Server -> Ngnix --> Gunicorn --> Flask --> News app -> PostgreSQL
                                                    RabbitMQ
```    

## Docker containers installation

We created a group of containers to help you deploy the application faster.
If you are interested in setting up the application manually please go to the Full Installation section.

Take a look at [Docker configuration](conf/docker) for more information about how to run this application using containers.
You will need:

- [Docker API server](conf/docker/apid/)
- [Docker RabbitMQ](conf/docker/rabbitmq) or external [RabbitMQ server](https://www.rabbitmq.com/rabbitmq-server.8.html)
- External PostgreSQL database (Example: Google Cloud SQL w/proxy)


## Full installation

To perform a manual installation follow the next steps:

## Software requirements

Python based API:

 - Flask
 - Gunicorn
 - Celery 
 - RabbitMQ
 - PostgreSQL
 - Ngnix
 - Google Cloud NLP
 - Ngnix -> Gunicorn -> Flask -> RabbitMQ/Celery/Postgres.
 
### Requirements

Install a Compute Engine instance using Ubuntu 16.

Python version: 3.6
 
```
sudo apt-get install python build-essential  -y
sudo apt-get install libpq-dev python-dev -y   # Required for psycopg2
sudo apt-get install git -y
sudo apt-get install python3-pip -y
sudo apt-get install rabbitmq-server -y
```

Clone GitHub repo

```
cd /usr/local/src
git clone https://github.com/gogasca/news_ml.git
```

Install dependencies

```
pip3 install -r requirements.txt
```

Install NLTK dependencies

Single line command:
```
python3 -c 'import nltk; nltk.download("stopwords"); nltk.download("punkt")'
```

Python Terminal:

```
python
>>>import nltk
>>>nltk.download("stopwords")
[nltk_data] Downloading package stopwords to /root/nltk_data...
[nltk_data]   Unzipping corpora/stopwords.zip.
True
>>>nltk.download("punkt")
[nltk_data] Downloading package punkt to /root/nltk_data...
[nltk_data]   Unzipping tokenizers/punkt.zip.
```

## Database information

You need to create a new Database based on PostgreSQL server:
 - Check [conf/database/news_ml.sql] for Database creation.
 - Check [conf/database/schema.sql] for Database schema.

## Using Google Cloud SQL proxy

```
./cloud_sql_proxy -instances=<>Project>:<Zone>:<Instance name>=tcp:5432
```

Example:
```
./cloud_sql_proxy -instances=news-ml:us-central1:newsml-database-1=tcp:5432
```
## Using Using Google Cloud SQL proxy Docker container

```
docker run -d \
  -v <PATH_TO_KEY_FILE>:/config \
  -p 127.0.0.1:5432:5432 \
  gcr.io/cloudsql-docker/gce-proxy:1.16 /cloud_sql_proxy \
  -instances=<INSTANCE_CONNECTION_NAME>=tcp:0.0.0.0:5432 -credential_file=/config
```

## RabbitMQ

Start RabbitMQ server:

```
/usr/local/sbin/rabbitmq-server
```

```
rabbitmqctl add_user news_ml news_ml
rabbitmqctl set_user_tags news_ml administrator
rabbitmqctl set_permissions -p / news_ml ".*" ".*" ".*"
```

## Celery

Start Celery and verify RabbitMQ tasks are successful.

```
export RABBITMQ_USER=news_ml
export RABBITMQ_PASSWORD=news_ml
export RABBITMQ_HOSTNAME=rabbitmq
export RABBITMQ_PORT=5672

cd /usr/local/src/news_ml/conf/
celery worker -n 1 -P processes -c 15 --loglevel=DEBUG -Ofair
```

## Environment variables

Update these parameters accordingly in the following files:

```
vim ~/.bashrc
vim ~/.profile
```

Change the following variables based on your settings:

```
export NEWSML_ENV="/usr/local/src/news_ml/"
```

Configure Database parameters:

```
export DBHOST=127.0.0.1
export DBPORT=5432
export DBUSERNAME="postgres"
export DBPASSWORD="postgres"
export DBNAME="newsml"

# NEWS API
export NEWS_API_KEY=""  # Change this www.newsapi.org

# System API information. 
export API_USERNAME="AC64861838b417b555d1c8868705e4453f" 
export API_PASSWORD="YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o" 

# Key for Email support from mailgun.com
export MAILGUN_API_KEY="key-"  # Change this
export MAILGUN_DOMAIN=""

# Key used for encrypting user information.
export SECRET_FERNET_KEY=""  # Change this
```

Note: To generate `SECRET_FERNET_KEY` can be generated as follows:

```
>>> from cryptography.fernet import Fernet
>>> key = Fernet.generate_key()
>>> f = Fernet(key)
>>> token = f.encrypt(b"YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o")
>>> token
```
Use token value

## Database schema generation

How to generate schema? Please read here:
https://pydigger.com/pypi/sqlacodegen

```
postgresql://username:password@hostname/database
```


## Configure API settings

Depending on the path where you clone the repo you may need to edit the file.

Define `NEWSML_ENV`:

```
if platform.system() == 'Linux':
    filepath = '/usr/local/src/news_ml/'
else:
    filepath = '/Users/user/Documents/Development/news/'
```


```
export GUNICORN_LOGFILE=/tmp/gunicorn.log
export API_PORT=8081
export NUM_WORKERS=1
export TIMEOUT=60
export WORKER_CONNECTIONS=1000
export BACKLOG=500
export LOG_LEVEL=DEBUG
```

Start API server

```
cd /usr/src/src/news_ml/api/version1_0
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

- Check API status

Local Authentication:

```
curl -u AC64861838b417b555d1c8868705e4453f:YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o -H "Content-Type: application/json" http://0.0.0.0:8081/api/1.0/
```

Database authentication:

```
curl -u AC64861838b417b555d1c8868705e4453f:YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o http://0.0.0.0:8081/api/1.0/status
```

- Request News from NEWS API:

```
curl -u AC64861838b417b555d1c8868705e4453f:YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o -H "Content-Type: application/json" -X POST -d '{ "provider": "news_api"}' http://0.0.0.0:8081/api/1.0/campaign
```

- Request News from NEWS API using a Report:

```
curl -u AC64861838b417b555d1c8868705e4453f:YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o -H "Content-Type: application/json" -X POST -d '{ "provider": "news_api", "report": {"email": "no-reply@newsml.io"}}' http://0.0.0.0:8081/api/1.0/campaign
``` 

- Search for news including 'tensorflow, keras and sagemaker' from NEWS API:

```
curl -u AC64861838b417b555d1c8868705e4453f:YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o -H "Content-Type: application/json" -X POST -d '{ "provider": "news_api", "query": "tensorflow, sagemaker, keras"}' http://0.0.0.0:8081/api/1.0/campaign
``` 

- Request News from TechMeme:

```
curl -u AC64861838b417b555d1c8868705e4453f:YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o -H "Content-Type: application/json" -X POST -d '{ "provider": "techmeme"}' http://0.0.0.0:8081/api/1.0/campaign
```

- Read for existing news:

```
curl -u AC64861838b417b555d1c8868705e4453f:YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o -H "Content-Type: application/json" http://0.0.0.0:8081/api/1.0/news
``` 

- Read for news from amazon.com:

```
curl -u AC64861838b417b555d1c8868705e4453f:YYPKpbIAYqz90oMN8A11YYPKpbIAYqz90o -H "Content-Type: application/json" http://0.0.0.0:8081/api/1.0/news?source=amazon.com
```

**Note:** If using zsh add: curl -w '\n' to avoid % at the end of response

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

Table api_users is the following:

```
CREATE TABLE api_users
(
    id              serial primary key,
    username        VARCHAR(256) unique not null,
	password_hash   VARCHAR(256) not null,
    created         timestamp(6) WITH TIME ZONE
);
```


## Token authentication

There is a good chance for Man in the middle attack while requesting data. 
In case of HTTP Basic Authentication, user credentials are sent along with every request which can be breached. 
So we use token based authentication, users request for a token and in the subsequent requests users use the obtained 
token to access data. This token lives for a short span of time, even if the attacker manages to get hold of the token, 
its only valid for short span of time. This way we can add one more layer of security to the REST API.


## Manage NewsML Services via supervisor 



```
pip3 install supervisor
```

Add the following environment variables:

```
export NEWSML_ENV="/usr/local/src/news_ml/"
export C_FORCE_ROOT="true"
```

to the following files:

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
supervisord -c /etc/supervisor/supervisord.conf
```

Use supervisorctl to check services status.


### Upgrades

```
cd /usr/local/src/news_ml
git pull

supervisorctl restart all
supervisorctl status
```

## Load balancer (Optional)

Ngnix acts as our API load balancer.

```
    apt-get update
    locale-gen en_US en_US.UTF-8
    apt-get install -y nano vim wget dialog net-tools
    apt-get install -y nginx nginx-common nginx-extras
    vim /etc/nginx/sites-available/default
    vim nginx.conf 
```

## Ranking algorithm

```
    def rank(self):
        """Assign score based on source.
        Sources defined in settings file.

        :return:
        """
    
        try:
            self._ranking_source = settings.RANKING_SOURCES.index(self._source)
        except ValueError:
            self._ranking_source = settings.UNKNOWN_SOURCE_SCORE

        try:
            self._ranking_provider = settings.RANKING_PROVIDERS.index(self._provider)
        except ValueError:
            self._ranking_provider = settings.UNKNOWN_PROVIDER_SCORE

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

Bugs and issues can be reported at support [at] newsml [dot] io
