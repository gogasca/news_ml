#
# Nginx Dockerfile
#
# https://github.com/dockerfile/nginx
#

# Pull base image.
FROM ubuntu

# File Author / Maintainer
MAINTAINER Gonzalo Gasca Meza gonzalo@

# Install Nginx.

# Update the repository
ENV LANG en_US.UTF-8
ENV DEBIAN_FRONTEND noninteractive

# Set hostname
RUN echo $(grep $(hostname) /etc/hosts | cut -f1) loadbalancer >> /etc/hosts

RUN apt-get update
RUN locale-gen en_US en_US.UTF-8
# Install necessary tools
RUN apt-get install -y nano vim wget dialog net-tools

# Download and Install Nginx
RUN apt-get install -y nginx nginx-common nginx-extras
RUN update-rc.d -f nginx disable

# Supervisor
RUN apt-get install supervisor -y
RUN update-rc.d -f supervisor disable

# Supervisor
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# start script
ADD startup /usr/local/bin/startup
RUN chmod +x /usr/local/bin/startup

CMD ["/usr/local/bin/startup"]

RUN mkdir /etc/nginx/ssl
# Copy a configuration file from the current directory
ADD nginx.conf /etc/nginx/
ADD nginx.key  /etc/nginx/ssl/
ADD nginx.crt  /etc/nginx/ssl/

# Define mountable directories.
VOLUME ["/etc/nginx/sites-enabled", "/etc/nginx/certs", "/etc/nginx/conf.d", "/var/log/nginx"]

# Expose ports.
EXPOSE 8443