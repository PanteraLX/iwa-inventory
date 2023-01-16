# Make a Docker container optimized for app development with Django

# Use the official Python image from the Docker Hub

FROM python:3.9

# Create a new user 'app-developer' and set the working directory to /home/app-developer

RUN useradd -ms /bin/bash iwa-developer

USER iwa-developer

RUN mkdir /home/iwa-developer/iwa-inventory

# Create directory iwa-inventory and make working directory

WORKDIR /home/iwa-developer/iwa-inventory

# Copy the requirements.txt file to the container at /app

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --user -r requirements.txt

# Copy the current directory contents into the container at /app

ADD . .

EXPOSE 8080