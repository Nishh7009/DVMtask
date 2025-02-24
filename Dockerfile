FROM python:3.12.3

# set work directory
WORKDIR /bus_booking

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /bus_booking/
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /bus_booking
