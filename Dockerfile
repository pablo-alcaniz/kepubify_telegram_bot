FROM debian:bookworm-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=1

WORKDIR /app

COPY pyproject.toml ./

RUN uv sync --no-dev


FROM debian:bookworm-slim

COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

RUN apt-get update && apt-get install -y \
    libpython3.11 \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY src/bot.py .
COPY src/kepubify . 
COPY src/TELEGRAM_API_TOKEN .

RUN chmod +x ./kepubify

ENV PYTHONUNBUFFERED=1

CMD [ "uv", "run", "bot.py" ]