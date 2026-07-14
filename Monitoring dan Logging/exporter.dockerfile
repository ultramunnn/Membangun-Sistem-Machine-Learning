FROM python:3.12-slim
WORKDIR /app
RUN pip install prometheus-client psutil
COPY 3.prometheus_exporter.py /app/exporter.py
EXPOSE 8000
CMD ["python", "/app/exporter.py"]
