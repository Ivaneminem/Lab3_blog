# Встановлюємо базовий образ Python
FROM python:3.11

# Встановлюємо робочу директорію в контейнері
WORKDIR /app

# Копіюємо файл вимог у робочу директорію
COPY requirements.txt .

# Встановлюємо залежності з файлу вимог
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо всі файли проекту в робочу директорію
COPY . .

# Відкриваємо порт 8000 для доступу до веб-застосунку
EXPOSE 8000

# Запускаємо команди міграцій та запуску сервера
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]