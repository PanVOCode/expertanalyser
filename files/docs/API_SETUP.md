# Настройка API ключа для OpenRouter

## Проблема
Получена ошибка 401 Unauthorized при обращении к OpenRouter API. Это означает, что API ключ истек или недействителен.

## Решение

### 1. Получение нового API ключа

1. Перейдите на [openrouter.ai](https://openrouter.ai)
2. Зарегистрируйтесь или войдите в аккаунт
3. Перейдите в раздел **API Keys**
4. Нажмите **"Create API Key"**
5. Скопируйте новый ключ (начинается с `sk-or-v1-`)

### 2. Обновление API ключа

#### Вариант A: Обновить в файле (рекомендуется для разработки)
Откройте файл `aiconfig.py` и замените значение `DEEPSEEK_API_KEY`:

```python
DEEPSEEK_API_KEY = "ваш-новый-api-ключ-здесь"
```

#### Вариант B: Использовать переменную окружения (рекомендуется для продакшена)

**Windows (PowerShell):**
```powershell
$env:DEEPSEEK_API_KEY="ваш-новый-api-ключ-здесь"
python main.py
```

**Windows (Command Prompt):**
```cmd
set DEEPSEEK_API_KEY=ваш-новый-api-ключ-здесь
python main.py
```

**Linux/Mac:**
```bash
export DEEPSEEK_API_KEY="ваш-новый-api-ключ-здесь"
python main.py
```

### 3. Проверка работы API

После обновления ключа запустите тест:

```bash
python test_deepseek.py
```

Если тест проходит успешно, вы увидите:
```
🎉 API DeepSeek через OpenRouter работает корректно!
```

### 4. Безопасность

⚠️ **Важно:** Не публикуйте API ключи в публичных репозиториях!

- Используйте переменные окружения для продакшена
- Добавьте `aiconfig.py` в `.gitignore` если содержит реальные ключи
- Регулярно обновляйте API ключи

### 5. Альтернативные решения

Если проблема с OpenRouter продолжается:

1. **Попробуйте другую модель:**
   ```python
   DEEPSEEK_MODEL = "deepseek/deepseek-coder"  # альтернативная модель
   ```

2. **Используйте другой провайдер:**
   - OpenAI GPT
   - Anthropic Claude
   - Google Gemini

3. **Проверьте лимиты:**
   - Убедитесь, что у вас есть кредиты на OpenRouter
   - Проверьте лимиты запросов

## Поддержка

Если проблема не решается:
1. Проверьте статус OpenRouter: [status.openrouter.ai](https://status.openrouter.ai)
2. Обратитесь в поддержку OpenRouter
3. Создайте issue в репозитории проекта 