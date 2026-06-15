FROM alpine:latest

# Install Python and pip
RUN apk add --no-cache python3 py3-pip

# Create a non-root user
RUN adduser -D -u 1000 appuser

WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --break-system-packages

# Copy application
COPY app.py .
COPY templates/ templates/
COPY static/ static/

# Hand off to non-root user
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

CMD ["gunicorn", \
     "--bind", "0.0.0.0:8080", \
     "--workers", "2", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "app:app"]
