# Быстрый старт

## Новая структура проекта

Проект реорганизован для лучшей организации:

```
master/analyser/
├── files/                       # Все файлы проекта
│   ├── code/                    # Исходный код
│   ├── config/                  # Конфигурационные файлы
│   ├── docs/                    # Документация
│   └── tgstat.csv               # Список каналов для анализа
├── results/                     # Результаты анализа
├── README.md                    # Основная документация
└── .gitignore                   # Игнорируемые файлы
```

## Быстрая настройка

### 1. Настройка API ключей

```bash
# Скопируйте пример файла
cp files/config/api_keys_example.py files/config/api_keys.py

# Отредактируйте files/config/api_keys.py и добавьте свои ключи
```

### 2. Запуск

```bash
# Анализ одного канала
python files/code/analyse.py

# Пакетный анализ из CSV
python files/code/main.py

# AI анализ существующих данных
python files/code/analyze_all_folders.py

# Тест AI API
python files/code/test_deepseek.py
```

## Основные файлы

- **`files/code/analyse.py`** - Основная логика анализа
- **`files/code/main.py`** - Пакетный анализ каналов
- **`files/config/config.py`** - Настройки анализа
- **`files/config/aiconfig.py`** - Настройки AI
- **`files/config/api_keys.py`** - API ключи (не в Git)
- **`files/docs/SETUP.md`** - Подробная настройка
- **`files/docs/API_SETUP.md`** - Настройка API

## Безопасность

- ✅ API ключи в `files/config/api_keys.py` игнорируются Git'ом
- ✅ Поддержка переменных окружения
- ✅ Пример файла без реальных ключей

## Подробная документация

- **`README.md`** - Полное описание проекта
- **`files/docs/SETUP.md`** - Инструкции по настройке
- **`files/docs/API_SETUP.md`** - Настройка API ключей 