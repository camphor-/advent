FROM python:3.10-slim

RUN mkdir -p /app/
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./data /app/data
COPY ./output /app/output

RUN pip install -r requirements.txt \
        && rm -rf /root/.cache

COPY . /app/

CMD ["python", "-m", "advent"]
