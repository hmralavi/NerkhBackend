
FROM python:3.9.19

WORKDIR /nerkh-backend

RUN apt-get update
RUN apt-get install build-essential -y

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY src/* /nerkh-backend

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"]