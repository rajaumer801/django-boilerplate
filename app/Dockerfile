###########
# BUILDER #
###########

# pull official base image
FROM python:3.8-slim-buster as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update && apt-get install -y gcc python3-dev

RUN pip install --upgrade pip
COPY . .

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.8-slim-buster

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup app && useradd -g app app

# create the appropriate directories, required when using non-root user
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME


# install dependencies
RUN apt-get update && apt-get install -y gcc python3-dev

COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy project
COPY . $APP_HOME

RUN mkdir -p $APP_HOME/{{cookiecutter.main_module}}/static
RUN mkdir -p $APP_HOME/{{cookiecutter.main_module}}/media

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app
