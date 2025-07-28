import requests
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
from aiconfig import (
    DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL,
    DEFAULT_MAX_TOKENS, DEFAULT_TEMPERATURE, DEFAULT_SYSTEM_PROMPT,
    REQUEST_TIMEOUT
)

def test_deepseek_api():
    """
    Простая функция для тестирования DeepSeek API через OpenRouter
    """
    print("Тестирование DeepSeek API через OpenRouter...")
    print(f"API Key: {DEEPSEEK_API_KEY[:10]}..." if DEEPSEEK_API_KEY else "API Key не найден")
    print(f"Base URL: {DEEPSEEK_BASE_URL}")
    print(f"Model: {DEEPSEEK_MODEL}")
    
    if not DEEPSEEK_API_KEY:
        print("❌ Ошибка: API ключ не указан в aiconfig.py")
        return False
    
    # Простой тестовый запрос
    test_message = "Привет! Как дела?"
    
    # Формируем сообщения для API
    messages = []
    
    if DEFAULT_SYSTEM_PROMPT:
        messages.append({
            "role": "system",
            "content": "Ты - полезный ассистент. Отвечай кратко и по делу."
        })
    
    messages.append({
        "role": "user",
        "content": test_message
    })
    
    # Параметры запроса
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
        "max_tokens": 100,  # Уменьшаем для теста
        "temperature": 0.7,
        "stream": False
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "HTTP-Referer": "https://github.com/your-repo",  # OpenRouter требует HTTP-Referer
        "X-Title": "Telegram Channel Analyzer",  # Опционально для OpenRouter
        "User-Agent": "Telegram-Channel-Analyzer/1.0",  # Добавляем User-Agent
        "Accept": "application/json"  # Явно указываем Accept
    }
    
    try:
        print(f"\nОтправляем запрос к {DEEPSEEK_BASE_URL}/v1/chat/completions")
        print(f"Тестовое сообщение: {test_message}")
        
        response = requests.post(
            f"{DEEPSEEK_BASE_URL}/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # Извлекаем ответ из результата
            ai_response = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            if ai_response:
                print(f"✅ API работает! Ответ: {ai_response}")
                return True
            else:
                print("❌ Получен пустой ответ от AI")
                return False
        else:
            print(f"❌ Ошибка HTTP: {response.status_code}")
            print(f"Ответ сервера: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка запроса: {str(e)}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Ошибка парсинга JSON: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_deepseek_api()
    if success:
        print("\n🎉 API DeepSeek через OpenRouter работает корректно!")
    else:
        print("\n💥 API DeepSeek через OpenRouter не работает. Проверьте настройки в aiconfig.py") 