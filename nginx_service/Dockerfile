FROM nginx
RUN mkdir /tmp/uwsgi
RUN touch /tmp/uwsgi/django_app.sock
RUN mkdir /usr/src/django_app
COPY ./uwsgi_params /etc/nginx/uwsgi_params
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./django.nginx.conf /etc/nginx/sites-available/django.nginx.conf
RUN mkdir /etc/nginx/sites-enabled
RUN ln -s /etc/nginx/sites-available/django.nginx.conf /etc/nginx/sites-enabled/
CMD ["nginx", "-g", "daemon off;"]
