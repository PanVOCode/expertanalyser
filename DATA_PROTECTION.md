# Система защиты данных от потери

## Обзор

Реализована комплексная система защиты от потери данных при анализе Telegram каналов. Система включает:

- ✅ **Checkpoint'ы** - автоматическое сохранение прогресса
- ✅ **Промежуточное сохранение** - результаты сохраняются каждые 10 каналов
- ✅ **Graceful shutdown** - корректное завершение при прерывании
- ✅ **Атомарные операции** - защита от повреждения файлов
- ✅ **Backup система** - создание и восстановление резервных копий
- ✅ **Восстановление** - продолжение анализа с места остановки

## Архитектура защиты

### 1. Checkpoint система

**Файл:** `results/analysis_checkpoint.json`

Содержит:
- Текущий индекс обрабатываемого канала
- Все уже проанализированные результаты
- Время начала и последнего сохранения
- Общее количество каналов

```json
{
  "current_index": 45,
  "results": [...],
  "total_channels": 1000,
  "start_time": "2024-01-15T10:30:00",
  "last_save": "2024-01-15T12:45:30"
}
```

### 2. Атомарные операции

Все операции записи файлов выполняются атомарно:

1. Запись во временный файл
2. Проверка целостности
3. Атомарное переименование

Это защищает от потери данных при сбоях во время записи.

### 3. Graceful Shutdown

Обработчики сигналов:
- `SIGINT` (Ctrl+C)
- `SIGTERM` (завершение процесса)

При получении сигнала:
1. Сохраняется текущий прогресс
2. Записываются результаты
3. Корректное завершение

## Использование

### Запуск анализа

```bash
# Из папки analyser
python files/code/main.py
```

Система автоматически:
- Загрузит предыдущий прогресс (если есть)
- Продолжит с места остановки
- Будет сохранять результаты каждые 10 каналов

### Управление через контроллер

```bash
# Проверка статуса
python files/code/analysis_controller.py status

# Создание backup
python files/code/analysis_controller.py backup --name my_backup

# Восстановление backup
python files/code/analysis_controller.py restore --name my_backup

# Список backup'ов
python files/code/analysis_controller.py list-backups

# Статистика анализа
python files/code/analysis_controller.py stats

# Очистка старых backup'ов (старше 7 дней)
python files/code/analysis_controller.py cleanup --days 7

# Сброс анализа (удаление checkpoint)
python files/code/analysis_controller.py reset --confirm
```

## Структура файлов

```
analyser/
├── results/
│   ├── analysis_results.csv          # Основные результаты
│   ├── analysis_results_temp.csv     # Временный файл результатов
│   ├── analysis_checkpoint.json      # Checkpoint прогресса
│   ├── analysis_checkpoint.json.tmp  # Временный checkpoint
│   ├── analysis_results.csv.backup   # Backup результатов
│   ├── backups/                      # Папка с backup'ами
│   │   ├── backup_20240115_104500/
│   │   │   ├── analysis_results.csv
│   │   │   ├── analysis_checkpoint.json
│   │   │   └── all_folders/
│   │   └── backup_20240115_120000/
│   └── all_folders/                  # Детальные результаты по каналам
└── files/code/
    ├── main.py                       # Основной скрипт анализа
    └── analysis_controller.py        # Контроллер управления
```

## Сценарии использования

### 1. Прерывание анализа

**Ситуация:** Анализ прерван (Ctrl+C, сбой питания, etc.)

**Действия:**
1. Система автоматически сохранит прогресс
2. При следующем запуске анализ продолжится с места остановки

```bash
# Проверить статус
python files/code/analysis_controller.py status

# Запустить анализ (продолжится автоматически)
python files/code/main.py
```

### 2. Создание backup перед важными изменениями

```bash
# Создать backup с именем
python files/code/analysis_controller.py backup --name before_update

# Продолжить анализ
python files/code/main.py
```

### 3. Восстановление после проблем

```bash
# Посмотреть доступные backup'ы
python files/code/analysis_controller.py list-backups

# Восстановить нужный backup
python files/code/analysis_controller.py restore --name before_update

# Продолжить анализ
python files/code/main.py
```

### 4. Мониторинг прогресса

```bash
# Проверить статус во время выполнения
python files/code/analysis_controller.py status

# Посмотреть статистику
python files/code/analysis_controller.py stats
```

## Безопасность

### Защита от потери данных

1. **Множественные копии:**
   - Основной файл результатов
   - Временный файл
   - Backup файл
   - Checkpoint с полными результатами

2. **Атомарные операции:**
   - Запись во временный файл
   - Проверка целостности
   - Атомарное переименование

3. **Graceful shutdown:**
   - Обработка сигналов прерывания
   - Автоматическое сохранение при завершении

### Автоматическая очистка

- Checkpoint удаляется после успешного завершения
- Временные файлы очищаются автоматически
- Старые backup'ы можно удалить через контроллер

## Мониторинг и диагностика

### Логирование

Система выводит подробную информацию:
- Прогресс анализа
- Время выполнения
- Ошибки и предупреждения
- Статистика сохранений

### Статистика

```bash
# Общая статистика
python files/code/analysis_controller.py stats

# Статус выполнения
python files/code/analysis_controller.py status
```

## Рекомендации

### 1. Регулярные backup'ы

Создавайте backup'ы перед важными операциями:
```bash
python files/code/analysis_controller.py backup --name before_major_changes
```

### 2. Мониторинг места на диске

Backup'ы могут занимать много места. Регулярно очищайте старые:
```bash
python files/code/analysis_controller.py cleanup --days 7
```

### 3. Проверка целостности

После восстановления проверяйте данные:
```bash
python files/code/analysis_controller.py stats
```

### 4. Тестирование восстановления

Периодически тестируйте восстановление из backup'ов на тестовых данных.

## Устранение неполадок

### Проблема: Checkpoint поврежден

```bash
# Удалить поврежденный checkpoint
python files/code/analysis_controller.py reset --confirm

# Восстановить из backup
python files/code/analysis_controller.py restore --name last_good_backup
```

### Проблема: Недостаточно места на диске

```bash
# Очистить старые backup'ы
python files/code/analysis_controller.py cleanup --days 1

# Удалить временные файлы
rm -f results/*.tmp results/*.backup
```

### Проблема: Анализ не продолжается

```bash
# Проверить статус
python files/code/analysis_controller.py status

# Принудительно сбросить
python files/code/analysis_controller.py reset --confirm
```

## Заключение

Новая система защиты данных обеспечивает:

- **Надежность:** Множественные уровни защиты от потери данных
- **Удобство:** Автоматическое восстановление и продолжение
- **Гибкость:** Полный контроль через контроллер
- **Мониторинг:** Подробная статистика и диагностика

Теперь можно безопасно прерывать и возобновлять анализ без потери данных! 