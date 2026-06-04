# Use official Python image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies (if any)
RUN pip install --no-cache-dir --upgrade pip

# Copy requirements first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Default command: run the orchestrator (override in compose)
CMD ["python", "orchestrator/runner.py"]