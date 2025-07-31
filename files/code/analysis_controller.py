#!/usr/bin/env python3
"""
Контроллер анализа с расширенными возможностями управления
- Восстановление прерванного анализа
- Мониторинг прогресса
- Управление backup'ами
- Статистика выполнения
"""

import os
import sys
import json
import shutil
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

# Добавляем пути для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
sys.path.append(os.path.dirname(__file__))

class AnalysisController:
    """Контроллер для управления процессом анализа"""
    
    def __init__(self):
        self.results_dir = '../results'
        self.checkpoint_file = f'{self.results_dir}/analysis_checkpoint.json'
        self.results_file = f'{self.results_dir}/analysis_results.csv'
        self.backup_dir = f'{self.results_dir}/backups'
        
        # Создаем необходимые директории
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def check_status(self):
        """Проверяет статус анализа"""
        print("📊 СТАТУС АНАЛИЗА")
        print("=" * 50)
        
        # Проверяем checkpoint
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                    checkpoint = json.load(f)
                
                current_index = checkpoint.get('current_index', 0)
                results_count = len(checkpoint.get('results', []))
                total_channels = checkpoint.get('total_channels', 0)
                start_time = datetime.fromisoformat(checkpoint.get('start_time', datetime.now().isoformat()))
                last_save = datetime.fromisoformat(checkpoint.get('last_save', datetime.now().isoformat()))
                
                print(f"✅ Анализ в процессе")
                print(f"📈 Прогресс: {results_count}/{total_channels} каналов ({results_count/total_channels*100:.1f}%)")
                print(f"🔄 Следующий канал: {current_index + 1}")
                print(f"⏰ Начало: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"💾 Последнее сохранение: {last_save.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Время выполнения
                elapsed = datetime.now() - start_time
                print(f"⏱️ Время выполнения: {elapsed}")
                
                if results_count > 0:
                    avg_time = elapsed / results_count
                    remaining_channels = total_channels - results_count
                    estimated_remaining = avg_time * remaining_channels
                    print(f"📊 Среднее время на канал: {avg_time}")
                    print(f"⏳ Оставшееся время: {estimated_remaining}")
                
                return True
                
            except Exception as e:
                print(f"❌ Ошибка чтения checkpoint: {e}")
                return False
        else:
            print("❌ Анализ не запущен или завершен")
            return False
    
    def create_backup(self, backup_name=None):
        """Создает backup результатов"""
        if not backup_name:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"backup_{timestamp}"
        
        backup_path = f"{self.backup_dir}/{backup_name}"
        os.makedirs(backup_path, exist_ok=True)
        
        print(f"💾 Создание backup: {backup_name}")
        
        # Копируем результаты
        if os.path.exists(self.results_file):
            shutil.copy2(self.results_file, f"{backup_path}/analysis_results.csv")
            print(f"  ✅ Результаты скопированы")
        
        # Копируем checkpoint
        if os.path.exists(self.checkpoint_file):
            shutil.copy2(self.checkpoint_file, f"{backup_path}/analysis_checkpoint.json")
            print(f"  ✅ Checkpoint скопирован")
        
        # Копируем папку all_folders если есть
        all_folders_path = f"{self.results_dir}/all_folders"
        if os.path.exists(all_folders_path):
            shutil.copytree(all_folders_path, f"{backup_path}/all_folders", dirs_exist_ok=True)
            print(f"  ✅ Папка all_folders скопирована")
        
        print(f"✅ Backup создан: {backup_path}")
        return backup_path
    
    def restore_backup(self, backup_name):
        """Восстанавливает backup"""
        backup_path = f"{self.backup_dir}/{backup_name}"
        
        if not os.path.exists(backup_path):
            print(f"❌ Backup {backup_name} не найден")
            return False
        
        print(f"🔄 Восстановление backup: {backup_name}")
        
        # Восстанавливаем результаты
        backup_results = f"{backup_path}/analysis_results.csv"
        if os.path.exists(backup_results):
            shutil.copy2(backup_results, self.results_file)
            print(f"  ✅ Результаты восстановлены")
        
        # Восстанавливаем checkpoint
        backup_checkpoint = f"{backup_path}/analysis_checkpoint.json"
        if os.path.exists(backup_checkpoint):
            shutil.copy2(backup_checkpoint, self.checkpoint_file)
            print(f"  ✅ Checkpoint восстановлен")
        
        # Восстанавливаем папку all_folders
        backup_all_folders = f"{backup_path}/all_folders"
        if os.path.exists(backup_all_folders):
            if os.path.exists(f"{self.results_dir}/all_folders"):
                shutil.rmtree(f"{self.results_dir}/all_folders")
            shutil.copytree(backup_all_folders, f"{self.results_dir}/all_folders")
            print(f"  ✅ Папка all_folders восстановлена")
        
        print(f"✅ Backup восстановлен")
        return True
    
    def list_backups(self):
        """Показывает список доступных backup'ов"""
        print("📋 ДОСТУПНЫЕ BACKUP'Ы")
        print("=" * 50)
        
        if not os.path.exists(self.backup_dir):
            print("❌ Папка backup'ов не существует")
            return
        
        backups = []
        for item in os.listdir(self.backup_dir):
            backup_path = f"{self.backup_dir}/{item}"
            if os.path.isdir(backup_path):
                # Получаем информацию о backup
                stat = os.stat(backup_path)
                created_time = datetime.fromtimestamp(stat.st_mtime)
                
                # Проверяем содержимое
                has_results = os.path.exists(f"{backup_path}/analysis_results.csv")
                has_checkpoint = os.path.exists(f"{backup_path}/analysis_checkpoint.json")
                has_folders = os.path.exists(f"{backup_path}/all_folders")
                
                backups.append({
                    'name': item,
                    'created': created_time,
                    'has_results': has_results,
                    'has_checkpoint': has_checkpoint,
                    'has_folders': has_folders
                })
        
        if not backups:
            print("❌ Backup'ы не найдены")
            return
        
        # Сортируем по дате создания (новые сначала)
        backups.sort(key=lambda x: x['created'], reverse=True)
        
        for i, backup in enumerate(backups, 1):
            print(f"{i}. {backup['name']}")
            print(f"   📅 Создан: {backup['created'].strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   📊 Содержимое: ", end="")
            if backup['has_results']:
                print("📄 результаты ", end="")
            if backup['has_checkpoint']:
                print("💾 checkpoint ", end="")
            if backup['has_folders']:
                print("📁 папки ", end="")
            print()
            print()
    
    def show_statistics(self):
        """Показывает статистику анализа"""
        print("📈 СТАТИСТИКА АНАЛИЗА")
        print("=" * 50)
        
        # Статистика результатов
        if os.path.exists(self.results_file):
            try:
                df = pd.read_csv(self.results_file, sep=';', encoding='utf-8')
                total_channels = len(df)
                
                # Статистика по экспертам
                expert_stats = df['эксперт'].value_counts()
                
                print(f"📊 Всего проанализировано каналов: {total_channels}")
                print(f"👨‍💼 Эксперты: {expert_stats.get('true', 0)} ({expert_stats.get('true', 0)/total_channels*100:.1f}%)")
                print(f"❌ Не эксперты: {expert_stats.get('false', 0)} ({expert_stats.get('false', 0)/total_channels*100:.1f}%)")
                print(f"❓ Неизвестно: {expert_stats.get('unknown', 0)} ({expert_stats.get('unknown', 0)/total_channels*100:.1f}%)")
                
                # Топ компетенций
                print("\n🏆 ТОП КОМПЕТЕНЦИЙ:")
                all_competencies = []
                for comp_str in df['компетенции'].dropna():
                    if comp_str and comp_str != 'Ошибка: не удалось получить данные':
                        competencies = [c.strip() for c in comp_str.split(',')]
                        all_competencies.extend(competencies)
                
                if all_competencies:
                    from collections import Counter
                    comp_counter = Counter(all_competencies)
                    top_comp = comp_counter.most_common(10)
                    
                    for i, (comp, count) in enumerate(top_comp, 1):
                        print(f"  {i}. {comp}: {count}")
                
            except Exception as e:
                print(f"❌ Ошибка чтения статистики: {e}")
        else:
            print("❌ Файл результатов не найден")
    
    def cleanup_old_backups(self, days=7):
        """Удаляет старые backup'ы"""
        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_count = 0
        
        print(f"🧹 Удаление backup'ов старше {days} дней")
        
        if not os.path.exists(self.backup_dir):
            print("❌ Папка backup'ов не существует")
            return
        
        for item in os.listdir(self.backup_dir):
            backup_path = f"{self.backup_dir}/{item}"
            if os.path.isdir(backup_path):
                stat = os.stat(backup_path)
                created_time = datetime.fromtimestamp(stat.st_mtime)
                
                if created_time < cutoff_date:
                    try:
                        shutil.rmtree(backup_path)
                        print(f"🗑️ Удален: {item}")
                        deleted_count += 1
                    except Exception as e:
                        print(f"❌ Ошибка удаления {item}: {e}")
        
        print(f"✅ Удалено backup'ов: {deleted_count}")
    
    def reset_analysis(self, confirm=False):
        """Сбрасывает анализ (удаляет checkpoint)"""
        if not confirm:
            print("⚠️ Для сброса анализа используйте --confirm")
            return False
        
        print("🔄 Сброс анализа")
        
        if os.path.exists(self.checkpoint_file):
            os.remove(self.checkpoint_file)
            print("✅ Checkpoint удален")
        
        print("✅ Анализ сброшен. Можно запустить заново.")
        return True

def main():
    """Основная функция контроллера"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Контроллер анализа Telegram каналов')
    parser.add_argument('action', choices=['status', 'backup', 'restore', 'list-backups', 
                                          'stats', 'cleanup', 'reset'], 
                       help='Действие для выполнения')
    parser.add_argument('--name', help='Имя backup для создания/восстановления')
    parser.add_argument('--days', type=int, default=7, help='Количество дней для cleanup')
    parser.add_argument('--confirm', action='store_true', help='Подтверждение для reset')
    
    args = parser.parse_args()
    
    controller = AnalysisController()
    
    if args.action == 'status':
        controller.check_status()
    
    elif args.action == 'backup':
        controller.create_backup(args.name)
    
    elif args.action == 'restore':
        if not args.name:
            print("❌ Укажите имя backup для восстановления: --name")
            return
        controller.restore_backup(args.name)
    
    elif args.action == 'list-backups':
        controller.list_backups()
    
    elif args.action == 'stats':
        controller.show_statistics()
    
    elif args.action == 'cleanup':
        controller.cleanup_old_backups(args.days)
    
    elif args.action == 'reset':
        controller.reset_analysis(args.confirm)

if __name__ == "__main__":
    main() 