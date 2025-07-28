# Telegram Channel Analyzer

Анализатор Telegram-каналов с интеграцией AI для оценки компетентности авторов.

## 1. Функционал

### Конфигурационные файлы

#### config.py - Основные настройки анализатора

```python
# Данные Telegram API
api_id = "25375051"
api_hash = "21e559fec16a53d6aa423eda559147d5"

# Период анализа (с учетом часового пояса UTC)
start_date = datetime(2025, 1, 1, tzinfo=timezone.utc)
end_date = datetime(2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

# Учитывать только текстовые сообщения в статистике
only_text = True

# Тип сортировки по умолчанию
SORT_BY_VIRALITY = 'default'  # 'default', 'coefficient', 'engagement', 'forwards', 'reactions', 'views', 'date'

# Какие виды статистики включать
stat_tables = {
    'default': True,        # Основная виральность
    'coefficient': False,   # Коэффициент виральности
    'engagement': False,    # Виральность вовлеченности
    'forwards': False,      # По пересылкам
    'reactions': False,     # По реакциям
    'views': False,         # По просмотрам
    'date': False           # По дате
}

# Создавать ли дополнительные файлы с разными типами сортировки
CREATE_MULTIPLE_SORTED_FILES = True

# Показывать ли статистику по виральности в консоли
SHOW_VIRALITY_STATISTICS = True

# Создавать ли сводный отчет по виральности
CREATE_VIRALITY_SUMMARY_REPORT = True
```

#### aiconfig.py - Настройки AI (DeepSeek через OpenRouter)

```python
# Импортируем API ключи из отдельного файла
try:
    from api_keys import get_deepseek_api_key
    DEEPSEEK_API_KEY = get_deepseek_api_key()
except ImportError:
    # Fallback если файл api_keys.py не найден
    import os
    DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', "")

# Базовый URL API OpenRouter
DEEPSEEK_BASE_URL = "https://openrouter.ai/api"

# Модель DeepSeek через OpenRouter
DEEPSEEK_MODEL = "deepseek/deepseek-chat"

# Параметры генерации
DEFAULT_MAX_TOKENS = 1000
DEFAULT_TEMPERATURE = 0.7
REQUEST_TIMEOUT = 30

# Системный промпт загружается из файла system_prompt.txt
DEFAULT_SYSTEM_PROMPT = load_system_prompt()
```

#### api_keys.py - API ключи (не отслеживается Git)

Файл содержит все API ключи для различных сервисов. **Добавлен в .gitignore для безопасности.**

```python
# Telegram API
TELEGRAM_API_ID = "ваш_telegram_api_id"
TELEGRAM_API_HASH = "ваш_telegram_api_hash"

# DeepSeek API через OpenRouter
DEEPSEEK_API_KEY = "ваш_deepseek_api_key"

# Другие API ключи...
```

**Для настройки:**
1. Скопируйте `api_keys_example.py` как `api_keys.py`
2. Заполните своими API ключами
3. Файл автоматически игнорируется Git'ом

#### system_prompt.txt - Системный промпт для AI

