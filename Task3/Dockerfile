# Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY load_balancer.py /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "load_balancer.py"]
