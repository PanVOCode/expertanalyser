#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
from aiconfig import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL

def test_api_simple():
    """Простой тест API для диагностики"""
    
    print("🔍 Диагностика API...")
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
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "HTTP-Referer": "https://github.com/your-repo",
        "X-Title": "Telegram Channel Analyzer"
    }
    
    print(f"\n📤 Отправляем запрос к {DEEPSEEK_BASE_URL}/v1/chat/completions")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(
            f"{DEEPSEEK_BASE_URL}/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"\n📥 Статус ответа: {response.status_code}")
        print(f"Заголовки ответа: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Успех! Ответ: {result}")
            return True
        else:
            print(f"❌ Ошибка {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"💥 Исключение: {e}")
        return False

if __name__ == "__main__":
    success = test_api_simple()
    if success:
        print("\n🎉 API работает!")
    else:
        print("\n�� API не работает!") 