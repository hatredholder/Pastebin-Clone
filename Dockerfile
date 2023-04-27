FROM python:alpine
WORKDIR /code

RUN pip install --upgrade pip

COPY /requirements/base.txt /code/
RUN pip install -r base.txt
COPY . /code/
