FROM python:3.11.9-slim-bookworm

RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

COPY . /app

RUN chown -R appuser:appuser /app

USER appuser

CMD ["bash", "tests/test.sh"]
