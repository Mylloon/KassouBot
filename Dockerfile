FROM fredboat/lavalink:master

FROM python:3.8.6-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt update && \
    apt install -y --no-install-recommends ffmpeg

COPY src .

CMD [ "python", "-u", "./main.py" ]
