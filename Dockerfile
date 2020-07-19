FROM python:3.8.4-slim

RUN mkdir -p /app/
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt \
        && rm -rf /root/.cache

COPY . /app/

CMD ["python", "-m", "advent"]
