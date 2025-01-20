FROM python:3.10-slim AS poetry_py

RUN pip install --no-cache-dir poetry==2.0.1
RUN poetry self add poetry-plugin-export

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-cache --no-root
RUN poetry export --without-hashes -f requirements.txt > requirements.txt

FROM python:3.10-slim AS final

WORKDIR /app
COPY --from=poetry_py /app/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY service_loopback /app/service_loopback
WORKDIR /app/service_loopback
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
