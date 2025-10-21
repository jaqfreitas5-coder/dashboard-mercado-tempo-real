FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

COPY requirements-minimal.txt .

RUN pip install --no-cache-dir -r requirements-minimal.txt

COPY backend/ ./backend/

EXPOSE 8000

CMD cd backend && python main_simple.py
