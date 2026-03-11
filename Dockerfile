# Fixed: Use latest slim image instead of old python:3.9
FROM python:3.13-slim

# Fixed: Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Fixed: Copy only necessary files, not entire directory
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

# Fixed: Run as non-root user
USER appuser

# Fixed: Add health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/users')"

EXPOSE 5000

CMD ["python", "app.py"]
