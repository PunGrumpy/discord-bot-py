FROM python:3.11 AS builder
LABEL author="PunGrumpy"

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --prefix=/install -r /tmp/requirements.txt

FROM python:3.11 AS runner

COPY --from=builder /install /usr/local

COPY . /app

WORKDIR /app

CMD ["python", "main.py"]
