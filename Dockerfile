FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code


COPY pyproject.toml uv.lock /code/


RUN uv sync --frozen --no-cache


COPY ./app /code/app


CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]