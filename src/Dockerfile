FROM --platform=linux/amd64 python:3.10-alpine
WORKDIR /src
COPY ./requirements.txt /src/requirements.txt
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      build-base gcc python3-dev musl-dev libffi-dev openssl-dev cargo
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt
COPY ./app /src/app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
