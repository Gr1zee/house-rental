FROM python:3.13
WORKDIR /app

# Устанавливаем Poetry
RUN pip install poetry

# Копируем зависимости
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-root

# Копируем код
COPY . .

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0"]