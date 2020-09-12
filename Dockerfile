FROM python:3.8-alpine
ADD requirements.txt /tmp/requirements.txt

RUN apk update \
    && apk add --no-cache --virtual build-deps gcc musl-dev libffi-dev openssl-dev \
    && pip3 install --no-cache -r /tmp/requirements.txt \
    && apk del build-deps

COPY app/ /app
CMD ["/app/main.py"]