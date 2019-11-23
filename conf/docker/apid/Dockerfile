#
# IMBUE Dockerfile
#
# Pull base image.
FROM python:3.6.4

# File Author / Maintainer
MAINTAINER Gonzalo Gasca Meza gogasca@


# Update the repository
# Set the locale
RUN apt-get update --fix-missing

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8

# Install dependencies
RUN apt-get install nano vim wget curl dialog net-tools iputils-ping openssh-server -y
RUN apt-get upgrade -y && apt-get dist-upgrade -y && apt-get install -y build-essential git-core
RUN apt-get install git -y
RUN apt-get install python build-essential  -y
RUN apt-get install python3-pip -y
RUN apt-get install libpq-dev python-dev -y   # Required for psycopg2

RUN apt-get install gunicorn -y
RUN apt-get install sudo -y
RUN pip3 install --upgrade pip

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile
RUN echo "export SECRET_FERNET_KEY=\"gAAAAABdt9nRsks3WHobSX-CZo3erIuG93Hs_riSl4sOZGvBNQ6DmSp6sEnMmpMttPjxXuGaBlp76e-9w4ItnBv90CyTuDzxVHS4P9-jEB_0_FvJ-whk9IMaMV4LI4FVAUmXGgIlBqV4\"" >> ~/.profile
RUN echo "export C_FORCE_ROOT=\"true\"" >> ~/.profile

RUN cd /usr/local/src
RUN git clone https://github.com/gogasca/news_ml.git

# Supervisor Install
RUN pip3 install supervisor

RUN mkdir -p /etc/supervisor/conf.d
RUN mkdir /var/log/supervisor/

RUN cp /usr/local/bin/supervisorctl /usr/bin/
RUN cp /usr/local/bin/supervisord /usr/bin/

# Supervisor configuration file
RUN rm -rf /etc/supervisor/conf.d/supervisord.conf
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN cat /etc/supervisor/conf.d/supervisord.conf

# Supervisor API and App Application
ADD apid.conf /etc/supervisor/conf.d/
ADD celeryd.conf /etc/supervisor/conf.d/

# mkdir log folder
RUN mkdir -p /usr/local/src/news_ml/log

# Define mountable directories.
VOLUME ["/usr/local/src/news_ml/conf/", "/usr/local/src/news_ml/api/", "/usr/local/src/news_ml/log"]

ADD requirements.txt /usr/local/src/news_ml/
RUN pip3 install -r /usr/local/src/news_ml/requirements.txt -U

# Install NLTK dependencies
RUN python3 -c 'import nltk;nltk.download("stopwords");nltk.download("punkt")'

WORKDIR /usr/local/src/news_ml

# Expose ports. App
EXPOSE 8081

CMD ["/usr/bin/supervisord"]