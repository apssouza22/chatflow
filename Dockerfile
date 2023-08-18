FROM python:3.10-slim-buster AS ApiImage

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip setuptools wheel
WORKDIR /app/
COPY ./requirements.txt ./requirements.txt
RUN python3 -m pip install --no-cache-dir --upgrade -r requirements.txt
#COPY ./requirements-data.txt ./requirements-data.txt
#RUN python3 -m pip install -r requirements-data.txt
COPY ./server/src ./src

WORKDIR /app/src
CMD ["sh", "/app/src/prepare-and-start.sh"]
