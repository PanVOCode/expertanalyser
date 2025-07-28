#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
import re
import json
import csv
from pathlib import Path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
from ai import ask_ai

def save_result_to_csv(result, filename='../results/analysis_results_all_folders.csv'):
    """Сохраняет результат анализа в CSV файл сразу после каждого канала"""
    try:
        # Проверяем, существует ли файл
        file_exists = False
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                file_exists = True
        except FileNotFoundError:
            pass
        
        # Открываем файл для записи
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['channelname', 'linktochannel', 'эксперт', 'компетенции']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            
            # Записываем заголовок, если файл новый
            if not file_exists:
                writer.writeheader()
            
            # Записываем результат
            writer.writerow(result)
            
        print(f"💾 Результат сохранен в {filename}")
        
    except Exception as e:
        print(f"❌ Ошибка при сохранении в CSV: {e}")

def extract_top_posts_from_excel(folder_path):
    """Извлекает топ-5 постов из Excel файла в папке канала"""
    try:
        # Ищем файл posts.xlsx в папке
        excel_file = folder_path / 'posts.xlsx'
        if not excel_file.exists():
            print(f"❌ Файл posts.xlsx не найден в {folder_path}")
            return ""
        
        # Читаем Excel файл
        df = pd.read_excel(excel_file)
        
        # Исключаем итоговые строки
        df = df[~df['Дата'].isin(['Итого', 'В среднем на пост'])].copy()
        
        if len(df) == 0:
            print(f"❌ Нет данных в файле {excel_file}")
            return ""
        
        # Получаем топ-5 по виральности
        top_5_posts = df.nlargest(5, 'Виральность')
        
        # Формируем текст для AI
        top_posts_text = ""
        for i, (_, row) in enumerate(top_5_posts.iterrows(), 1):
            post_text = row.get('Полный_текст', '')
            if post_text and post_text.strip():
                top_posts_text += f"текст {i}:\n{post_text.strip()}\n\n"
        
        return top_posts_text
        
    except Exception as e:
        print(f"❌ Ошибка при чтении Excel файла {folder_path}: {e}")
        return ""

def analyze_all_folders():
    """Анализирует все каналы в папке all_folders через AI"""
    
    all_folders_path = Path('../results/all_folders')
    if not all_folders_path.exists():
        print("❌ Папка all_folders не найдена!")
        return
    
    # Получаем список всех папок
    folders = [f for f in all_folders_path.iterdir() if f.is_dir()]
    print(f"Найдено {len(folders)} папок с каналами для анализа")
    
    results = []
    
    for index, folder in enumerate(folders, 1):
        channel_name = folder.name
        print(f"\n{'='*60}")
        print(f"АНАЛИЗ КАНАЛА {index}/{len(folders)}: {channel_name}")
        print(f"{'='*60}")
        
        try:
            # Извлекаем топ-5 постов из Excel файла
            print(f"📊 Читаем данные из {folder}/posts.xlsx...")
            top_posts_text = extract_top_posts_from_excel(folder)
            
            if top_posts_text:
                print(f"✅ Получено {len(top_posts_text.split('текст')) - 1} постов для анализа")
                
                # Передаем тексты в AI для анализа компетенций
                print("🤖 Анализируем компетенции через AI...")
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
                
                # Создаем результат
                result = {
                    'channelname': channel_name,
                    'linktochannel': f"https://t.me/{channel_name}",
                    'эксперт': expert,
                    'компетенции': competencies
                }
                
                # СРАЗУ сохраняем результат в CSV
                save_result_to_csv(result)
                
                # Добавляем в список для статистики
                results.append(result)
                
                print(f"✅ Анализ завершен для {channel_name}")
                print(f"Эксперт: {expert}")
                print(f"Компетенции: {competencies}")
                
            else:
                print(f"❌ Не удалось получить данные для {channel_name}")
                result = {
                    'channelname': channel_name,
                    'linktochannel': f"https://t.me/{channel_name}",
                    'эксперт': 'unknown',
                    'компетенции': 'Ошибка: не удалось получить данные'
                }
                save_result_to_csv(result)
                results.append(result)
                
        except Exception as e:
            print(f"❌ Ошибка при анализе {channel_name}: {e}")
            result = {
                'channelname': channel_name,
                'linktochannel': f"https://t.me/{channel_name}",
                'эксперт': 'unknown',
                'компетенции': f'Ошибка: {str(e)}'
            }
            save_result_to_csv(result)
            results.append(result)
        
        # Пауза между запросами
        if index < len(folders):
            print("Пауза 1.5 секунды...")
            import time
            time.sleep(1.5)
    
    # Финальная статистика
    print(f"\n{'='*60}")
    print(f"✅ АНАЛИЗ ЗАВЕРШЕН!")
    print(f"Результаты сохранены в файл: analysis_results_all_folders.csv")
    print(f"Проанализировано каналов: {len(results)}")
    
    # Статистика по экспертам
    experts = [r['эксперт'] for r in results if r['эксперт'] != 'unknown']
    true_experts = [e for e in experts if e == 'true']
    false_experts = [e for e in experts if e == 'false']
    
    print(f"Найдено экспертов: {len(true_experts)}")
    print(f"Не экспертов: {len(false_experts)}")
    print(f"{'='*60}")

if __name__ == "__main__":
    analyze_all_folders() 