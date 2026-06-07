FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install fastapi uvicorn
COPY api.py ./
COPY api.py ./
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
