# Используем минимальный официальный образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt .

# Обновляем pip и устанавливаем зависимости, включая python-dotenv
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install python-dotenv

# Копируем исходный код проекта в рабочую директорию
COPY . .

# Команда для запуска бота
CMD ["python", "bot.py"]
