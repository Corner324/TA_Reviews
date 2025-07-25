# Простой Dockerfile для сервиса анализа сентимента отзывов
FROM python:3.12-slim

# Устанавливаем uv для быстрого управления зависимостями
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

# Копируем код приложения
COPY app/ ./app/
COPY .env.example .env

# Создаем директории для ML модели и базы данных
RUN mkdir -p app/ml app/data

# Устанавливаем переменные окружения
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]