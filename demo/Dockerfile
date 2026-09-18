FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn

COPY mock_app.py .

EXPOSE 8000

CMD ["uvicorn", "mock_app:app", "--host", "0.0.0.0", "--port", "8000"]