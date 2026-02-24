# Use an official Python runtime as the base image.
FROM python:3.12-slim

# Avoid writing .pyc files and force stdout/stderr to flush directly.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container.
WORKDIR /app

# Copy dependency file first to leverage Docker layer caching.
COPY requirements.txt .

# Install Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend source code.
COPY . .

# Document the port this service listens on.
EXPOSE 5000

# Start the Flask application.
CMD ["python", "app.py"]
