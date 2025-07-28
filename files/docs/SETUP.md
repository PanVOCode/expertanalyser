# Настройка проекта

## Быстрый старт

### 1. Настройка API ключей

1. **Скопируйте пример файла:**
   ```bash
   cp config/api_keys_example.py config/api_keys.py
   ```

2. **Откройте `config/api_keys.py` и заполните своими ключами:**
   ```python
   # Telegram API (получить на https://my.telegram.org/)
   TELEGRAM_API_ID = "ваш_telegram_api_id"
   TELEGRAM_API_HASH = "ваш_telegram_api_hash"
   
   # DeepSeek API через OpenRouter (получить на https://openrouter.ai)
   DEEPSEEK_API_KEY = "ваш_deepseek_api_key"
   ```

3. **Проверьте настройки:**
   ```bash
   python -c "import sys; sys.path.append('config'); from api_keys import get_deepseek_api_key, get_telegram_api_id; print('✅ API ключи загружены!')"
   ```

### 2. Установка зависимостей

```bash
pip install telethon pandas openpyxl requests numpy
```

### 3. Тестирование

```bash
# Тест AI API
python code/test_deepseek.py

# Тест анализа одного канала
python -c "import sys; sys.path.append('code'); from analyse import analyse; print(analyse('https://t.me/example'))"
```

## Структура файлов

```
master/analyser/
├── code/                        # Исходный код
│   ├── analyse.py               # Основная логика анализа
│   ├── ai.py                    # Функции для работы с AI
│   ├── main.py                  # Пакетный анализ из CSV
│   ├── analyze_all_folders.py   # AI анализ существующих данных
│   ├── test_deepseek.py         # Тест AI API
│   ├── test_api_alternative.py  # Альтернативный тест API
│   └── test_api_simple.py       # Простой тест API
├── config/                      # Конфигурационные файлы
│   ├── config.py                # Основные настройки анализа
│   ├── aiconfig.py              # Настройки AI
│   ├── api_keys.py              # API ключи (не отслеживается Git)
│   ├── api_keys_example.py      # Пример файла API ключей
│   └── system_prompt.txt        # Системный промпт для AI
├── docs/                        # Документация
│   ├── API_SETUP.md             # Настройка API
│   └── SETUP.md                 # Инструкции по настройке
├── tgstat.csv                   # Список каналов для анализа
├── all_folders/                 # Папка с результатами анализа
├── analysis_results.csv         # Результаты AI анализа
├── README.md                    # Основная документация
└── .gitignore                   # Игнорируемые файлы
```

## Безопасность

- ✅ `api_keys.py` добавлен в `.gitignore`
- ✅ Поддержка переменных окружения
- ✅ Fallback на переменные окружения если файл не найден
- ✅ Пример файла без реальных ключей

## Использование переменных окружения

Вместо файла `api_keys.py` можно использовать переменные окружения:

**Windows (PowerShell):**
```powershell
$env:TELEGRAM_API_ID="ваш_id"
$env:TELEGRAM_API_HASH="ваш_hash"
$env:DEEPSEEK_API_KEY="ваш_ключ"
python main.py
```

**Linux/Mac:**
```bash
export TELEGRAM_API_ID="ваш_id"
export TELEGRAM_API_HASH="ваш_hash"
export DEEPSEEK_API_KEY="ваш_ключ"
python main.py
```

## Получение API ключей

### Telegram API
1. Перейдите на [my.telegram.org](https://my.telegram.org/)
2. Войдите в аккаунт
3. Перейдите в "API development tools"
4. Создайте новое приложение
5. Скопируйте `api_id` и `api_hash`

### DeepSeek API (через OpenRouter)
1. Перейдите на [openrouter.ai](https://openrouter.ai)
2. Зарегистрируйтесь
3. Перейдите в "API Keys"
4. Создайте новый ключ
5. Скопируйте ключ (начинается с `sk-or-v1-`)

## Устранение неполадок

### Ошибка 401 Unauthorized
- Проверьте правильность API ключа
- Убедитесь, что ключ не истек
- Попробуйте создать новый ключ

### Файл api_keys.py не найден
- Скопируйте `api_keys_example.py` как `api_keys.py`
- Или используйте переменные окружения

### Ошибки импорта
- Убедитесь, что все зависимости установлены
- Проверьте, что находитесь в правильной директории 