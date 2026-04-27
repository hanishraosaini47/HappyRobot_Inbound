FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY seed/ ./seed/

EXPOSE 8000

CMD ["sh", "-c", "python -m seed.seed && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
