# Конфигурация для DeepSeek API через OpenRouter

# API ключ для OpenRouter (DeepSeek)
DEEPSEEK_API_KEY = "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" 

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
        with open('system_prompt.txt', 'r', encoding='utf-8') as f:
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