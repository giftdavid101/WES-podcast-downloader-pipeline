# Dockerfile
FROM apache/airflow:2.7.1

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt