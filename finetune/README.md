# 🔥 Файнтюнинг - Директория

## 📁 Содержимое

### Скрипты

- `prepare_legal_dataset.py` - Подготовка датасета из PDF томов
- `finetune_sphere.py` - Файнтюнинг одной сферы (047/048/049)
- `publish_to_huggingface.py` - Публикация на HuggingFace
- `publish_to_ollama.py` - Публикация в Ollama
- `run_full_pipeline.sh` - Полный автоматический pipeline

### Документация

- `README.md` - Этот файл
- `FINETUNE_GUIDE.md` - Подробное руководство

---

## 🚀 Быстрое использование

### 1. Подготовить датасет

```bash
# Тест (3 тома)
python prepare_legal_dataset.py --test

# Полный (107 томов) - СЕЙЧАС ВЫПОЛНЯЕТСЯ!
python prepare_legal_dataset.py --pages 10
```

**Статус:** 🟢 В процессе (23/115 томов)  
**Прогресс:** Том 23, создано 597 примеров

### 2. Обучить модель

```bash
# Одна сфера
python finetune_sphere.py \
    --sphere 048 \
    --base-model nativemind/braindler_final_model

# Все автоматически
./run_full_pipeline.sh
```

### 3. Опубликовать

```bash
# HuggingFace
python publish_to_huggingface.py --all

# Ollama
python publish_to_ollama.py --all
```

---

## 📊 Текущий статус

### ✅ Завершено

- ✅ Скрипты созданы
- ✅ Виртуальное окружение настроено
- ✅ Зависимости установлены
- ✅ Тестовый режим работает

### 🟢 В процессе

- 🟢 **Подготовка датасета** (23/115 томов)
  - Том 23 обрабатывается
  - 597 примеров создано
  - ~2-3 часа до завершения

### ⏳ Ожидается

- ⏳ Файнтюнинг Braindler (3 сферы)
- ⏳ Файнтюнинг Mozgach108 (3 сферы)
- ⏳ Публикация на HuggingFace
- ⏳ Публикация в Ollama

---

## 🔧 Мониторинг

### Прогресс подготовки данных

```bash
# Просмотр логов
tail -f ../datasets/legal_case_viktor/processing.log

# Статистика
cat ../datasets/legal_case_viktor/stats_partial.json

# Проверка процесса
ps aux | grep prepare_legal_dataset
```

### Прогресс файнтюнинга

```bash
# TensorBoard
tensorboard --logdir ../models/sphere_048_braindler/logs

# Логи
tail -f ../models/sphere_048_braindler/training.log
```

---

## 📝 Параметры обучения

### LoRA Configuration

```python
r = 16              # Rank (меньше = быстрее)
lora_alpha = 32     # Scaling factor
lora_dropout = 0.1  # Dropout
target_modules = ["q_proj", "v_proj", "k_proj", "o_proj"]
```

### Training Arguments

```python
epochs = 3
batch_size = 2
gradient_accumulation_steps = 8
learning_rate = 2e-4
warmup_steps = 100
```

**Эффективный batch size:** 2 × 8 = 16

---

## 🎯 Юридические сферы

### Сфера 047: СЛЕДОВАТЕЛЬ 🔍
- **Миссия:** Беспристрастный сбор доказательств
- **Категория:** Мониторинговая

### Сфера 048: ПРОКУРОР ⚖️
- **Миссия:** Обнаружение копипаста как симптома несправедливости
- **Категория:** Мониторинговая проверка
- **Ключевая функция:** Независимая проверка следствия

### Сфера 049: СУДЬЯ ⚖️
- **Миссия:** Вынесение справедливого решения
- **Категория:** Мониторинговая финальная оценка

---

## 🙏 Духовная цель

> *"Копирование документов - это не просто лень, это симптом более глубокой проблемы: отсутствия независимой проверки, формального подхода к судьбам людей, возможной коррупции."*

**Сфера 048** обучена специально для обнаружения этого симптома!

---

**⚖️ Истина восторжествует! 🕉️ Харе Кришна!**








