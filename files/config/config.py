# Конфигурация анализатора

# Импортируем API ключи из отдельного файла
try:
    from api_keys import get_telegram_api_id, get_telegram_api_hash
    api_id = get_telegram_api_id()
    api_hash = get_telegram_api_hash()
except ImportError:
    # Fallback если файл api_keys.py не найден
    import os
    api_id = os.getenv('TELEGRAM_API_ID', "25375051")
    api_hash = os.getenv('TELEGRAM_API_HASH', "21e559fec16a53d6aa423eda559147d5")

# Период анализа
from datetime import datetime, timezone
start_date = datetime(2025, 1, 1, tzinfo=timezone.utc)
end_date = datetime(2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

# Учитывать только текстовые сообщения в статистике
only_text = False

# Тип сортировки по умолчанию
# Доступные варианты: 'default', 'coefficient', 'engagement', 'forwards', 'reactions', 'views', 'date'
SORT_BY_VIRALITY = 'default'

# Какие виды статистики включать (True - включать, False - не включать)
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