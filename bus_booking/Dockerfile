FROM python:3.12.3

# set work directory
WORKDIR /bus_booking

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv --python /usr/local/bin/python3.12

# copy project
COPY . /bus_booking

RUN pipenv install --system --deploy
