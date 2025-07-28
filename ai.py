import requests
import json
from aiconfig import (
    DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL,
    DEFAULT_MAX_TOKENS, DEFAULT_TEMPERATURE, DEFAULT_SYSTEM_PROMPT,
    REQUEST_TIMEOUT
)

def ask_ai(text: str) -> str:
    """
    Простая функция для запроса к DeepSeek API через OpenRouter
    
    Args:
        text (str): Текст запроса
        
    Returns:
        str: Ответ от AI или сообщение об ошибке
    """
    if not DEEPSEEK_API_KEY:
        return "Ошибка: API ключ не указан в aiconfig.py"
    
    # Формируем сообщения для API
    messages = []
    
    if DEFAULT_SYSTEM_PROMPT:
        messages.append({
            "role": "system",
            "content": DEFAULT_SYSTEM_PROMPT
        })
    
    messages.append({
        "role": "user",
        "content": text
    })
    
    # Параметры запроса для OpenRouter
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
        "max_tokens": DEFAULT_MAX_TOKENS,
        "temperature": DEFAULT_TEMPERATURE,
        "stream": False
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "HTTP-Referer": "https://github.com/your-repo",  # OpenRouter требует HTTP-Referer
        "X-Title": "Telegram Channel Analyzer"  # Опционально для OpenRouter
    }
    
    try:
        response = requests.post(
            f"{DEEPSEEK_BASE_URL}/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT
        )
        
        response.raise_for_status()
        
        result = response.json()
        
        # Извлекаем ответ из результата
        ai_response = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        if ai_response:
            return ai_response
        else:
            return "Ошибка: Пустой ответ от AI"
            
    except requests.exceptions.RequestException as e:
        return f"Ошибка запроса: {str(e)}"
    except json.JSONDecodeError as e:
        return f"Ошибка парсинга JSON: {str(e)}"
    except Exception as e:
        return f"Неожиданная ошибка: {str(e)}"

if __name__ == "__main__":
    # Пример использования
    # response = ask_ai("Привет! Как дела?")
    # print(response)
    pass 