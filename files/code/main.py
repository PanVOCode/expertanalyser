import os
import sys
import pandas as pd
import time
import tempfile
import shutil
from telethon.sync import TelegramClient
from telethon.tl.types import ReactionEmoji, ReactionPaid, ReactionCustomEmoji, MessageMediaPhoto
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Alignment
from datetime import datetime
import numpy as np
import csv
import json
import re
import signal
import atexit

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

class AnalysisManager:
    """Менеджер анализа с защитой от потери данных"""
    
    def __init__(self, checkpoint_file='../results/analysis_checkpoint.json', 
                 results_file='../results/analysis_results.csv',
                 temp_results_file='../results/analysis_results_temp.csv'):
        self.checkpoint_file = checkpoint_file
        self.results_file = results_file
        self.temp_results_file = temp_results_file
        self.results = []
        self.current_index = 0
        self.total_channels = 0
        self.start_time = datetime.now()
        
        # Создаем папку results если её нет
        os.makedirs(os.path.dirname(self.results_file), exist_ok=True)
        
        # Регистрируем обработчики для graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        atexit.register(self._cleanup)
        
        # Загружаем предыдущий прогресс если есть
        self._load_checkpoint()
    
    def _signal_handler(self, signum, frame):
        """Обработчик сигналов для graceful shutdown"""
        print(f"\n⚠️ Получен сигнал {signum}. Сохраняем прогресс...")
        self._save_checkpoint()
        self._save_results()
        print("✅ Прогресс сохранен. Можно продолжить анализ позже.")
        sys.exit(0)
    
    def _cleanup(self):
        """Очистка при завершении программы"""
        try:
            self._save_checkpoint()
            self._save_results()
        except:
            pass
    
    def _load_checkpoint(self):
        """Загружает checkpoint с предыдущего запуска"""
        try:
            if os.path.exists(self.checkpoint_file):
                with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                    checkpoint = json.load(f)
                
                self.current_index = checkpoint.get('current_index', 0)
                self.results = checkpoint.get('results', [])
                self.total_channels = checkpoint.get('total_channels', 0)
                self.start_time = datetime.fromisoformat(checkpoint.get('start_time', datetime.now().isoformat()))
                
                print(f"📂 Загружен checkpoint: {len(self.results)} каналов уже проанализировано")
                print(f"🔄 Продолжаем с канала {self.current_index + 1}")
                return True
        except Exception as e:
            print(f"⚠️ Ошибка загрузки checkpoint: {e}")
        
        return False
    
    def _save_checkpoint(self):
        """Сохраняет текущий прогресс в checkpoint"""
        try:
            checkpoint = {
                'current_index': self.current_index,
                'results': self.results,
                'total_channels': self.total_channels,
                'start_time': self.start_time.isoformat(),
                'last_save': datetime.now().isoformat()
            }
            
            # Сначала сохраняем во временный файл
            temp_checkpoint = self.checkpoint_file + '.tmp'
            with open(temp_checkpoint, 'w', encoding='utf-8') as f:
                json.dump(checkpoint, f, indent=2, ensure_ascii=False)
            
            # Атомарно переименовываем
            if os.path.exists(self.checkpoint_file):
                os.remove(self.checkpoint_file)
            os.rename(temp_checkpoint, self.checkpoint_file)
            
        except Exception as e:
            print(f"⚠️ Ошибка сохранения checkpoint: {e}")
    
    def _save_results(self):
        """Сохраняет результаты во временный файл"""
        try:
            with open(self.temp_results_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['channelname', 'linktochannel', 'эксперт', 'компетенции']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
                
                writer.writeheader()
                for result in self.results:
                    writer.writerow(result)
            
            # Атомарно переименовываем временный файл в основной
            if os.path.exists(self.results_file):
                backup_file = self.results_file + '.backup'
                shutil.copy2(self.results_file, backup_file)
                print(f"💾 Создан backup: {backup_file}")
            
            shutil.move(self.temp_results_file, self.results_file)
            
        except Exception as e:
            print(f"⚠️ Ошибка сохранения результатов: {e}")
    
    def _save_intermediate_results(self):
        """Сохраняет промежуточные результаты"""
        self._save_checkpoint()
        self._save_results()
        print(f"💾 Промежуточное сохранение: {len(self.results)} каналов")
    
    def analyze_channel(self, channel_url, channel_index):
        """Анализирует один канал с обработкой ошибок"""
        try:
            print(f"\n{'='*60}")
            print(f"АНАЛИЗ КАНАЛА {channel_index + 1}/{self.total_channels}: {channel_url}")
            print(f"{'='*60}")
            
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
                
                result = {
                    'channelname': channel_name,
                    'linktochannel': channel_url,
                    'эксперт': expert,
                    'компетенции': competencies
                }
                
                print(f"✅ Анализ завершен для {channel_url}")
                print(f"Канал: {channel_name}")
                print(f"Эксперт: {expert}")
                print(f"Компетенции: {competencies}")
                
                return result
                
            else:
                print(f"❌ Не удалось получить данные для {channel_url}")
                return {
                    'channelname': "unknown",
                    'linktochannel': channel_url,
                    'эксперт': 'unknown',
                    'компетенции': 'Ошибка: не удалось получить данные'
                }
                
        except Exception as e:
            print(f"❌ Ошибка при анализе {channel_url}: {e}")
            return {
                'channelname': "unknown",
                'linktochannel': channel_url,
                'эксперт': 'unknown',
                'компетенции': f'Ошибка: {str(e)}'
            }
    
    def run_analysis(self, channels_df, link_column):
        """Запускает анализ всех каналов с защитой от потери данных"""
        self.total_channels = len(channels_df)
        
        print(f"🚀 Запуск анализа {self.total_channels} каналов")
        print(f"📊 Уже проанализировано: {len(self.results)} каналов")
        print(f"🔄 Начинаем с канала: {self.current_index + 1}")
        
        # Анализируем каждый канал
        for index in range(self.current_index, len(channels_df)):
            row = channels_df.iloc[index]
            channel_url = row[link_column]
            
            # Пропускаем пустые ссылки
            if pd.isna(channel_url) or not str(channel_url).strip():
                print(f"Пропускаем канал {index + 1}: пустая ссылка")
                self.current_index = index + 1
                continue
            
            # Анализируем канал
            result = self.analyze_channel(channel_url, index)
            self.results.append(result)
            self.current_index = index + 1
            
            # Сохраняем промежуточные результаты каждые 10 каналов
            if len(self.results) % 10 == 0:
                self._save_intermediate_results()
            
            # Пауза между запросами, чтобы не перегружать API
            if index < len(channels_df) - 1:  # Не делаем паузу после последнего канала
                print("Пауза 1.5 секунды...")
                time.sleep(1.5)
            
            # Ограничиваем анализ 1000 каналами
            if index >= 999:  # 0-based indexing, поэтому 999 = 1000-й канал
                print("🔍 Достигнуто ограничение в 1000 каналов. Останавливаемся.")
                break
        
        # Финальное сохранение
        self._save_intermediate_results()
        
        # Выводим статистику
        elapsed_time = datetime.now() - self.start_time
        print(f"\n{'='*60}")
        print(f"✅ АНАЛИЗ ЗАВЕРШЕН!")
        print(f"Результаты сохранены в файл: {self.results_file}")
        print(f"Проанализировано каналов: {len(self.results)}")
        print(f"Время выполнения: {elapsed_time}")
        print(f"Среднее время на канал: {elapsed_time / len(self.results) if self.results else 0}")
        print(f"{'='*60}")
        
        # Удаляем checkpoint после успешного завершения
        if os.path.exists(self.checkpoint_file):
            os.remove(self.checkpoint_file)
            print("🗑️ Checkpoint удален (анализ завершен успешно)")

def main():
    """Основная функция"""
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
    if len(channels_df.columns) >= 3:
        link_column = channels_df.columns[2]
        print(f"Используем третий столбец: {link_column}")
    else:
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
    
    # Создаем менеджер анализа и запускаем
    manager = AnalysisManager()
    manager.run_analysis(channels_df, link_column)

if __name__ == "__main__":
    main()
