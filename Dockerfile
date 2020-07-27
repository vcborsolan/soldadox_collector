FROM python:3-alpine

RUN apk add --virtual .build-dependencies \ 
            --no-cache \
            python3-dev \
            build-base \
            linux-headers \
            postgresql-dev \
            gcc \
            pcre-dev

RUN apk add --no-cache pcre

WORKDIR /SOLDADOX
COPY ./ /SOLDADOX
RUN pip install -r requirements.txt
RUN apk del .build-dependencies && rm -rf /var/cache/apk/*

RUN flask db init
RUN flask db migrate -m "Initial migration."
RUN flask db upgrade

CMD ["gunicorn","--bind" , "0.0.0.0:5001" , "wsgi:app" , "--timeout","1200"]