#!/usr/bin/env python3
"""
Обновление существующих моделей сфер разработки на HuggingFace

Обновляет уже существующие репозитории с улучшенными моделями

© 2025 NativeMind - NativeMindNONC License
"""

import os
import sys
import subprocess
import time
from typing import Dict, List

def check_model_exists(model_name: str) -> bool:
    """Проверка существования модели на HuggingFace"""
    try:
        result = subprocess.run(
            ["huggingface-cli", "repo", "info", model_name],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0
    except:
        return False

def update_model_on_huggingface(sphere: str, model_path: str, model_name: str):
    """Обновление одной модели на HuggingFace"""
    
    sphere_names = {
        "073": "DEVELOPER",
        "074": "CODE_REVIEWER", 
        "075": "ARCHITECT",
        "076": "DEVOPS",
        "077": "QA_TESTER",
        "078": "TECH_WRITER"
    }
    
    print(f"\n{'='*80}")
    print(f"🔄 ОБНОВЛЕНИЕ СФЕРЫ {sphere}: {sphere_names[sphere]}")
    print(f"{'='*80}")
    print(f"📦 Модель: {model_name}")
    print(f"📁 Путь: {model_path}")
    
    if not os.path.exists(model_path):
        print(f"❌ Модель не найдена: {model_path}")
        return False
    
    try:
        # Проверка существования репозитория
        print(f"\n🔍 Проверка существования репозитория {model_name}...")
        if not check_model_exists(model_name):
            print(f"❌ Репозиторий {model_name} не найден!")
            return False
        
        print(f"✅ Репозиторий {model_name} существует")
        
        # Клонирование репозитория
        print(f"\n📥 Клонирование репозитория...")
        clone_cmd = ["git", "clone", f"https://huggingface.co/{model_name}", f"temp_{sphere}"]
        result = subprocess.run(clone_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Ошибка клонирования: {result.stderr}")
            return False
        
        print("✅ Репозиторий клонирован")
        
        # Копирование файлов модели
        print(f"\n📋 Копирование файлов модели...")
        temp_dir = f"temp_{sphere}"
        
        # Копируем все файлы из model_path в temp_dir
        copy_cmd = ["cp", "-r", f"{model_path}/*", temp_dir]
        result = subprocess.run(copy_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Ошибка копирования: {result.stderr}")
            return False
        
        print("✅ Файлы скопированы")
        
        # Создание README с информацией об обновлении
        readme_content = f"""# Сфера {sphere}: {sphere_names[sphere]}

## 🚀 Обновленная модель

Эта модель была улучшена с использованием высококачественного датасета на основе nativemind/mozgach_alpaca_gift.

### Улучшения:
- ✅ Высококачественный датасет (200 примеров)
- ✅ Ролевые промпты для специализации
- ✅ Улучшенные параметры обучения (5 эпох, batch size 4)
- ✅ Расширенный контекст (4096 токенов)
- ✅ Оптимизированная LoRA конфигурация

### Ожидаемое качество: 8.0+/10

### Использование:
```python
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# Загрузка базовой модели
base_model = AutoModelForCausalLM.from_pretrained("nativemind/shridhar_8k_multimodal")
tokenizer = AutoTokenizer.from_pretrained("nativemind/shridhar_8k_multimodal")

# Загрузка LoRA адаптера
model = PeftModel.from_pretrained(base_model, "{model_name}")
```

### Специализация:
{sphere_names[sphere]} - специализированная модель для задач разработки

---
© 2025 NativeMind - NativeMindNONC License
"""
        
        with open(f"{temp_dir}/README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        print("✅ README обновлен")
        
        # Коммит и пуш изменений
        print(f"\n💾 Коммит и пуш изменений...")
        
        # Переход в директорию репозитория
        os.chdir(temp_dir)
        
        # Git add
        subprocess.run(["git", "add", "."], check=True)
        
        # Git commit
        commit_cmd = ["git", "commit", "-m", f"🚀 Обновление Сферы {sphere}: улучшенная модель с высококачественным датасетом"]
        result = subprocess.run(commit_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"⚠️  Коммит: {result.stderr}")
        
        # Git push
        push_cmd = ["git", "push"]
        result = subprocess.run(push_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Модель успешно обновлена на HuggingFace!")
        else:
            print(f"❌ Ошибка push: {result.stderr}")
            return False
        
        # Возврат в исходную директорию
        os.chdir("..")
        
        # Очистка временной директории
        subprocess.run(["rm", "-rf", temp_dir], check=True)
        
        print(f"✅ Сфера {sphere} ({sphere_names[sphere]}) обновлена!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при обновлении сферы {sphere}: {e}")
        return False

def main():
    """Основная функция обновления моделей"""
    print("==================================================================================")
    print("🔄 ОБНОВЛЕНИЕ СУЩЕСТВУЮЩИХ МОДЕЛЕЙ НА HUGGINGFACE")
    print("==================================================================================")
    print()
    
    # Существующие модели на HuggingFace
    existing_models = {
        "073": "nativemind/sphere_073_developer",
        "074": "nativemind/sphere_074_developer", 
        "075": "nativemind/sphere_075_developer",
        "076": "nativemind/sphere_076_developer",
        "077": "nativemind/sphere_077_developer",
        "078": "nativemind/sphere_078_developer"
    }
    
    # Проверка доступности улучшенных моделей
    models_dir = "../models_improved"
    available_models = []
    
    for sphere, model_name in existing_models.items():
        model_path = f"{models_dir}/sphere_{sphere}_improved"
        if os.path.exists(model_path):
            # Проверяем наличие файлов модели
            model_files = [f for f in os.listdir(model_path) 
                          if f.endswith(('.bin', '.safetensors', '.json'))]
            if model_files:
                available_models.append((sphere, model_path, model_name))
                print(f"✅ Сфера {sphere}: {model_name} - готова к обновлению")
            else:
                print(f"⏳ Сфера {sphere}: {model_name} - еще обучается")
        else:
            print(f"❌ Сфера {sphere}: {model_name} - не найдена")
    
    if not available_models:
        print("\n❌ Нет готовых моделей для обновления!")
        return
    
    print(f"\n📊 Найдено {len(available_models)} готовых моделей для обновления")
    
    # Обновление каждой модели
    results = {}
    
    for sphere, model_path, model_name in available_models:
        print(f"\n🚀 Обновление сферы {sphere}...")
        
        success = update_model_on_huggingface(sphere, model_path, model_name)
        results[sphere] = success
        
        if success:
            print(f"✅ Сфера {sphere} успешно обновлена!")
        else:
            print(f"❌ Ошибка обновления сферы {sphere}")
        
        # Пауза между обновлениями
        if sphere != available_models[-1][0]:  # Не последняя
            print("\n⏳ Пауза 30 секунд...")
            time.sleep(30)
    
    # Итоговый отчет
    print("\n" + "="*80)
    print("📊 ИТОГОВЫЙ ОТЧЕТ ОБНОВЛЕНИЯ")
    print("="*80)
    
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    
    print(f"✅ Успешно обновлено: {successful}/{total}")
    print()
    
    for sphere, success in results.items():
        model_name = existing_models[sphere]
        if success:
            status = "✅ УСПЕШНО"
            print(f"Сфера {sphere}: {status}")
            print(f"   🔗 https://huggingface.co/{model_name}")
        else:
            status = "❌ ОШИБКА"
            print(f"Сфера {sphere}: {status}")
        print()
    
    print("🙏 Обновление моделей завершено!")

if __name__ == "__main__":
    main()
