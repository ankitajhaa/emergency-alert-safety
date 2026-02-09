FROM python:3.11-alpine3.19
LABEL maintainer="django_task.com"

ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/py/bin:$PATH"

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/python -m ensurepip && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    addgroup -S django && adduser -S django-user -G django

COPY . /app

USER django-user