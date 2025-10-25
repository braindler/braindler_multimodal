#!/usr/bin/env python3
"""
Создание высококачественного датасета для сфер разработки (073-078)
на основе nativemind/mozgach_alpaca_gift

Использует существующий качественный датасет как основу и адаптирует его
для специализированных сфер разработки

© 2025 NativeMind - NativeMindNONC License
"""

import json
import os
import random
from datasets import load_dataset
from typing import List, Dict

def load_mozgach_dataset():
    """Загрузка базового датасета mozgach_alpaca_gift"""
    print("📥 Загрузка базового датасета mozgach_alpaca_gift...")
    try:
        dataset = load_dataset("nativemind/mozgach_alpaca_gift", split="train")
        print(f"   ✅ Загружено {len(dataset)} примеров")
        return dataset
    except Exception as e:
        print(f"   ❌ Ошибка загрузки: {e}")
        return None

def create_developer_examples(base_dataset, sphere, count=200):
    """Создание примеров для сферы разработки на основе базового датасета"""
    
    sphere_configs = {
        "073": {
            "name": "DEVELOPER",
            "keywords": ["код", "программирование", "разработка", "функция", "алгоритм", "python", "javascript", "java", "git", "api"],
            "role_prompt": "### Роль: Senior Python Developer\n### Задача: {instruction}\n### Решение:",
            "examples": [
                "Напиши функцию на Python для сортировки массива",
                "Создай класс для работы с базой данных",
                "Оптимизируй производительность этого кода",
                "Реализуй паттерн Singleton на Python",
                "Создай REST API с использованием Flask"
            ]
        },
        "074": {
            "name": "CODE_REVIEWER", 
            "keywords": ["код", "проверка", "ошибка", "баг", "рефакторинг", "качество", "стандарты", "безопасность"],
            "role_prompt": "### Роль: Code Reviewer\n### Код для проверки: {instruction}\n### Анализ:",
            "examples": [
                "Проверь этот код на наличие ошибок",
                "Найди проблемы производительности в этом коде",
                "Проверь соответствие стандартам кодирования",
                "Выяви уязвимости безопасности",
                "Предложи улучшения архитектуры"
            ]
        },
        "075": {
            "name": "ARCHITECT",
            "keywords": ["архитектура", "система", "микросервисы", "масштабирование", "паттерны", "дизайн", "инфраструктура"],
            "role_prompt": "### Роль: System Architect\n### Требования: {instruction}\n### Архитектурное решение:",
            "examples": [
                "Спроектируй архитектуру микросервисов",
                "Создай масштабируемую систему для 1M пользователей",
                "Спроектируй систему реального времени",
                "Выбери подходящие технологии для проекта",
                "Создай архитектуру для высоконагруженной системы"
            ]
        },
        "076": {
            "name": "DEVOPS",
            "keywords": ["devops", "ci/cd", "docker", "kubernetes", "мониторинг", "развертывание", "автоматизация", "инфраструктура"],
            "role_prompt": "### Роль: DevOps Engineer\n### Задача: {instruction}\n### Решение:",
            "examples": [
                "Настрой CI/CD pipeline для Python проекта",
                "Создай Docker контейнер для приложения",
                "Настрой мониторинг производительности",
                "Автоматизируй развертывание в Kubernetes",
                "Настрой безопасность инфраструктуры"
            ]
        },
        "077": {
            "name": "QA_TESTER",
            "keywords": ["тестирование", "тесты", "qa", "баг", "качество", "автоматизация", "покрытие", "проверка"],
            "role_prompt": "### Роль: QA Engineer\n### Задача: {instruction}\n### Тестовое решение:",
            "examples": [
                "Напиши unit тесты для этой функции",
                "Создай план тестирования для API",
                "Автоматизируй тестирование UI",
                "Проверь покрытие кода тестами",
                "Создай тесты производительности"
            ]
        },
        "078": {
            "name": "TECH_WRITER",
            "keywords": ["документация", "readme", "api", "руководство", "техническая", "писательство", "объяснение"],
            "role_prompt": "### Роль: Technical Writer\n### Задача: {instruction}\n### Документация:",
            "examples": [
                "Напиши техническую документацию для API",
                "Создай README для проекта",
                "Напиши руководство пользователя",
                "Создай архитектурную документацию",
                "Напиши инструкцию по развертыванию"
            ]
        }
    }
    
    config = sphere_configs[sphere]
    print(f"\n🎯 Создание примеров для Сферы {sphere}: {config['name']}")
    
    # Фильтрация базового датасета по ключевым словам
    relevant_examples = []
    for example in base_dataset:
        instruction = example.get('instruction', '').lower()
        output = example.get('output', '').lower()
        text = f"{instruction} {output}"
        
        # Проверка на наличие ключевых слов
        if any(keyword in text for keyword in config['keywords']):
            relevant_examples.append(example)
    
    print(f"   📊 Найдено {len(relevant_examples)} релевантных примеров")
    
    # Если недостаточно примеров, дополняем синтетическими
    synthetic_examples = []
    if len(relevant_examples) < count:
        needed = count - len(relevant_examples)
        print(f"   🔧 Создание {needed} синтетических примеров...")
        
        for i in range(needed):
            base_example = random.choice(base_dataset)
            synthetic_instruction = random.choice(config['examples'])
            
            synthetic_examples.append({
                "instruction": synthetic_instruction,
                "input": "",
                "output": base_example.get('output', ''),
                "sphere": sphere,
                "role": config['name'].lower(),
                "source": "synthetic_from_mozgach"
            })
    
    # Адаптация примеров для сферы
    adapted_examples = []
    for example in relevant_examples[:count-len(synthetic_examples)]:
        adapted_examples.append({
            "instruction": example.get('instruction', ''),
            "input": example.get('input', ''),
            "output": example.get('output', ''),
            "sphere": sphere,
            "role": config['name'].lower(),
            "source": "mozgach_alpaca_gift"
        })
    
    # Объединение адаптированных и синтетических примеров
    all_examples = adapted_examples + synthetic_examples
    random.shuffle(all_examples)
    
    print(f"   ✅ Создано {len(all_examples)} примеров")
    return all_examples

