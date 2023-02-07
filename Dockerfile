FROM python:3.11

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt && rm -rf requirements.txt

COPY . .

CMD ["python", "main.py"]
