# Полная инструкция по развертыванию Django проекта с Nginx и Gunicorn

## 1. Подготовка сервера

### 1.1. Обновление системы и установка базовых пакетов
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv python3-dev libpq-dev nginx git build-essential
```

### 1.2. Клонирование репозитория
```bash
git clone https://github.com/NikitaGryn/ppnn23.git
cd ppnn23
```

## 2. Настройка виртуального окружения и зависимостей

### 2.1. Создание и активация виртуального окружения

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2.2. Установка зависимостей

```bash
pip install --upgrade pip
pip install -r requirements.txt  # если файл есть в репозитории
```

## 3. Настройка Django проекта

### 3.1. Создание файла .env для переменных окружения

```bash
nano .env
```

Пример содержимого:
```ini
SECRET_KEY=

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

### 3.2. Применение миграций
```bash
python manage.py migrate
```

## 4. Настройка Gunicorn

### 4.1. Создание systemd службы
```bash
sudo nano /etc/systemd/system/gunicorn.service
```
Содержимое файла:
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/ppnn23
EnvironmentFile=/home/ppnn23/.env
ExecStart=/home/ppnn23/.venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          ppnn23.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 4.2. Запуск и автозагрузка Gunicorn
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn  
```

## 5. Настройка Nginx

### 5.1. Создание конфигурационного файла
```bash
sudo nano /etc/nginx/sites-available/ppnn23
```
Пример конфигурации:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        proxy_redirect off;
    }
}
```

### 5.2. Активация конфигурации
```bash
sudo ln -s /etc/nginx/sites-available/ppnn23 /etc/nginx/sites-enabled
sudo nginx -t  
sudo systemctl restart nginx
```

## 6. Настройка брандмауэра
```bash
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## 7. Проверка работы

1. Проверьте работу Gunicorn:
```bash
curl --unix-socket /run/gunicorn.sock http
```

2. Откройте в браузере ваш домен или IP-адрес сервера.

