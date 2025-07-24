FROM python:3.13-slim

WORKDIR /backend
ENV PYTHONPATH=/app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry 1.8 (поддерживает Python 3.13)
RUN pip install --upgrade pip && \
    pip install poetry==1.8.0

# Копируем только файлы зависимостей
COPY pyproject.toml poetry.lock* ./

# Установка зависимостей
RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi --no-root

# Копируем остальной код
COPY . .

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]