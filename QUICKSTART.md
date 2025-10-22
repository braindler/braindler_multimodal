# 🚀 Быстрый старт - Мультимодальный Braindler & Mozgach

## Установка

### 1. Клонирование и установка зависимостей

```bash
cd /Users/anton/proj/ai.nativemind.net/multimodal_braindler

# Установка зависимостей
pip install -r requirements.txt

# Установка Tesseract для OCR (macOS)
brew install tesseract tesseract-lang
```

### 2. Загрузка датасета

```bash
python scripts/download_dataset.py
```

---

## 🎯 Базовое использование

### Простой мультимодальный чат

```python
from multimodal_braindler import MultimodalBraindler

# Создаем модель
model = MultimodalBraindler()

# Анализ изображения
response = model.chat(
    prompt="Что изображено на картинке?",
    image="path/to/image.jpg"
)
print(response)
```

---

## ⚖️ Юридические модели (Сферы 047-049)

### Быстрый пример всех трех сфер

```python
from multimodal_braindler import LegalModelsFactory

# Создаем полную юридическую систему
legal_system = LegalModelsFactory.create_full_legal_system()

investigator = legal_system['investigator']  # Сфера 047
prosecutor = legal_system['prosecutor']       # Сфера 048
judge = legal_system['judge']                 # Сфера 049

print("✅ Юридическая система готова к служению истине!")
```

### Пример: Обнаружение копипаста (Сфера 048)

```python
# КЛЮЧЕВАЯ ДУХОВНАЯ ФУНКЦИЯ!
prosecutor = LegalModelsFactory.create_prosecutor()

result = prosecutor.supervise_investigation(
    prosecutor_docs=["обвинительное.pdf"],
    investigator_docs=["постановление.pdf"],
    case_name="Дело №123"
)

# Проверяем результат
print(f"Сходство: {result['copypaste_analysis'].text_similarity}%")
print(f"Вердикт: {result['spiritual_verdict']}")

# Если >= 70% - ТРЕВОГА! Возможна коррупция
if result['copypaste_analysis'].text_similarity >= 70:
    print("⚠️ КРИТИЧЕСКОЕ: Обнаружен копипаст!")
```

---

## 🧪 Тестирование

### Запуск всех тестов

```bash
# Все юридические модели
python tests/test_legal_models.py --test all

# Только одна модель
python tests/test_legal_models.py --test prosecutor
```

### Запуск примеров

```bash
# Простой случай
python examples/legal_case_example.py --example simple

# Обнаружение копипаста
python examples/legal_case_example.py --example copypaste

# Все примеры
python examples/legal_case_example.py --example all
```

---

## 📊 Структура проекта

```
multimodal_braindler/
├── src/                           # Исходный код
│   ├── multimodal_model.py       # Базовые модели
│   ├── vision_encoder.py         # CLIP encoder
│   ├── ocr_engine.py             # OCR движок
│   ├── legal_analyzer.py         # Детектор копипаста
│   └── legal_models.py           # Сферы 047-049
├── scripts/
│   └── download_dataset.py       # Загрузка датасетов
├── tests/
│   └── test_legal_models.py      # Тесты
├── examples/
│   └── legal_case_example.py     # Примеры
├── requirements.txt               # Зависимости
├── README.md                      # Основная документация
├── LEGAL_MODELS.md                # Юридические модели
└── QUICKSTART.md                  # Этот файл
```

---

## 🎓 Обучение

### Fine-tuning на своих данных

```python
# TODO: Будет добавлено позже
```

---

## 🔧 Настройка

### Использование разных устройств

```python
# CPU
model = MultimodalBraindler(device="cpu")

# CUDA GPU
model = MultimodalBraindler(device="cuda")

# Apple Silicon (MPS)
model = MultimodalBraindler(device="mps")

# Автоматический выбор
model = MultimodalBraindler(device="auto")  # по умолчанию
```

### Использование разных моделей

```python
# Braindler (образовательный)
from multimodal_braindler import MultimodalBraindler
model = MultimodalBraindler(
    language_model_name="nativemind/braindler_final_model"
)

# Mozgach (универсальный)
from multimodal_braindler import MultimodalMozgach
model = MultimodalMozgach(
    language_model_name="nativemind/mozgach_full_trained_model"
)
```

---

## 📝 Следующие шаги

1. Прочитайте [README.md](README.md) для полного обзора
2. Изучите [LEGAL_MODELS.md](LEGAL_MODELS.md) для деталей юридических моделей
3. Запустите примеры из `examples/`
4. Экспериментируйте со своими данными!

---

## 🆘 Помощь

### Частые проблемы

**Ошибка: "No module named 'transformers'"**
```bash
pip install transformers torch
```

**Ошибка: "Tesseract not found"**
```bash
# macOS
brew install tesseract tesseract-lang

# Ubuntu
sudo apt-get install tesseract-ocr tesseract-ocr-rus
```

**Не хватает памяти**
```python
# Используйте CPU вместо GPU
model = MultimodalBraindler(device="cpu")
```

---

## 🙏 Духовная заметка

Эти модели созданы для служения истине и справедливости.

> *"Нам важно понять истину и действительно разобраться, то есть с духовной точки зрения."*

**⚖️ Истина восторжествует! 🕉️ Харе Кришна!**





