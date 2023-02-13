FROM python:3.12.0a5-slim-bullseye
LABEL AUTHOR="PunGrumpy"
LABEL MAINTAINER="PunGrumpy: Discord bot with pycord"

WORKDIR /app/discord-bot

COPY . .

RUN pip install -r requirements.txt && \
    rm -rf /root/.cache/pip

CMD ["python", "main.py"]