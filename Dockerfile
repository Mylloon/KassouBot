FROM python:3.9.2-slim

RUN apt update && \
    apt install -y --no-install-recommends ffmpeg git && \
    apt autoremove
RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src .

CMD [ "python", "-u", "./main.py" ]
