# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /app

COPY supervisord.conf /etc/supervisor/supervisord.conf

RUN pip install --upgrade pip
RUN pip install pika supervisor
