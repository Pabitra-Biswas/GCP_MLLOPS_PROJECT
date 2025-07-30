# 1. Use the official slim Python image from Docker Hub
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy and install your application
COPY . .
RUN pip install --no-cache-dir -e .

# 2. Ensure the training step is removed from here

EXPOSE 8080
CMD ["python", "application.py"]