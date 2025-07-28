# Telegram Channel Analyzer - Виральность

Анализатор каналов Telegram с расширенными возможностями сортировки по виральности.

## Работа с конфигурационным файлом (`config.py`)

Вся настройка анализа производится в файле `config.py`. Вот основные параметры:

### 1. Данные Telegram API
```python
api_id = "..."
api_hash = "..."
```
Получить можно на [my.telegram.org](https://my.telegram.org/).

### 2. Период анализа
```python
from datetime import datetime
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31, 23, 59, 59)
```

### 3. Фильтрация только текстовых сообщений
```python
only_text = True  # True — анализируются только текстовые сообщения, False — все типы
```

### 4. Тип сортировки по умолчанию
```python
SORT_BY_VIRALITY = 'default'  # варианты: 'default', 'coefficient', 'engagement', 'forwards', 'reactions', 'views', 'date'
```

### 5. Виды статистики для вывода и отчетов
```python
stat_tables = {
    'default': True,        # Основная виральность
    'coefficient': False,   # Коэффициент виральности
    'engagement': False,    # Виральность вовлеченности
    'forwards': False,      # По пересылкам
    'reactions': False,     # По реакциям
    'views': False,         # По просмотрам
    'date': False           # По дате
}
```
Только те виды, где `True`, будут выводиться в консоли и сохраняться в отдельные файлы.

### 6. Флаги создания файлов и отчетов
```python
CREATE_MULTIPLE_SORTED_FILES = True  # Создавать ли дополнительные файлы с разными сортировками
SHOW_VIRALITY_STATISTICS = True      # Показывать ли статистику в консоли
CREATE_VIRALITY_SUMMARY_REPORT = True # Создавать ли сводный отчет
```

---

## Использование

1. Откройте и настройте `config.py` под свои задачи.
2. Импортируйте и вызовите функцию:
```python
from main import analyse
analyse("https://t.me/sellerx")
```
3. Все результаты будут сохранены в папку с названием канала (например, `sellerx/`).

---

## Остальные возможности и формулы см. ниже в оригинальной документации. 