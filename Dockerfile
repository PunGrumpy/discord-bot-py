FROM python:3.12.0-alpine3.14 AS builder
LABEL author="PunGrumpy"

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --prefix=/install -r /tmp/requirements.txt

FROM python:3.12.0-alpine3.14 AS runner

COPY --from=builder /install /usr/local

COPY . /app

WORKDIR /app

CMD ["python", "main.py"]
