FROM python:3.11

COPY . .

RUN pip install -r requirements.txt && rm -rf requirements.txt

RUN python main.py
