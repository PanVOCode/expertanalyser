#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
from aiconfig import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL

def test_api_alternative():
    """Альтернативный тест API с разными методами аутентификации"""
    
    print("🔍 Альтернативная диагностика API...")
    print(f"API Key: {DEEPSEEK_API_KEY[:20]}...")
    print(f"Base URL: {DEEPSEEK_BASE_URL}")
    print(f"Model: {DEEPSEEK_MODEL}")
    
    # Простой запрос
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "user", "content": "Привет! Ответь одним словом: работает"}
        ],
        "max_tokens": 10,
        "temperature": 0.7
    }
    
    # Вариант 1: Стандартные заголовки
    headers1 = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "HTTP-Referer": "https://github.com/your-repo",
        "X-Title": "Telegram Channel Analyzer"
    }
    
    # Вариант 2: С дополнительными заголовками
    headers2 = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "HTTP-Referer": "https://github.com/your-repo",
        "X-Title": "Telegram Channel Analyzer",
        "User-Agent": "Telegram-Channel-Analyzer/1.0",
        "Accept": "application/json"
    }
    
    # Вариант 3: Без HTTP-Referer
    headers3 = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "X-Title": "Telegram Channel Analyzer"
    }
    
    # Вариант 4: Минимальные заголовки
    headers4 = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    
    headers_list = [
        ("Вариант 1: Стандартные заголовки", headers1),
        ("Вариант 2: С дополнительными заголовками", headers2),
        ("Вариант 3: Без HTTP-Referer", headers3),
        ("Вариант 4: Минимальные заголовки", headers4)
    ]
    
    for name, headers in headers_list:
        print(f"\n{'='*50}")
        print(f"Тестируем: {name}")
        print(f"Заголовки: {json.dumps(headers, indent=2)}")
        
        try:
            response = requests.post(
                f"{DEEPSEEK_BASE_URL}/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            print(f"Статус ответа: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ УСПЕХ! Ответ: {result}")
                return True
            else:
                print(f"❌ Ошибка {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"💥 Исключение: {e}")
    
    return False

if __name__ == "__main__":
    success = test_api_alternative()
    if success:
        print("\n🎉 API работает с одним из вариантов!")
    else:
        print("\n💥 API не работает ни с одним вариантом!")
        print("\n🔧 Рекомендации:")
        print("1. Проверьте, не истек ли API ключ")
        print("2. Убедитесь, что ключ действителен для OpenRouter")
        print("3. Попробуйте создать новый API ключ на openrouter.ai") 