def enhance_examples_with_role_prompts(examples, sphere):
    """Улучшение примеров с добавлением ролевых промптов"""
    
    sphere_configs = {
        "073": "### Роль: Senior Python Developer",
        "074": "### Роль: Code Reviewer", 
        "075": "### Роль: System Architect",
        "076": "### Роль: DevOps Engineer",
        "077": "### Роль: QA Engineer",
        "078": "### Роль: Technical Writer"
    }
    
    role_prompt = sphere_configs[sphere]
    
    enhanced_examples = []
    for example in examples:
        # Добавляем ролевой промпт к инструкции
        enhanced_instruction = f"{role_prompt}\n### Задача:\n{example['instruction']}"
        
        enhanced_examples.append({
            "instruction": enhanced_instruction,
            "input": example.get('input', ''),
            "output": example['output'],
            "sphere": sphere,
            "role": example['role'],
            "source": example['source']
        })
    
    return enhanced_examples

def create_high_quality_dataset():
    """Создание высококачественного датасета для всех сфер"""
    print("==================================================================================")
    print("🌟 СОЗДАНИЕ ВЫСОКОКАЧЕСТВЕННОГО ДАТАСЕТА НА ОСНОВЕ MOZGACH_ALPACA_GIFT")
    print("==================================================================================")
    print()
    
    # Загрузка базового датасета
    base_dataset = load_mozgach_dataset()
    if not base_dataset:
        print("❌ Не удалось загрузить базовый датасет!")
        return
    
    all_examples = []
    spheres = ["073", "074", "075", "076", "077", "078"]
    
    # Создание примеров для каждой сферы
    for sphere in spheres:
        print(f"\n{'='*60}")
        print(f"🎯 СФЕРА {sphere}")
        print(f"{'='*60}")
        
        # Создание примеров
        examples = create_developer_examples(base_dataset, sphere, count=200)
        
        # Улучшение с ролевыми промптами
        enhanced_examples = enhance_examples_with_role_prompts(examples, sphere)
        
        all_examples.extend(enhanced_examples)
        print(f"✅ Сфера {sphere}: {len(enhanced_examples)} примеров")
    
    # Сохранение датасета
    output_file = "../datasets/developers_high_quality_from_mozgach.jsonl"
    print(f"\n💾 Сохранение датасета в {output_file}...")
    
    with open(output_file, "w", encoding="utf-8") as f:
        for example in all_examples:
            f.write(json.dumps(example, ensure_ascii=False) + "\n")
    
    # Статистика
    print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА:")
    print(f"   📝 Всего примеров: {len(all_examples)}")
    
    sphere_counts = {}
    source_counts = {}
    
    for example in all_examples:
        sphere = example["sphere"]
        source = example["source"]
        sphere_counts[sphere] = sphere_counts.get(sphere, 0) + 1
        source_counts[source] = source_counts.get(source, 0) + 1
    
    print(f"\n   🎯 По сферам:")
    for sphere, count in sorted(sphere_counts.items()):
        print(f"      Сфера {sphere}: {count} примеров")
    
    print(f"\n   📚 По источникам:")
    for source, count in sorted(source_counts.items()):
        print(f"      {source}: {count} примеров")
    
    print(f"\n✅ Высококачественный датасет создан!")
    print(f"📁 Файл: {output_file}")
    print(f"🚀 Готов для переобучения моделей!")
    
    return output_file

def main():
    create_high_quality_dataset()

if __name__ == "__main__":
    main()
