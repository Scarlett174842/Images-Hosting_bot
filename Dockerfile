# Используем Python 3.10
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы в контейнер
COPY . .

# Устанавливаем зависимости
RUN pip install --upgrade pip && pip install -r requirements.txt

# Запускаем бота
CMD ["python", "bot.py"]
