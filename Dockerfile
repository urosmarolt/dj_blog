FROM nginx

RUN apt-get update
RUN apt-get install -y git vim python3.5 python3-pip supervisor

RUN git clone https://github.com/urosmarolt/dj_blog.git

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/


COPY  django-nginx.conf /etc/nginx/conf.d/default.conf

# restart nginx to load the config
RUN service nginx stop
