FROM python:3.10-bookworm

COPY venv /venv

RUN adduser --uid 1000 musicforprogramming
ADD musicforprogramming.py /usr/src
WORKDIR /usr/src/

USER musicforprogramming

CMD ["/venv/bin/python", "musicforprogramming.py"]