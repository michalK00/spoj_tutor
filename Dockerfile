FROM python:3.11-apline

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
END PYTHONUNBUFFERED 1

# Install system dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .
