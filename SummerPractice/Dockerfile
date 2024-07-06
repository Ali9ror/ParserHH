FROM python:3.10-alpine
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir /tmp/uwsgi
WORKDIR /usr/src/django_app
COPY . /usr/src/django_app
RUN apk add python3-dev build-base linux-headers pcre-dev
RUN pip install uwsgi
RUN pip install -r requirements.txt
RUN chmod +x /usr/src/django_app/docker-entrypoint.sh
ENTRYPOINT [ "/bin/sh","/usr/src/django_app/docker-entrypoint.sh" ]
