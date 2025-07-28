import os
import sys
import pandas as pd
import time
from telethon.sync import TelegramClient
from telethon.tl.types import ReactionEmoji, ReactionPaid, ReactionCustomEmoji, MessageMediaPhoto
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Alignment
from datetime import datetime
import numpy as np
import csv
import json
import re

# Добавляем пути для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
sys.path.append(os.path.dirname(__file__))

# Импортируем конфигурацию
from config import (
    only_text, stat_tables, api_id, api_hash, start_date, end_date, SORT_BY_VIRALITY,
    CREATE_MULTIPLE_SORTED_FILES, SHOW_VIRALITY_STATISTICS, CREATE_VIRALITY_SUMMARY_REPORT
)

# Импортируем наши модули
from analyse import analyse
from ai import ask_ai

if __name__ == "__main__":
    # Читаем список каналов из tgstat.csv
    try:
        # Пробуем разные разделители
        try:
            channels_df = pd.read_csv('files/tgstat.csv', sep=';', encoding='utf-8')
        except:
            try:
                channels_df = pd.read_csv('files/tgstat.csv', sep=',', encoding='utf-8')
            except:
                channels_df = pd.read_csv('files/tgstat.csv', sep='\t', encoding='utf-8')
        
        print(f"Найдено {len(channels_df)} каналов для анализа")
    except FileNotFoundError:
        print("Файл files/tgstat.csv не найден!")
        exit(1)
    except Exception as e:
        print(f"Ошибка при чтении tgstat.csv: {e}")
        print("Проверьте формат файла. Поддерживаемые разделители: ; , tab")
        exit(1)
    
    # Определяем столбец с ссылками на каналы
    # Сначала проверяем третий столбец (индекс 2), так как ссылки обычно там
    if len(channels_df.columns) >= 3:
        link_column = channels_df.columns[2]
        print(f"Используем третий столбец: {link_column}")
    else:
        # Если столбцов меньше 3, ищем по названию
        link_column = None
        for col in channels_df.columns:
            if 'link' in col.lower() or 'channel' in col.lower() or 'url' in col.lower() or 't.me' in col.lower():
                link_column = col
                break
        
        if not link_column:
            print("Не найден столбец со ссылками на каналы в tgstat.csv")
            print(f"Доступные столбцы: {list(channels_df.columns)}")
            exit(1)
    
    print(f"Используем столбец: {link_column}")
    
    # Создаем список для результатов
    results = []
    
    # Анализируем каждый канал
    for index, row in channels_df.iterrows():
        channel_url = row[link_column]
        
        # Пропускаем пустые ссылки
        if pd.isna(channel_url) or not str(channel_url).strip():
            print(f"Пропускаем канал {index + 1}: пустая ссылка")
            continue
        
        print(f"\n{'='*60}")
        print(f"АНАЛИЗ КАНАЛА {index + 1}/{len(channels_df)}: {channel_url}")
        print(f"{'='*60}")
        
        try:
            # Анализируем канал и получаем тексты топ-5 постов
            top_posts_text = analyse(channel_url)
            
            if top_posts_text:
                print(f"Получено {len(top_posts_text.split('текст')) - 1} постов для анализа")
                
                # Передаем тексты в AI для анализа компетенций
                print("Анализируем компетенции через AI...")
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
                
                # Извлекаем имя канала из URL
                channel_name = ""
                try:
                    match = re.search(r"(?:https?://)?t\.me/(.+?)(?:/|$)", channel_url)
                    if match:
                        channel_name = match.group(1).replace('@', '')
                except:
                    channel_name = "unknown"
                
                # Сохраняем результат
                results.append({
                    'channelname': channel_name,
                    'linktochannel': channel_url,
                    'эксперт': expert,
                    'компетенции': competencies
                })
                
                print(f"✅ Анализ завершен для {channel_url}")
                print(f"Канал: {channel_name}")
                print(f"Эксперт: {expert}")
                print(f"Компетенции: {competencies}")
                
            else:
                print(f"❌ Не удалось получить данные для {channel_url}")
                results.append({
                    'channelname': "unknown",
                    'linktochannel': channel_url,
                    'эксперт': 'unknown',
                    'компетенции': 'Ошибка: не удалось получить данные'
                })
                
        except Exception as e:
            print(f"❌ Ошибка при анализе {channel_url}: {e}")
            results.append({
                'channelname': "unknown",
                'linktochannel': channel_url,
                'эксперт': 'unknown',
                'компетенции': f'Ошибка: {str(e)}'
            })
        
        # Пауза между запросами, чтобы не перегружать API
        if index < len(channels_df) - 1:  # Не делаем паузу после последнего канала
            print("Пауза 1.5 секунды...")
            time.sleep(1.5)
        
        # Ограничиваем анализ 1000 каналами
        if index >= 999:  # 0-based indexing, поэтому 999 = 1000-й канал
            print("🔍 Достигнуто ограничение в 1000 каналов. Останавливаемся.")
            break
    
    # Сохраняем результаты в CSV файл
    output_filename = '../results/analysis_results.csv'
    try:
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['channelname', 'linktochannel', 'эксперт', 'компетенции']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            
            writer.writeheader()
            for result in results:
                writer.writerow(result)
        
        print(f"\n{'='*60}")
        print(f"✅ АНАЛИЗ ЗАВЕРШЕН!")
        print(f"Результаты сохранены в файл: {output_filename}")
        print(f"Проанализировано каналов: {len(results)}")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"❌ Ошибка при сохранении результатов: {e}")
        # Выводим результаты в консоль как резервный вариант
        print("\nРЕЗУЛЬТАТЫ АНАЛИЗА:")
        for result in results:
            print(f"{result['channelname']};{result['linktochannel']};{result['эксперт']};{result['компетенции']}")
