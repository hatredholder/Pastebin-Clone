FROM python:alpine
WORKDIR /code

RUN pip install --upgrade pip

COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
