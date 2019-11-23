#
# NewsML RabbitMQ
#
# Pull base image.
FROM ubuntu
MAINTAINER Gonzalo Gasca Meza gonzalo@

# Install RabbitMQ
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F7B8CEA6056E8E56 && \
    echo "deb http://www.rabbitmq.com/debian/ testing main" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y rabbitmq-server pwgen && \
    rabbitmq-plugins enable rabbitmq_management && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# RabbitMQ configuration
ADD rabbitmq.config /etc/rabbitmq/
RUN chmod u+rw /etc/rabbitmq/rabbitmq.config

# RabbitMQ clustering
ADD erlang.cookie /var/lib/rabbitmq/.erlang.cookie
RUN chown rabbitmq:rabbitmq /var/lib/rabbitmq/.erlang.cookie
RUN chmod 400 /var/lib/rabbitmq/.erlang.cookie

# Add scripts
ADD set_rabbitmq_password.sh /set_rabbitmq_password.sh
RUN chmod 755 ./*.sh

# Start script
ADD startup /usr/local/bin/startup
RUN chmod +x /usr/local/bin/startup

EXPOSE 5672
EXPOSE 15672
EXPOSE 25672
EXPOSE 4369
EXPOSE 9100
EXPOSE 9101
EXPOSE 9102
EXPOSE 9103
EXPOSE 9104
EXPOSE 9105

CMD ["/usr/local/bin/startup"]