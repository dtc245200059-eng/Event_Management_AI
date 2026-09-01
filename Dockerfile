# Base Image
FROM python:3.12-slim

# Set Working Directory
WORKDIR /app

# Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    PORT=5000

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies list
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Run Seeder to initialize DB and Mock Data
RUN python seed.py

# Expose Port
EXPOSE 5000

# Start Application
CMD ["python", "run.py"]
