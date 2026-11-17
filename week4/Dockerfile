FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY week4/pg_etl.py .


CMD ["python","pg_etl.py"]