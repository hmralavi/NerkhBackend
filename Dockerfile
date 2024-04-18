# syntax=docker/dockerfile:1
FROM python:3.9.19
WORKDIR /nerkh-backend
RUN apt-get update
RUN apt-get install build-essential -y
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY src/* ./
# EXPOSE 10000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]