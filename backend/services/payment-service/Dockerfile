FROM python:3.11-slim
WORKDIR /app
COPY ../../shared/requirements.txt /app/shared-requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY ../../shared /app/shared
COPY . /app
ENV PYTHONPATH=/app
EXPOSE 8003
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
