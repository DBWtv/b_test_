# Используем базовый образ Python
FROM python:3.10

RUN apt-get update

# Установка рабочей директории внутри контейнера
WORKDIR /app

# Копируем исходный код FastAPI-приложения в контейнер
COPY . .

# Устанавливаем зависимости
RUN apt install libpq-dev gcc python3-dev -y
RUN pip install poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Запускаем FastAPI приложение при старте контейнера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
