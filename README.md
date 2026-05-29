# Py-Scraper-Integrator

Асинхронный Python-сервис для парсинга веб-страниц и автоматической отправки данных в Google Sheets.
![Python Version](https://img.shields.io/badge/python-3.14-blue?style=flat-square&logo=python&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%E2%9C%93-blue?style=flat-square&logo=docker&logoColor=white) ![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

> **Важное примечание:**  
> На текущий момент scraper работает **только с сайтом Читай-город** (chitai-gorod.ru).  

Проект создавался как lightweight ETL-инструмент для автоматизации рутинного сбора данных: мониторинга цен, сбора объявлений, обновления каталогов и аналитических таблиц.

**Результаты парсинга:**
[![Google Sheets](https://img.shields.io/badge/Google_Sheets-10k+_записей-green?style=flat-square&logo=google-sheets&logoColor=white)](https://docs.google.com/spreadsheets/d/1p79ZRntXOnKVh7qT5MY59zquakvTdNvzTdFop4dVyC0/edit?usp=sharing)

## Основные возможности

- Асинхронный парсинг на `aiohttp`
- Интеграция с Google Sheets через Google Service Account
- Контейнеризация в Docker
- Конфигурация через `.env`
- Изоляция секретов через volume mounts
- Простая модульная структура

---

## Технологический стек

- Python 3.14
- aiohttp
- asyncio
- gspread
- Docker

---

## Архитектура

```text
Сайт → Асинхронный парсер → Обработка данных → Google Sheets
```

### Project structure

```text
Py-Scraper-Integrator/
├── main.py          # Точка входа
├── scraper.py       # Логика асинхронного парсинга
├── sheets.py        # Интеграция с Google Sheets
├── requirements.txt
├── Dockerfile
├── .env.example
├── .gitignore
└── README.md
```

---

# Переменные окружения

Create `.env` file:

```env
BASE_URL=https://github.com
ENDPOINT=/fkfjdkso/py-scraper-integrator
CREDENTIALS_FILE=/app/credentials.json
SHEET_NAME=SHEET NAME
```

---

## Настройка Google Sheets

1. Создайте новую Google Таблицу
2. Создайте Service Account в Google Cloud Console
3. Скачайте JSON-файл с ключами
4. Добавьте email сервисного аккаунта в таблицу с правами «Редактор»
5. Поместите файл с ключами в корень проекта

---

## Запуск через Docker

### Сборка образа

```bash
docker build -t py-scraper-integrator .
```

### Запуск контейнера

```powershell
docker run --rm -it --env-file .env -v "$(Get-Location)/credentials.json:/app/credentials.json" py-scraper-integrator
```

---

## Примеры использования

- Мониторинг цен
- Парсинг маркетплейсов
- Автоматический сбор данных
- Лёгкие ETL-пайплайны
- Автоматическое наполнение отчётов в Google Sheets

---

## Почему асинхронный?

Использование асинхронных запросов позволяет парсеру обрабатывать несколько страниц параллельно, вместо того чтобы ждать завершения каждого запроса последовательно.

Это значительно повышает пропускную способность для задач, ограниченных скоростью ввода-вывода (IO-bound), к которым относится веб-скрейпинг.

---

## Замечания по безопасности

- Секреты исключены через `.gitignore`
- Ключи монтируются в контейнер только во время запуска
- Переменные окружения отделены от исходного кода

---

## Лицензия

MIT
