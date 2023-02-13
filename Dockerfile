FROM python:3.12.0a5-slim-bullseye
LABEL AUTHOR="PunGrumpy"
LABEL MAINTAINER="PunGrumpy: Discord bot with pycord"

WORKDIR /app/discord-bot

COPY . .

RUN pip install -r requirements.txt && \
    rm -rf /root/.cache/pip

RUN apt-get update && \
    apt-get install -y git

CMD ["python", "main.py"]