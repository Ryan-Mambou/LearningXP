FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

# Copy application files
COPY server.py .
COPY index.html .
COPY static/ ./static/

ENV PATH=/root/.local/bin:$PATH

EXPOSE 5000

CMD ["python", "server.py"]