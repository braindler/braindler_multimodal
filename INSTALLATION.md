# 🔧 Установка - Мультимодальный Braindler & Mozgach

## Быстрая установка

```bash
cd /Users/anton/proj/ai.nativemind.net/multimodal_braindler

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# или
venv\Scripts\activate  # Windows

# Установка базовых зависимостей
pip install torch torchvision transformers datasets pillow \
    python-Levenshtein fuzzywuzzy

# Опциональные зависимости для OCR
pip install pytesseract PyMuPDF pdf2image

# Для macOS: установка Tesseract
brew install tesseract tesseract-lang

# Проверка установки
python demo_quickstart.py
```

## Детальная установка

### 1. Системные требования

**Минимальные:**
- Python 3.8+
- 8GB RAM
- 5GB свободного места

**Рекомендуемые:**
- Python 3.10+
- 16GB+ RAM
- GPU с 8GB+ VRAM (опционально)
- 20GB свободного места

### 2. Создание окружения

```bash
# Создать виртуальное окружение
python3 -m venv venv

# Активировать
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Обновить pip
pip install --upgrade pip
```

### 3. Установка PyTorch

**CPU версия (быстрая установка):**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

**GPU версия (CUDA):**
```bash
# CUDA 11.8
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

**Apple Silicon (M1/M2/M3):**
```bash
pip install torch torchvision
# PyTorch автоматически использует MPS
```

### 4. Основные библиотеки

```bash
pip install transformers>=4.35.0
pip install datasets>=2.14.0
pip install Pillow>=10.0.0
pip install huggingface-hub>=0.19.0
pip install safetensors>=0.4.0
```

### 5. Библиотеки для детектора копипаста

```bash
pip install python-Levenshtein>=0.21.0
pip install fuzzywuzzy>=0.18.0
pip install jellyfish>=1.0.0
```

### 6. OCR библиотеки

```bash
# Python библиотеки
pip install pytesseract>=0.3.10
pip install PyMuPDF>=1.23.0
pip install pdf2image>=1.16.3
pip install opencv-python>=4.8.0

# Системные зависимости
# macOS:
brew install tesseract tesseract-lang

# Ubuntu/Debian:
sudo apt-get install tesseract-ocr tesseract-ocr-rus

# Windows:
# Скачать с https://github.com/UB-Mannheim/tesseract/wiki
```

### 7. Опциональные библиотеки

```bash
# Для обработки аудио (будущие версии)
pip install librosa soundfile torchaudio

# Для видео (будущие версии)
pip install moviepy av

# Для веб-интерфейса (будущие версии)
pip install fastapi uvicorn gradio
```

## Проверка установки

### Быстрая проверка

```bash
python demo_quickstart.py
```

Вы должны увидеть:
```
✅ QUICKSTART ЗАВЕРШЕН
⚖️  Истина восторжествует! 🕉️  Харе Кришна!
```

### Детальная проверка

```python
# Проверка PyTorch
import torch
print(f"PyTorch: {torch.__version__}")
print(f"CUDA доступен: {torch.cuda.is_available()}")
print(f"MPS доступен: {torch.backends.mps.is_available()}")

# Проверка Transformers
import transformers
print(f"Transformers: {transformers.__version__}")

# Проверка PIL
from PIL import Image
print(f"PIL установлен")

# Проверка алгоритмов сравнения
from Levenshtein import ratio
from fuzzywuzzy import fuzz
print(f"Детектор копипаста готов")
```

## Решение проблем

### Ошибка: "No module named 'torch'"

```bash
pip install torch torchvision
```

### Ошибка: "Tesseract not found"

```bash
# macOS
brew install tesseract tesseract-lang

# Ubuntu
sudo apt-get install tesseract-ocr tesseract-ocr-rus

# Проверка
tesseract --version
```

### Ошибка: Out of memory

```python
# Используйте CPU вместо GPU
model = MultimodalBraindler(device="cpu")

# Или уменьшите batch size
# В training_args измените per_device_train_batch_size=1
```

### Ошибка: "externally-managed-environment"

Это означает, что система защищена от установки пакетов глобально.

**Решение:**
```bash
# Используйте виртуальное окружение (рекомендуется)
python3 -m venv venv
source venv/bin/activate
pip install ...

# ИЛИ установите с --user
pip install --user torch

# ИЛИ используйте pipx
brew install pipx
pipx install ...
```

## Загрузка моделей

### Модели Braindler

```bash
# Через HuggingFace CLI
huggingface-cli login
huggingface-cli download nativemind/braindler_final_model

# Или через Python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "nativemind/braindler_final_model"
)
```

### Модели Mozgach

```bash
huggingface-cli download nativemind/mozgach_full_trained_model
```

### Датасет kene_multimodal_gift

```bash
python scripts/download_dataset.py
```

## Настройка окружения

### Переменные окружения

```bash
# Для HuggingFace
export HF_HOME="/path/to/cache"
export HF_TOKEN="your_token"

# Для Tesseract (если не в PATH)
export TESSDATA_PREFIX="/usr/local/share/tessdata"
```

### Конфигурация для разных устройств

**Apple Silicon (M1/M2/M3):**
```python
device = "mps"  # Metal Performance Shaders
```

**NVIDIA GPU:**
```python
device = "cuda"
```

**CPU:**
```python
device = "cpu"
```

**Автоматический выбор:**
```python
device = "auto"  # Автоматически выберет лучший
```

## Обновление

```bash
# Обновить все зависимости
pip install --upgrade -r requirements.txt

# Обновить PyTorch
pip install --upgrade torch torchvision

# Обновить Transformers
pip install --upgrade transformers
```

## Удаление

```bash
# Удалить виртуальное окружение
deactivate
rm -rf venv

# Удалить кэш моделей
rm -rf ~/.cache/huggingface
```

---

## 🙏 Готово!

После успешной установки:

1. Запустите `python demo_quickstart.py` для проверки
2. Изучите `QUICKSTART.md` для начала работы
3. Прочитайте `LEGAL_MODELS.md` для юридических моделей
4. Попробуйте примеры в `examples/`

**⚖️ Истина восторжествует! 🕉️ Харе Кришна!**





