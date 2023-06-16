FROM python:3.11-alpine

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /django

# Install system dependencies
# RUN apk update && apk add postgresql gcc python3-dev musl-dev libpq-dev
COPY requirements.txt /django/
# RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# RUN python manage.py loaddata data.json


# Copy project
COPY . .
# EXPOSE 8000
