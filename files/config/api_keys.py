# API ключи для всех сервисов
# ⚠️ ВНИМАНИЕ: Этот файл добавлен в .gitignore для безопасности
# Не публикуйте реальные API ключи в публичных репозиториях!

# Telegram API (получить на https://my.telegram.org/)
TELEGRAM_API_ID = "25375051"
TELEGRAM_API_HASH = "21e559fec16a53d6aa423eda559147d5"

# DeepSeek API через OpenRouter (получить на https://openrouter.ai)
DEEPSEEK_API_KEY = "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"

# Альтернативные API ключи (закомментированы, раскомментируйте при необходимости)

# OpenAI API (получить на https://platform.openai.com/)
# OPENAI_API_KEY = "sk-..."

# Anthropic Claude API (получить на https://console.anthropic.com/)
# ANTHROPIC_API_KEY = "sk-ant-..."

# Google Gemini API (получить на https://makersuite.google.com/)
# GEMINI_API_KEY = "AIza..."

# Hugging Face API (получить на https://huggingface.co/settings/tokens)
# HUGGINGFACE_API_KEY = "hf_..."

# Cohere API (получить на https://cohere.ai/)
# COHERE_API_KEY = "..."

# Mistral AI API (получить на https://console.mistral.ai/)
# MISTRAL_API_KEY = "..."

# Perplexity API (получить на https://www.perplexity.ai/)
# PERPLEXITY_API_KEY = "pplx-..."

# Ollama (локальный API, не требует ключа)
# OLLAMA_BASE_URL = "http://localhost:11434"

# Функция для получения API ключа с приоритетом переменных окружения
import os

def get_api_key(key_name: str, default_value: str = "") -> str:
    """
    Получает API ключ с приоритетом переменных окружения
    
    Args:
        key_name (str): Имя переменной окружения
        default_value (str): Значение по умолчанию из файла
        
    Returns:
        str: API ключ
    """
    return os.getenv(key_name, default_value)

# Функции для получения конкретных API ключей
def get_telegram_api_id() -> str:
    return get_api_key('TELEGRAM_API_ID', TELEGRAM_API_ID)

def get_telegram_api_hash() -> str:
    return get_api_key('TELEGRAM_API_HASH', TELEGRAM_API_HASH)

def get_deepseek_api_key() -> str:
    return get_api_key('DEEPSEEK_API_KEY', DEEPSEEK_API_KEY)

def get_openai_api_key() -> str:
    return get_api_key('OPENAI_API_KEY', '')

def get_anthropic_api_key() -> str:
    return get_api_key('ANTHROPIC_API_KEY', '')

def get_gemini_api_key() -> str:
    return get_api_key('GEMINI_API_KEY', '')

def get_huggingface_api_key() -> str:
    return get_api_key('HUGGINGFACE_API_KEY', '')

def get_cohere_api_key() -> str:
    return get_api_key('COHERE_API_KEY', '')

def get_mistral_api_key() -> str:
    return get_api_key('MISTRAL_API_KEY', '')

def get_perplexity_api_key() -> str:
    return get_api_key('PERPLEXITY_API_KEY', '')

def get_ollama_base_url() -> str:
    return get_api_key('OLLAMA_BASE_URL', 'http://localhost:11434') 