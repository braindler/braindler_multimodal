#!/usr/bin/env python3
"""
Тестирование обученных сфер разработки (073-078)

© 2025 NativeMind - NativeMindNONC License
"""

import os
import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import json

def test_sphere_model(sphere, model_path, test_prompts):
    """
    Тестирование одной сферы
    
    Args:
        sphere: Номер сферы
        model_path: Путь к обученной модели
        test_prompts: Список тестовых промптов
    """
    
    sphere_names = {
        "073": "DEVELOPER",
        "074": "CODE_REVIEWER", 
        "075": "ARCHITECT",
        "076": "DEVOPS",
        "077": "QA_TESTER",
        "078": "TECH_WRITER"
    }
    
    print(f"\n{'='*80}")
    print(f"🧪 ТЕСТИРОВАНИЕ СФЕРЫ {sphere}: {sphere_names[sphere]}")
    print(f"{'='*80}")
    
    if not os.path.exists(model_path):
        print(f"❌ Модель не найдена: {model_path}")
        return False
    
    try:
        # Загрузка токенизатора
        print("📥 Загрузка токенизатора...")
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        print("   ✅ Токенизатор загружен")
        
        # Загрузка базовой модели
        print("📥 Загрузка базовой модели...")
        base_model = AutoModelForCausalLM.from_pretrained(
            "nativemind/shridhar_8k_multimodal",
            torch_dtype=torch.float32,  # Используем float32 для стабильности
            device_map=None  # Загружаем на CPU для стабильности
        )
        
        # Загрузка LoRA адаптера
        print("📥 Загрузка LoRA адаптера...")
        model = PeftModel.from_pretrained(base_model, model_path)
        print("   ✅ Модель загружена")
        
        # Тестирование
        print(f"\n🧪 Тестирование {len(test_prompts)} промптов...")
        
        for i, prompt in enumerate(test_prompts, 1):
            print(f"\n--- Тест {i} ---")
            print(f"Промпт: {prompt}")
            
            # Токенизация
            inputs = tokenizer(prompt, return_tensors="pt")
            # Оставляем на CPU для стабильности
            
            # Генерация
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=200,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            # Декодирование
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = response[len(prompt):].strip()
            
            print(f"Ответ: {response}")
            print("-" * 50)
        
        print(f"\n✅ Сфера {sphere} ({sphere_names[sphere]}) протестирована успешно!")
        return True
        
    except Exception as e:
        print(f"\n❌ Ошибка при тестировании сферы {sphere}: {e}")
        return False

def main():
    # Тестовые промпты для каждой сферы
    test_prompts = {
        "073": [
            "Напиши функцию на Python для сортировки массива",
            "Как оптимизировать SQL запрос?",
            "Объясни принципы SOLID в программировании"
        ],
        "074": [
            "Проверь этот код на наличие ошибок",
            "Какие проблемы видишь в этой архитектуре?",
            "Как улучшить читаемость этого кода?"
        ],
        "075": [
            "Спроектируй архитектуру микросервисов",
            "Как организовать масштабируемую систему?",
            "Какие паттерны использовать для распределенной системы?"
        ],
        "076": [
            "Настрой CI/CD pipeline для Python проекта",
            "Как мониторить производительность приложения?",
            "Обеспечь безопасность Docker контейнеров"
        ],
        "077": [
            "Напиши unit тесты для этой функции",
            "Как протестировать интеграцию с API?",
            "Проверь покрытие кода тестами"
        ],
        "078": [
            "Напиши техническую документацию для API",
            "Создай README для проекта",
            "Объясни архитектуру системы для новых разработчиков"
        ]
    }
    
    print("==================================================================================")
    print("🧪 ТЕСТИРОВАНИЕ ВСЕХ СФЕР РАЗРАБОТКИ")
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
        print("\n❌ Нет обученных моделей для тестирования!")
        return
    
    # Тестирование каждой доступной сферы
    results = {}
    
    for sphere in available_spheres:
        model_path = f"{models_dir}/sphere_{sphere}_shridhar"
        success = test_sphere_model(
            sphere, 
            model_path, 
            test_prompts[sphere]
        )
        results[sphere] = success
    
    # Итоговый отчет
    print("\n" + "="*80)
    print("📊 ИТОГОВЫЙ ОТЧЕТ ТЕСТИРОВАНИЯ")
    print("="*80)
    
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    
    print(f"✅ Успешно протестировано: {successful}/{total}")
    print()
    
    for sphere, success in results.items():
        status = "✅ УСПЕШНО" if success else "❌ ОШИБКА"
        print(f"Сфера {sphere}: {status}")
    
    print(f"\n🙏 Тестирование завершено!")

if __name__ == "__main__":
    main()
