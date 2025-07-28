# Конфигурация для DeepSeek API через OpenRouter

import os

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

# Параметры генерации по умолчанию
DEFAULT_MAX_TOKENS = 1000
DEFAULT_TEMPERATURE = 0.7

# Системный промпт по умолчанию (загружается из файла)
def load_system_prompt():
    """Загружает системный промпт из файла system_prompt.txt"""
    try:
        # Ищем файл в текущей директории (config/)
        prompt_path = os.path.join(os.path.dirname(__file__), 'system_prompt.txt')
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("⚠️ Файл system_prompt.txt не найден. Используется пустой промпт.")
        return ""
    except Exception as e:
        print(f"⚠️ Ошибка при чтении system_prompt.txt: {e}. Используется пустой промпт.")
        return ""

DEFAULT_SYSTEM_PROMPT = load_system_prompt()


# Таймаут запроса в секундах
REQUEST_TIMEOUT = 30 