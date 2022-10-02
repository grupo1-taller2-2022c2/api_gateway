FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

COPY ./app /app/app

RUN apt-get -y update

RUN apt-get -y install \
  dos2unix \
  libpq-dev \
  libmariadb-dev-compat \
  libmariadb-dev \
  gcc \
  && apt-get clean

RUN pip install --no-cache-dir fastapi uvicorn pydantic[email] python-multipart