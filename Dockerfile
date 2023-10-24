# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Set environment variables that prevent Python from writing pyc files and buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# Create and set the working directory for the application
WORKDIR /app

# Install system dependencies (if required)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all the files from the local directory to the container's workdir.
COPY . /app

# Specify the command to run on container start (runs the FastAPI application)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
