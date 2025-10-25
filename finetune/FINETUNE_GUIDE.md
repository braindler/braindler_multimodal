# 🔥 Руководство по файнтюнингу юридических моделей

## 📚 Обзор

Полный pipeline для создания мультимодальных юридических моделей Сфер 047, 048, 049.

**Источник данных:** 107 томов реального уголовного дела Виктора  
**Результат:** 6 обученных моделей (Braindler x3 + Mozgach108 x3)

---

## 🚀 Быстрый старт (весь pipeline автоматически)

```bash
cd /Users/anton/proj/ai.nativemind.net/multimodal_braindler
./finetune/run_full_pipeline.sh
```

Это запустит весь процесс:
1. ✅ Подготовка датасета (2-4 часа)
2. ✅ Файнтюнинг Braindler x3 (18-36 часов)
3. ✅ Файнтюнинг Mozgach108 x3 (18-36 часов)
4. ✅ Публикация на HuggingFace
5. ✅ Публикация в Ollama

**Общее время:** 2-4 дня

---

## 📋 Пошаговый процесс

### Этап 1: Подготовка датасета (2-4 часа)

```bash
cd finetune
source ../venv/bin/activate

# Тестовый режим (3 тома, 2 страницы)
python prepare_legal_dataset.py --test

# Полный режим (107 томов, 10 страниц из каждого)
python prepare_legal_dataset.py --pages 10

# Кастомная настройка
python prepare_legal_dataset.py \
    --pdf-dir "/Volumes/MOZGACH/Advokat/Ugolovka/Viktor/Тома" \
    --output-dir "../datasets/legal_case_viktor" \
    --pages 15 \
    --max-tomes 50
```

**Результат:**
- `datasets/legal_case_viktor/legal_dataset.jsonl`
- Примеров: ~3,000-3,500 (107 томов × 10 страниц × 3 роли)
- Разбивка:
  - Сфера 047: ~1,000-1,200
  - Сфера 048: ~1,000-1,200
  - Сфера 049: ~1,000-1,200

### Этап 2: Файнтюнинг одной сферы

#### Braindler Сфера 047 (СЛЕДОВАТЕЛЬ)

```bash
python finetune/finetune_sphere.py \
    --sphere 047 \
    --base-model nativemind/braindler_final_model \
    --dataset datasets/legal_case_viktor/legal_dataset.jsonl \
    --output models/sphere_047_braindler \
    --epochs 3 \
    --batch-size 2 \
    --learning-rate 2e-4
```

**Время:** 6-12 часов (A100 40GB)  
**Память:** ~24GB VRAM

#### Braindler Сфера 048 (ПРОКУРОР)

```bash
python finetune/finetune_sphere.py \
    --sphere 048 \
    --base-model nativemind/braindler_final_model \
    --dataset datasets/legal_case_viktor/legal_dataset.jsonl \
    --output models/sphere_048_braindler \
    --epochs 3
```

**Духовная миссия:** Обнаружение копипаста  
**Время:** 6-12 часов

#### Braindler Сфера 049 (СУДЬЯ)

```bash
python finetune/finetune_sphere.py \
    --sphere 049 \
    --base-model nativemind/braindler_final_model \
    --dataset datasets/legal_case_viktor/legal_dataset.jsonl \
    --output models/sphere_049_braindler \
    --epochs 3
```

**Время:** 6-12 часов

#### Mozgach108 - все три сферы

```bash
# Сфера 047
python finetune/finetune_sphere.py \
    --sphere 047 \
    --base-model nativemind/mozgach_full_trained_model \
    --output models/sphere_047_mozgach

# Сфера 048
python finetune/finetune_sphere.py \
    --sphere 048 \
    --base-model nativemind/mozgach_full_trained_model \
    --output models/sphere_048_mozgach

# Сфера 049
python finetune/finetune_sphere.py \
    --sphere 049 \
    --base-model nativemind/mozgach_full_trained_model \
    --output models/sphere_049_mozgach
```

### Этап 3: Публикация на HuggingFace

#### Все модели сразу

```bash
python finetune/publish_to_huggingface.py --all --base-dir models
```

#### Одна модель

