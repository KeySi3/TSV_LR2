# Task Management

Сервис для управления задачами на базе **FastAPI** с сохранением данных в локальном JSON-файле.

## Структура проекта

```text
.
├── data/
│   └── tasks.json          # Файл хранения задач 
├── .dockerignore           # Исключения для сборки Docker
├── .gitignore              # Исключения для Git
├── docker-compose.yml      # Конфигурация запуска мультиконтейнерного окружения
├── Dockerfile              # Инструкция сборки Docker-образа
├── main.py                 # Основной файл приложения с эндпоинтами FastAPI
├── README.md               # Документация проекта
├── requirements.txt        # Список зависимостей Python
└── utils.py                # Вспомогательные функции для чтения и записи JSON
```

## Локальный запуск

Для запуска необходим установленный интерпретатор Python 3.11+.

1. **Перейдите в директорию проекта:**
   ```bash
   cd <путь_к_проекту>
   ```

2. **Создайте виртуальное окружение:**
   - На Linux / macOS:
     ```bash
     python3 -m venv .venv
     ```
   - На Windows:
     ```bash
     python -m venv .venv
     ```

3. **Активируйте виртуальное окружение:**
   - На Linux / macOS:
     ```bash
     source .venv/bin/activate
     ```
   - На Windows (CMD):
     ```cmd
     .venv\Scripts\activate.bat
     ```
   - На Windows (PowerShell):
     ```powershell
     .venv\Scripts\Activate.ps1
     ```

4. **Установите зависимости:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Запустите сервер приложения:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

После запуска сервис будет доступен по адресу: `http://localhost:8000`.

## Сборка и запуск контейнера Docker

1. **Сборка и запуск в фоновом режиме:**
   ```bash
   docker compose up --build -d
   ```

2. **Просмотр логов:**
   ```bash
   docker compose logs -f
   ```

3. **Остановка сервиса:**
   ```bash
   docker compose down
   ```

## Эндпоинты

| Метод | Путь | Описание |
| :--- | :--- | :--- |
| `GET` | `/tasks` | Получение списка всех задач (фильтрация по параметру `owner_id=<int>`) |
| `GET` | `/tasks/{task_id}` | Получение задачи по её `task_id` |
| `POST` | `/tasks` | Создание новой задачи |
| `DELETE` | `/tasks/{task_id}` | Удаление задачи по `task_id` |
