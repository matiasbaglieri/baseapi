FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    screen \
    g++ \
    make \
    libopenblas-dev \
    liblapack-dev \
    gfortran \
    linux-headers-amd64 \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 80

# Command to run the application
# CMD ["python3.11", "app.py"] 
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "80"]