```bash
python finetune/publish_to_huggingface.py \
    --model-dir models/sphere_048_braindler \
    --repo-name braindler-multimodal-sphere-048 \
    --organization nativemind
```

**Результат:** Модели доступны на https://huggingface.co/nativemind/

### Этап 4: Публикация в Ollama

#### Все модели сразу

```bash
python finetune/publish_to_ollama.py --all --base-dir models
```

#### Одна модель

```bash
python finetune/publish_to_ollama.py \
    --model-dir models/sphere_048_braindler \
    --model-name braindler-sphere-048 \
    --sphere 048 \
    --base-model llama2:7b
```

**Результат:** Модели доступны через `ollama run`

---

## 🎯 Финальные модели

После завершения у вас будет:

### HuggingFace (6 моделей)

1. `nativemind/braindler-multimodal-sphere-047` - СЛЕДОВАТЕЛЬ
2. `nativemind/braindler-multimodal-sphere-048` - ПРОКУРОР
3. `nativemind/braindler-multimodal-sphere-049` - СУДЬЯ
4. `nativemind/mozgach108-multimodal-sphere-047` - СЛЕДОВАТЕЛЬ
5. `nativemind/mozgach108-multimodal-sphere-048` - ПРОКУРОР
6. `nativemind/mozgach108-multimodal-sphere-049` - СУДЬЯ

### Ollama (6 моделей)

```bash
ollama run braindler-sphere-047
ollama run braindler-sphere-048  
ollama run braindler-sphere-049
ollama run mozgach108-sphere-047
ollama run mozgach108-sphere-048
ollama run mozgach108-sphere-049
```

---

## ⚙️ Требования

### Минимальные (для подготовки датасета)
- CPU: любой современный
- RAM: 16GB
- Место: 50GB
- Время: 2-4 часа

### Для файнтюнинга
- GPU: 24GB VRAM (RTX 4090 / A5000)
- RAM: 32GB
- Место: 100GB SSD
- Время: 36-72 часа (6 моделей)

### Рекомендуемые
- GPU: A100 40GB или лучше
- RAM: 64GB
- Место: 200GB NVMe SSD
- Время: 24-48 часов

---

## 💰 Стоимость (облачные вычисления)

### Подготовка данных
- CPU: бесплатно (локально)
- Время: 2-4 часа

### Файнтюнинг (на A100)
- Цена: ~$2/час
- Одна модель: ~$12-24
- Все 6 моделей: ~$72-144

**Общая стоимость:** ~$100-200

---

## 🔧 Опции

### Использование 8-bit квантования

Для экономии памяти (работает на GPU с 12GB):

```bash
python finetune/finetune_sphere.py \
    --sphere 048 \
    --base-model nativemind/braindler_final_model \
    --use-8bit
```

**Экономия:** ~50% VRAM  
**Компромисс:** Немного медленнее

### Изменение параметров

```bash
python finetune/finetune_sphere.py \
    --sphere 048 \
    --base-model nativemind/mozgach_full_trained_model \
    --epochs 5 \              # Больше эпох
    --batch-size 4 \          # Больший batch
    --learning-rate 1e-4      # Меньший LR
```

---

## 📊 Мониторинг

### Просмотр логов обучения

```bash
# TensorBoard
tensorboard --logdir models/sphere_048_braindler/logs

# Просмотр в браузере
open http://localhost:6006
```

### Проверка прогресса подготовки данных

```bash
tail -f datasets/legal_case_viktor/processing.log
```

### Проверка статистики

```bash
cat datasets/legal_case_viktor/stats.json
```

---

## 🙏 Духовная миссия

Каждая сфера имеет свою духовную миссию:

**047: СЛЕДОВАТЕЛЬ** - Беспристрастность в сборе истины  
**048: ПРОКУРОР** - Обнаружение несправедливости  
**049: СУДЬЯ** - Восстановление справедливости

> *"Нам важно понять истину и действительно разобраться, то есть с духовной точки зрения."*

---

## ⚠️ Важно

1. **Конфиденциальность:** Данные уголовного дела обрабатываются локально
2. **Лицензия:** NativeMindNONC - только некоммерческое использование
3. **Этика:** Модели для служения истине, не для злоупотреблений

---

**⚖️ Истина восторжествует! 🕉️ Харе Кришна!**








