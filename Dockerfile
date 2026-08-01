# Dockerfile
FROM apache/airflow:3.3.0

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt