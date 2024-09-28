# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /app

COPY supervisord.conf /etc/supervisor/supervisord.conf

RUN pip install --upgrade pip
RUN pip install pika supervisor

RUN mkdir /etc/periodic/1min
RUN mkdir /etc/periodic/5min

RUN chmod -R a+x /etc/periodic/1min
RUN chmod -R a+x /etc/periodic/5min
RUN chmod -R a+x /etc/periodic/15min

RUN echo "*/1 * * * * run-parts /etc/periodic/1min" >> /etc/crontabs/root
RUN echo "*/5 * * * * run-parts /etc/periodic/5min" >> /etc/crontabs/root

COPY entrypoint.sh /scripts/entrypoint.sh
RUN chmod +x /scripts/entrypoint.sh

ENTRYPOINT [ "/scripts/entrypoint.sh" ]
