#!/usr/bin/env python3
"""
Публикация обученных сфер разработки (073-078) на HuggingFace

© 2025 NativeMind - NativeMindNONC License
"""

import os
import sys
import json
from huggingface_hub import HfApi, create_repo
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

def publish_sphere_model(sphere, model_path, repo_name, organization="nativemind"):
    """
    Публикация одной сферы на HuggingFace
    
    Args:
        sphere: Номер сферы
        model_path: Путь к обученной модели
        repo_name: Имя репозитория
        organization: Организация на HuggingFace
    """
    
    sphere_names = {
        "073": "DEVELOPER",
        "074": "CODE_REVIEWER", 
        "075": "ARCHITECT",
        "076": "DEVOPS",
        "077": "QA_TESTER",
        "078": "TECH_WRITER"
    }
    
    full_repo_name = f"{organization}/{repo_name}"
    
    print(f"\n{'='*80}")
    print(f"📤 ПУБЛИКАЦИЯ СФЕРЫ {sphere}: {sphere_names[sphere]}")
    print(f"{'='*80}")
    print(f"📦 Репозиторий: {full_repo_name}")
    print(f"📁 Модель: {model_path}")
    
    if not os.path.exists(model_path):
        print(f"❌ Модель не найдена: {model_path}")
        return False
    
    try:
        # Создание репозитория
        print("\n📁 Создание репозитория...")
        try:
            create_repo(
                repo_id=full_repo_name,
                private=False,
                exist_ok=True
            )
            print(f"   ✅ Репозиторий создан: {full_repo_name}")
        except Exception as e:
            print(f"   ⚠️  Репозиторий уже существует: {e}")
        
        # Инициализация API
        api = HfApi()
        
        # Загрузка файлов модели
        print("\n📤 Загрузка файлов модели...")
        
        # Основные файлы модели
        model_files = [
            "adapter_model.safetensors",
            "adapter_config.json",
            "tokenizer.json",
            "tokenizer_config.json",
            "special_tokens_map.json",
            "vocab.json"
        ]
        
        uploaded_files = []
        
        for file_name in model_files:
            file_path = os.path.join(model_path, file_name)
            if os.path.exists(file_path):
                print(f"   📤 Загружаем {file_name}...")
                api.upload_file(
                    path_or_fileobj=file_path,
                    path_in_repo=file_name,
                    repo_id=full_repo_name,
                    commit_message=f"Upload {file_name} for sphere {sphere}"
                )
                uploaded_files.append(file_name)
                print(f"   ✅ {file_name} загружен")
            else:
                print(f"   ⚠️  Файл не найден: {file_name}")
        
        # Создание README.md
        print("\n📝 Создание README.md...")
        
        readme_content = f"""# Сфера {sphere}: {sphere_names[sphere]}

Модель для сферы разработки {sphere} ({sphere_names[sphere]}), обученная на базе [nativemind/shridhar_8k_multimodal](https://huggingface.co/nativemind/shridhar_8k_multimodal).

## 🎯 Назначение

**Сфера {sphere} ({sphere_names[sphere]})** - специализированная модель для задач разработки программного обеспечения.

## 🚀 Использование

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# Загрузка базовой модели
base_model = AutoModelForCausalLM.from_pretrained("nativemind/shridhar_8k_multimodal")
tokenizer = AutoTokenizer.from_pretrained("nativemind/shridhar_8k_multimodal")

# Загрузка LoRA адаптера
model = PeftModel.from_pretrained(base_model, "{full_repo_name}")

# Генерация
prompt = "Напиши функцию на Python для сортировки массива"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=200, temperature=0.7)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
```

## 📊 Технические характеристики

- **Базовая модель**: nativemind/shridhar_8k_multimodal
- **Архитектура**: LoRA адаптация
- **Специализация**: {sphere_names[sphere]}
- **Языки**: Русский, английский
- **Контекст**: 8192 токена

## 🎯 Применение

Модель предназначена для:
- Разработки программного обеспечения
- Code review и анализа кода
- Архитектурного проектирования
- DevOps задач
- Тестирования
- Технического писательства

## 📚 Обучение

Модель обучена на датасете developers_108_perfect.jsonl с 108 примерами для сферы {sphere}.

## 📄 Лицензия

MIT License

---

**Автор**: NativeMind  
**Дата**: 25 октября 2025  
**Версия**: 1.0
"""
        
        # Сохранение README во временный файл
        readme_path = f"/tmp/readme_{sphere}.md"
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        # Загрузка README
        api.upload_file(
            path_or_fileobj=readme_path,
            path_in_repo="README.md",
            repo_id=full_repo_name,
            commit_message=f"Add README for sphere {sphere}"
        )
        print("   ✅ README.md загружен")
        
        # Удаление временного файла
        os.remove(readme_path)
        
        print(f"\n✅ Сфера {sphere} ({sphere_names[sphere]}) успешно опубликована!")
        print(f"🔗 Ссылка: https://huggingface.co/{full_repo_name}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Ошибка при публикации сферы {sphere}: {e}")
        return False

def main():
    print("==================================================================================")
    print("📤 ПУБЛИКАЦИЯ СФЕР РАЗРАБОТКИ НА HUGGINGFACE")
    print("==================================================================================")
    print()
    
    # Проверка доступности моделей
    models_dir = "../models"
    available_spheres = []
    
    for sphere in ["073", "074", "075", "076", "077", "078"]:
        model_path = f"{models_dir}/sphere_{sphere}_shridhar"
        if os.path.exists(model_path):
            available_spheres.append(sphere)
            print(f"✅ Сфера {sphere}: {model_path}")
        else:
            print(f"❌ Сфера {sphere}: не найдена")
    
    print(f"\n📊 Найдено {len(available_spheres)} обученных сфер")
    
    if not available_spheres:
        print("\n❌ Нет обученных моделей для публикации!")
        return
    
    # Публикация каждой доступной сферы
    results = {}
    
    for sphere in available_spheres:
        model_path = f"{models_dir}/sphere_{sphere}_shridhar"
        repo_name = f"sphere_{sphere}_developer"
        
        success = publish_sphere_model(
            sphere=sphere,
            model_path=model_path,
            repo_name=repo_name
        )
        results[sphere] = success
    
    # Итоговый отчет
    print("\n" + "="*80)
    print("📊 ИТОГОВЫЙ ОТЧЕТ ПУБЛИКАЦИИ")
    print("="*80)
    
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    
    print(f"✅ Успешно опубликовано: {successful}/{total}")
    print()
    
    for sphere, success in results.items():
        status = "✅ УСПЕШНО" if success else "❌ ОШИБКА"
        repo_link = f"https://huggingface.co/nativemind/sphere_{sphere}_developer"
        print(f"Сфера {sphere}: {status}")
        if success:
            print(f"   🔗 {repo_link}")
    
    print(f"\n🙏 Публикация завершена!")

if __name__ == "__main__":
    main()
