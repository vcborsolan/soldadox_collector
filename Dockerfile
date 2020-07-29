FROM python:3.8.1-slim-buster


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR /SOLDADOX

CMD ["gunicorn","--bind" , "0.0.0.0:5001" , "wsgi:app" , "--timeout","1200"]