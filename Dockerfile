FROM python:3.8-slim-buster as build-python

RUN apt-get -y update \
    && apt-get install -y curl gcc build-essential libtool automake \
    # Cleanup apt cache
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY microservices/requirements.txt /app/
RUN pip install -r requirements.txt
COPY microservices /app/
CMD ["python", "service1.py"]
