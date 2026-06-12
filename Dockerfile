# Use Python 3.12-slim (matches your local Python version)
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Install system dependencies
# Fixed: removed space in "apt-get" and simplified packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project code
COPY . /app/

# Expose port
EXPOSE 8000

# Start command
CMD ["gunicorn", "ecommerce_api.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]