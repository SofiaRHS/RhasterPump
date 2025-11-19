# Используем официальный Python
FROM python:3.12-slim

# Рабочая директория
WORKDIR /app

# Копируем весь проект
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir websockets flask

# Открываем порт для Render
EXPOSE 10000

# Переменная окружения для Flask
ENV FLASK_RUN_PORT=10000
ENV FLASK_RUN_HOST=0.0.0.0

# Запуск main.py
CMD ["python", "main.py"]
