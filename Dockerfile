FROM python:3.11 as runner
LABEL AUTHOR="PunGrumpy"
LABEL MAINTAINER="PunGrumpy: Discord bot with pycord"

COPY . .

RUN pip install -r requirements.txt && \
    rm -rf /root/.cache/pip

CMD ["python", "main.py"]