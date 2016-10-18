FROM python:3.5-slim
MAINTAINER Yusuke Miyazaki <miyazaki.dev@gmail.com>

RUN mkdir -p /app/
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt \
        && rm -rf /root/.cache

COPY . /app/

CMD ["python", "run.py"]
