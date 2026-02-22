FROM python:3.11-slim

WORKDIR /app
COPY . .

WORKDIR /app/src

ENTRYPOINT ["python", "-m", "elysia_core.cli"]
CMD [""]