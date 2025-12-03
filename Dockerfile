# Build stage
FROM python:3.9-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --user -r requirements.txt

# Production stage
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/root/.local/bin:$PATH"

# Install runtime system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /root/.local /root/.local

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
