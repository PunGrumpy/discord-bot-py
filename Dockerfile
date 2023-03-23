FROM python:3.11 AS runner
LABEL AUTHOR="PunGrumpy"
LABEL MAINTAINER="PunGrumpy: Discord bot with pycord"

WORKDIR /app/discord-bot

COPY . .

RUN pip install -r requirements.txt && \
    rm -rf /root/.cache/pip

RUN git config --global --add safe.directory /app/discord-bot

CMD ["python", "main.py"]