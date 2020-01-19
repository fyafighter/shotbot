# base image
FROM python:3.8.0-alpine

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
# musl-dev provides libc, alpine-sdk provides make
RUN apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev alpine-sdk
# add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app