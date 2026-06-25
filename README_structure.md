```
/nve-rsync-host-monitor/
│
├── app/
│   ├── __init__.py              # Инициализация Python пакета
│   ├── main.py                  # FastAPI приложение (основной файл)
│   ├── models.py                # SQLAlchemy модели БД
│   ├── database.py              # Подключение к SQLite
│   ├── schemas.py               # Pydantic схемы для API
│   ├── crud.py                  # Операции с БД
│   ├── config.py                # Конфигурация приложения
│   └── templates/               # HTML шаблоны
│       ├── index.html           # Главная страница (таблица)
│       └── chart.html           # Страница с графиком
├── static/                      # Статические файлы
│   ├── css/                     # Файлы Cascade Style Sheets (CSS) стилей
│   │   └── style.css
│   └── js/                      # Файлы JavaScript логики
│       └── scripts.js
├── data/                        # Каталог с локальными данными
│   └── monitoring.db            # Файл БД SQLite
├── logs/                        # Логи
│   └── sync.log                 # Лог в который записываются события полной синхронизации отдельного каталога
├── venv/                        # Виртуальное окружение Python
├── requirements.txt             # Конфигурация зависимостей Python проекта
├── run.sh                       # Скрипт запуска сервера
├── install.sh                   # Скрипт установки
├── monitoring.service           # systemd сервис (для автозапуска)
├── cron.job                     # Конфигурация для планировщика Cron задач по расписанию 
└── README.md                    # Инструкция по развертыванию
```
