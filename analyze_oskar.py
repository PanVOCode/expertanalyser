#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from analyse import analyse
from ai import ask_ai
import re
import json

def analyze_oskar_channel():
    """Анализирует канал Оскара Хартманна"""
    
    channel_url = "https://t.me/Oskar_Hartmann"
    
    print("="*60)
    print("АНАЛИЗ КАНАЛА: Оскар Хартманн")
    print("="*60)
    
    try:
        # Анализируем канал и получаем тексты топ-5 постов
        print("📊 Получаем данные канала...")
        top_posts_text = analyse(channel_url)
        
        if top_posts_text:
            print(f"✅ Получено {len(top_posts_text.split('текст')) - 1} постов для анализа")
            print("\n" + "="*50)
            print("ТОП-5 ПОСТОВ ПО ВИРАЛЬНОСТИ:")
            print("="*50)
            print(top_posts_text)
            
            # Передаем тексты в AI для анализа компетенций
            print("\n🤖 Анализируем компетенции через AI...")
            ai_analysis = ask_ai(top_posts_text)
            
            # Парсим JSON ответ от AI
            expert = "unknown"
            competencies = []
            
            try:
                # Ищем JSON в ответе AI
                json_match = re.search(r'\{.*\}', ai_analysis, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    ai_data = json.loads(json_str)
                    
                    expert = str(ai_data.get('эксперт', 'unknown')).lower()
                    competencies = ai_data.get('компетенции', [])
                    
                    if isinstance(competencies, list):
                        competencies = ', '.join(competencies)
                    else:
                        competencies = str(competencies)
                else:
                    print(f"Не удалось найти JSON в ответе AI: {ai_analysis}")
                    competencies = ai_analysis
                    
            except json.JSONDecodeError as e:
                print(f"Ошибка парсинга JSON: {e}")
                print(f"Ответ AI: {ai_analysis}")
                competencies = ai_analysis
            
            print("\n" + "="*50)
            print("РЕЗУЛЬТАТЫ AI АНАЛИЗА:")
            print("="*50)
            print(f"Эксперт: {expert}")
            print(f"Компетенции: {competencies}")
            
        else:
            print("❌ Не удалось получить данные для канала")
            
    except Exception as e:
        print(f"❌ Ошибка при анализе канала: {e}")

if __name__ == "__main__":
    analyze_oskar_channel() 