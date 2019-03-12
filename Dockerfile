FROM python:3.7-alpine as base

RUN apk --update add libpq
# prepare compiling environment as virtual package `build-dependencies`
RUN apk --update add --virtual build-dependencies \
  build-base \
  musl-dev \
  python3-dev \
  postgresql-dev \
  libffi-dev

RUN mkdir /var/log/loki/
WORKDIR /var/www/main

RUN pip install --no-cache-dir pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system

# remove compiling environment `build-dependencies`
RUN apk del build-dependencies

COPY . .

ARG version
ENV CONTAINER_VERSION ${version}

########################################
# dev stage for conveinent development envrionment
FROM base as dev
RUN apk --update add --no-cache curl bash less
RUN apk --update add --no-cache postgresql-client redis

########################################
# release stage
FROM base as release
