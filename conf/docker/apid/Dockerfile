#
# NewsML
#
# Pull base image.
FROM python:3.6.4

# File Author / Maintainer
MAINTAINER Gonzalo Gasca Meza gogasca@

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
RUN apt-get install python build-essential  -y
RUN apt-get install python3-pip -y
RUN apt-get install libpq-dev python-dev -y   # Required for psycopg2

RUN apt-get install gunicorn -y
RUN apt-get install sudo -y
RUN pip3 install --upgrade pip

RUN echo "export SECRET_FERNET_KEY=\"gAAAAABdt9nRsks3WHobSX-CZo3erIuG93Hs_riSl4sOZGvBNQ6DmSp6sEnMmpMttPjxXuGaBlp76e-9w4ItnBv90CyTuDzxVHS4P9-jEB_0_FvJ-whk9IMaMV4LI4FVAUmXGgIlBqV4\"" >> ~/.profile
RUN echo "export C_FORCE_ROOT=\"true\"" >> ~/.profile

# Install dependencies.
ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt -U
# Install NLTK dependencies.
RUN python3 -c 'import nltk;nltk.download("stopwords");nltk.download("punkt")'

# Supervisor Install
RUN pip3 install supervisor

RUN mkdir -p /etc/supervisor/conf.d
RUN mkdir /var/log/supervisor/

RUN cp /usr/local/bin/supervisorctl /usr/bin/
RUN cp /usr/local/bin/supervisord /usr/bin/

# Supervisor configuration file
RUN rm -rf /etc/supervisor/supervisord.conf
ADD supervisord.conf /etc/supervisor/supervisord.conf
ADD apid.conf /etc/supervisor/conf.d/
ADD celeryd.conf /etc/supervisor/conf.d/

# mkdir log folder
RUN mkdir -p /usr/local/src/news_ml/log

# Define mountable directories.
VOLUME ["/usr/local/src/news_ml/log"]

WORKDIR /usr/local/src/news_ml

# Expose ports. API
EXPOSE 8081

CMD ["/usr/bin/supervisord"]
