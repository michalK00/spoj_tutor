FROM python:3.11-alpine

WORKDIR /django

# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
# RUN apk update && apk add gcc python3-dev musl-dev

COPY requirements.txt requirements.txt
# RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
# COPY . .
# EXPOSE 8000
