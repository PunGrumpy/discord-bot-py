FROM python:3.11

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

COPY . /app

WORKDIR /app

CMD ["python", "main.py"]
