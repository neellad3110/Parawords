FROM python:3
WORKDIR /app
COPY . /app

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

RUN python manage.py migrate

EXPOSE 8000