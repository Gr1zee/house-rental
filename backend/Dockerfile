FROM python:3.13-slim

WORKDIR /backend
ENV PYTHONPATH=/app

# Установка зависимостей
COPY pyproject.toml poetry.lock* ./
RUN pip install --upgrade pip && \
    pip install poetry==1.8.0 && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi --no-root

# Копируем весь код
COPY . .

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]