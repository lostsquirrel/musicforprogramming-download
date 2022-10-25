FROM docker.io/python:3.10 AS builder

RUN pip install --user pipenv

ENV PIPENV_VENV_IN_PROJECT=1

ADD Pipfile.lock Pipfile /usr/src/

WORKDIR /usr/src

RUN /root/.local/bin/pipenv sync

FROM docker.io/python:3.10 AS runtime

RUN mkdir -v /usr/src/venv

COPY --from=builder /usr/src/.venv/ /usr/src/venv/

RUN adduser --uid 1000 musicforprogramming
ADD musicforprogramming.py /usr/src
WORKDIR /usr/src/

USER musicforprogramming

CMD ["./venv/bin/python", "-m", "musicforprogramming.py"]