Файл содержит детальный промпт для оценки компетентности авторов каналов. Включает:
- Список из 41 бизнес-компетенции для оценки
- Критерии определения эксперта vs инфоцыгана
- Формат JSON-ответа
```

### Как запустить

#### 1. Анализ одного канала

```bash
python files/code/analyse.py
```

Функция `analyse(channel_url)` принимает ссылку на канал и:

- Создает папку `results/all_folders/{channel_name}/`
- Сохраняет `posts.xlsx` с данными
- Возвращает текст топ-5 постов для AI анализа

#### 2. Пакетный анализ каналов из CSV

```bash
python files/code/main.py
```

Читает `files/tgstat.csv` и для каждого канала:

- Вызывает `analyse(channel_url)`
- Отправляет топ-5 постов в AI
- Сохраняет результаты в `results/analysis_results.csv`

Формат `files/tgstat.csv`:

```csv
column1;column2;https://t.me/channel_name;column4
```

#### 3. AI анализ уже скачанных данных

```bash
python files/code/analyze_all_folders.py
```

Обрабатывает все папки в `results/all_folders/`:

- Читает `posts.xlsx` из каждой папки
- Извлекает топ-5 постов
- Отправляет в AI для анализа
- Сохраняет в `results/analysis_results_all_folders.csv`

#### 4. Тестирование AI API

```bash
python files/code/test_deepseek.py
```

Проверяет подключение к DeepSeek API через OpenRouter.

### Структура файлов

```
master/analyser/
├── files/                       # Все файлы проекта
│   ├── code/                    # Исходный код
│   │   ├── analyse.py           # Основная логика анализа
│   │   ├── ai.py                # Функции для работы с AI
│   │   ├── main.py              # Пакетный анализ из CSV
│   │   ├── analyze_all_folders.py # AI анализ существующих данных
│   │   ├── test_deepseek.py     # Тест AI API
│   │   ├── test_api_alternative.py # Альтернативный тест API
│   │   └── test_api_simple.py   # Простой тест API
│   ├── config/                  # Конфигурационные файлы
│   │   ├── config.py            # Основные настройки анализа
│   │   ├── aiconfig.py          # Настройки AI
│   │   ├── api_keys.py          # API ключи (не отслеживается Git)
│   │   ├── api_keys_example.py  # Пример файла API ключей
│   │   └── system_prompt.txt    # Системный промпт для AI
│   ├── docs/                    # Документация
│   │   ├── API_SETUP.md         # Настройка API
│   │   └── SETUP.md             # Инструкции по настройке
│   └── tgstat.csv               # Список каналов для анализа
├── results/                     # Результаты анализа
│   ├── all_folders/             # Папка с результатами анализа каналов
│   │   ├── channel1/
│   │   │   ├── posts.xlsx
│   │   │   ├── posts_sorted_by_*.xlsx
│   │   │   └── virality_summary_report.xlsx
│   │   └── channel2/
│   ├── analysis_results.csv     # Результаты AI анализа
│   ├── analysis_results_all_folders.csv # Результаты AI анализа существующих данных
│   └── *.xlsx                   # Дополнительные отчеты
├── README.md                    # Основная документация
├── QUICK_START.md               # Быстрый старт
└── .gitignore                   # Игнорируемые файлы
```

## 2. Описание формул расчета и логики приложения

### Метрики виральности

#### 1. ER% (Engagement Rate)

```
ER% = (Реакции + Комментарии + Пересылки) / Просмотры × 100
```

#### 2. Основная виральность

```
Виральность = log1p(Просмотры) × log1p(Реакции + Комментарии + Пересылки) × ER%
```

#### 3. Коэффициент виральности

```
Коэффициент виральности = (Реакции + Комментарии + Пересылки) / log1p(Просмотры)
```

#### 4. Виральность вовлеченности

```
Виральность вовлеченности = log1p(Реакции + Комментарии + Пересылки) × ER%
```

### Логика работы приложения

#### Этап 1: Получение данных из Telegram

1. **Подключение к API**: Использует Telethon для подключения к Telegram API
2. **Извлечение username**: Извлекает имя канала из URL (например, из `https://t.me/sellerx` получает `sellerx`)
3. **Получение сообщений**: Итерируется по сообщениям в указанном временном диапазоне
4. **Сбор метрик**:
   - Просмотры (`views_count`)
   - Реакции (положительные и отрицательные)
   - Комментарии (`comments_count`)
   - Пересылки (`forwards_count`)

#### Этап 2: Обработка данных

1. **Фильтрация**: Если `only_text = True`, оставляет только текстовые сообщения
2. **Типизация**: Приводит числовые столбцы к типу `float`
3. **Расчет метрик**: Вычисляет все виды виральности
4. **Сортировка**: Сортирует по выбранному типу виральности
5. **Добавление итогов**: Добавляет строки "Итого" и "В среднем на пост"

#### Этап 3: Сохранение результатов

1. **Создание папки**: `all_folders/{channel_name}/`
2. **Основной файл**: `posts.xlsx` с полными данными
3. **Дополнительные файлы**: Если `CREATE_MULTIPLE_SORTED_FILES = True`
   - `posts_sorted_by_default.xlsx`
   - `posts_sorted_by_coefficient.xlsx`
   - `posts_sorted_by_engagement.xlsx`
   - и т.д.
4. **Сводный отчет**: Если `CREATE_VIRALITY_SUMMARY_REPORT = True`
   - `virality_summary_report.xlsx`

#### Этап 4: AI анализ (опционально)

1. **Извлечение топ-5 постов**: Берет 5 самых вирусных постов
2. **Форматирование**: Создает текст в формате:
   ```
   текст 1:
   [содержание поста]

   текст 2:
   [содержание поста]
   ...
   ```
3. **Отправка в AI**: Использует DeepSeek через OpenRouter
4. **Парсинг ответа**: Извлекает JSON с полями `эксперт` и `компетенции`
5. **Сохранение**: Записывает в CSV файл

### Типы сортировки

- **default**: По основной виральности
- **coefficient**: По коэффициенту виральности
- **engagement**: По виральности вовлеченности
- **forwards**: По количеству пересылок
- **reactions**: По количеству реакций
- **views**: По количеству просмотров
- **date**: По дате публикации

### Обработка ошибок

1. **API ошибки**: Обрабатываются через `try-except`
2. **Отсутствие данных**: Возвращается пустая строка
3. **Некорректные ссылки**: Проверяется формат URL
4. **Сетевые ошибки**: Таймауты и повторные попытки
5. **JSON парсинг**: Fallback на сохранение сырого ответа AI

### Особенности реализации

1. **Часовые пояса**: Все даты обрабатываются в UTC
2. **Реакции**: Поддержка как новых, так и старых версий Telethon
3. **Инкрементальное сохранение**: Результаты сохраняются сразу после каждого канала
4. **Паузы**: 1.5 секунды между запросами для соблюдения лимитов API
5. **Лимиты**: Максимум 1000 каналов за один запуск
