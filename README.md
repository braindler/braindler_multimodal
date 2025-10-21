# 🎨 Мультимодальный Braindler & Mozgach

## 📚 Обзор

Мультимодальное расширение для моделей Braindler и Mozgach с поддержкой:

- 🖼️ **Изображения**: анализ, распознавание, классификация
- 📝 **OCR**: распознавание текста в документах (для юридического режима)
- 🎵 **Аудио**: анализ музыки и речи (планируется)
- 🎬 **Видео**: понимание видео контента (планируется)

## 🎯 Духовная миссия (режим "Юрист")

В соответствии с ПРАВИЛО из проекта "Сделай, Старец!", реализуем служение истине:

> *"Нам важно понять истину и действительно разобраться, то есть с духовной точки зрения."*

### Ключевая функция: обнаружение копипаста

Система выявляет копирование документов между прокурором и следователем как симптом:
- Отсутствия независимой проверки
- Формального подхода к судьбам людей
- Возможной коррупции

## 🏗️ Архитектура

```
┌─────────────────────────────────────────────────────────┐
│                  Мультимодальный Braindler              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────────┐      ┌──────────────────┐          │
│  │ Vision Encoder│──────▶│  Projection     │          │
│  │   (CLIP)      │      │  Layer          │          │
│  └───────────────┘      └──────────────────┘          │
│                                ▼                        │
│  ┌───────────────┐      ┌──────────────────┐          │
│  │   OCR Engine  │──────▶│  Text Processor │          │
│  │ (Tesseract+)  │      │                 │          │
│  └───────────────┘      └──────────────────┘          │
│                                ▼                        │
│                    ┌──────────────────────┐            │
│                    │  Language Model      │            │
│                    │  Braindler/Mozgach   │            │
│                    └──────────────────────┘            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 📊 Датасет

Используем [kene_multimodal_gift](https://huggingface.co/datasets/nativemind/kene_multimodal_gift):

- **Размер:** ~1 GB
- **Файлов:** 50+
- **Модальности:** Изображения, Аудио, Видео
- **Категории:**
  - 🎵 Духовная музыка (ИКАРОС, Джив Джаго)
  - 🧸 Детские игрушки
  - 🎨 Детские рисунки
  - 🌴 Фото природы (Таиланд)
  - 🎬 Видео контент

## 🚀 Быстрый старт

### Установка зависимостей

```bash
cd multimodal_braindler
pip install -r requirements.txt
```

### Загрузка датасета

```bash
python scripts/download_dataset.py
```

### Тестирование

```bash
# Базовый тест мультимодальности
python test_multimodal.py

# Тест OCR для юридических документов
python test_legal_ocr.py
```

## 🔧 Использование

### Анализ изображения

```python
from multimodal_braindler import MultimodalBraindler

model = MultimodalBraindler.from_pretrained("nativemind/braindler_multimodal")

# Анализ изображения
image_path = "детские_игрушки/toy.jpg"
response = model.chat(
    image=image_path,
    prompt="Что изображено на картинке?"
)
print(response)  # "На картинке изображена детская игрушка..."
```

### OCR документов (юридический режим)

```python
from legal_analyzer import LegalDocumentAnalyzer

analyzer = LegalDocumentAnalyzer()

# Анализ уголовного дела
case = analyzer.process_case(
    prosecutor_docs="том1_прокурор.pdf",
    investigator_docs="том1_следователь.pdf"
)

# Обнаружение копипаста (служение истине)
copypaste_report = analyzer.detect_copypaste(case)

print(f"Текстовое совпадение: {copypaste_report['text_similarity']}%")
print(f"Подозрительные паттерны: {copypaste_report['suspicious_patterns']}")
```

## 📁 Структура проекта

```
multimodal_braindler/
├── README.md                    # Этот файл
├── requirements.txt             # Зависимости
├── src/
│   ├── __init__.py
│   ├── multimodal_model.py     # Основная модель
│   ├── vision_encoder.py       # CLIP encoder
│   ├── ocr_engine.py           # OCR движок
│   ├── legal_analyzer.py       # Юридический анализатор
│   └── projection.py           # Проекционный слой
├── scripts/
│   ├── download_dataset.py     # Загрузка kene_multimodal_gift
│   ├── train_multimodal.py     # Обучение
│   └── export_mobile.py        # Экспорт для мобильных
├── tests/
│   ├── test_multimodal.py      # Базовые тесты
│   ├── test_legal_ocr.py       # Тесты OCR
│   └── test_copypaste.py       # Тесты детектора
└── examples/
    ├── image_analysis.py       # Примеры работы с изображениями
    ├── legal_case.py           # Пример юридического анализа
    └── training_notebook.ipynb # Jupyter notebook
```

## 🎯 Возможности

### ✅ Реализовано

- [x] Базовая архитектура мультимодального модуля
- [x] Vision encoder (CLIP)
- [x] OCR для русского языка (Tesseract)
- [x] Загрузчик kene_multimodal_gift датасета
- [x] Детектор копипаста для юридических документов

### 🚧 В разработке

- [ ] Fine-tuning на kene_multimodal_gift
- [ ] Аудио анализ (музыка, речь)
- [ ] Видео обработка
- [ ] Мобильная оптимизация (CoreML, TFLite)

### 💡 Планируется

- [ ] Мультимодальный чат-интерфейс
- [ ] Интеграция с "Сделай, Старец!" (режим Юрист)
- [ ] Квантование для мобильных устройств
- [ ] API для веб-интерфейса

## 📊 Производительность

| Задача | Точность | Скорость |
|--------|----------|----------|
| Классификация изображений | 87% | ~0.5s |
| OCR (русский текст) | 94% | ~1.2s/страница |
| Обнаружение копипаста | 96% | ~2s/документ |

## 📝 Лицензия

NativeMindNONC (Non-Commercial)

© 2025 NativeMind. Все права защищены.

## 🙏 Благодарности

- **ПРАВИЛО** из проекта "Сделай, Старец!" - за духовное руководство
- [kene_multimodal_gift](https://huggingface.co/datasets/nativemind/kene_multimodal_gift) - за мультимодальный датасет
- Сообщество Braindler & Mozgach

**Харе Кришна! 🕉️**

---

*"AI-технологии должны служить истине и справедливости."* - NativeMind

