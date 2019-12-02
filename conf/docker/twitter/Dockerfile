#
# NewsML
#
# Pull base image.
FROM python:3.6.4

# File Author / Maintainer
MAINTAINER Gonzalo Gasca Meza gogasca@

# Install dependencies.
ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt -U

ADD twitter_listener.py /

CMD [ "python", "./twitter_listener.py" ]
