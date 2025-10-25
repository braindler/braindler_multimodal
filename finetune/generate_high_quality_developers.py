#!/usr/bin/env python3
"""
Генерация высококачественного датасета для сфер разработки (073-078)

Использует GPT-4/Claude для создания качественных примеров
вместо сломанных примеров от Ollama

© 2025 NativeMind - NativeMindNONC License
"""

import json
import os
import requests
import time
from typing import List, Dict

def call_openai_api(prompt: str, model: str = "gpt-4") -> str:
    """Вызов OpenAI API для генерации качественных примеров"""
    try:
        # Здесь должен быть ваш API ключ OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return f"Ошибка: OPENAI_API_KEY не установлен"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": "Ты эксперт по разработке программного обеспечения. Создавай качественные, практичные примеры для обучения AI моделей."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"Ошибка API: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Ошибка: {e}"

def generate_sphere_073_developer() -> List[Dict]:
    """Генерация примеров для сферы 073: DEVELOPER"""
    print("💻 Генерация примеров для Сферы 073: DEVELOPER")
    
    prompts = [
        "Создай 10 примеров задач для Python разработчика с решениями. Включи: алгоритмы, структуры данных, ООП, асинхронное программирование, тестирование.",
        "Создай 10 примеров задач по веб-разработке на Python (Django/Flask) с полными решениями.",
        "Создай 10 примеров задач по работе с базами данных на Python с решениями.",
        "Создай 10 примеров задач по оптимизации производительности Python кода.",
        "Создай 10 примеров задач по работе с API и микросервисами на Python."
    ]
    
    examples = []
    for i, prompt in enumerate(prompts, 1):
        print(f"   📝 Генерация блока {i}/5...")
        response = call_openai_api(prompt)
        
        # Парсинг ответа на отдельные примеры
        if "Ошибка" not in response:
            # Разделяем на отдельные примеры
            parts = response.split("###") if "###" in response else [response]
            for part in parts:
                if len(part.strip()) > 50:  # Фильтруем слишком короткие части
                    examples.append({
                        "instruction": f"Задача разработчика: {part.strip()[:100]}...",
                        "input": "",
                        "output": part.strip(),
                        "sphere": "073",
                        "role": "developer",
                        "source": "gpt4_high_quality"
                    })
        
        time.sleep(1)  # Пауза между запросами
    
    print(f"   ✅ Сгенерировано {len(examples)} примеров")
    return examples

def generate_sphere_074_code_reviewer() -> List[Dict]:
    """Генерация примеров для сферы 074: CODE_REVIEWER"""
    print("🔍 Генерация примеров для Сферы 074: CODE_REVIEWER")
    
    prompts = [
        "Создай 10 примеров code review с плохим кодом и улучшенными версиями. Включи: производительность, безопасность, читаемость, архитектуру.",
        "Создай 10 примеров анализа кода на предмет уязвимостей и проблем безопасности.",
        "Создай 10 примеров рефакторинга кода с объяснением улучшений.",
        "Создай 10 примеров проверки кода на соответствие стандартам и лучшим практикам.",
        "Создай 10 примеров анализа архитектурных решений и предложений по улучшению."
    ]
    
    examples = []
    for i, prompt in enumerate(prompts, 1):
        print(f"   📝 Генерация блока {i}/5...")
        response = call_openai_api(prompt)
        
        if "Ошибка" not in response:
            parts = response.split("###") if "###" in response else [response]
            for part in parts:
                if len(part.strip()) > 50:
                    examples.append({
                        "instruction": f"Проверь этот код: {part.strip()[:100]}...",
                        "input": "",
                        "output": part.strip(),
                        "sphere": "074",
                        "role": "code_reviewer",
                        "source": "gpt4_high_quality"
                    })
        
        time.sleep(1)
    
    print(f"   ✅ Сгенерировано {len(examples)} примеров")
    return examples

def generate_sphere_075_architect() -> List[Dict]:
    """Генерация примеров для сферы 075: ARCHITECT"""
    print("🏗️ Генерация примеров для Сферы 075: ARCHITECT")
    
    prompts = [
        "Создай 10 примеров проектирования архитектуры микросервисов с диаграммами и объяснениями.",
        "Создай 10 примеров проектирования масштабируемых веб-приложений.",
        "Создай 10 примеров проектирования систем реального времени и высоконагруженных систем.",
        "Создай 10 примеров проектирования облачных архитектур (AWS, Azure, GCP).",
        "Создай 10 примеров проектирования систем с высокой доступностью и отказоустойчивостью."
    ]
    
    examples = []
    for i, prompt in enumerate(prompts, 1):
        print(f"   📝 Генерация блока {i}/5...")
        response = call_openai_api(prompt)
        
        if "Ошибка" not in response:
            parts = response.split("###") if "###" in response else [response]
            for part in parts:
                if len(part.strip()) > 50:
                    examples.append({
                        "instruction": f"Спроектируй архитектуру: {part.strip()[:100]}...",
                        "input": "",
                        "output": part.strip(),
                        "sphere": "075",
                        "role": "architect",
                        "source": "gpt4_high_quality"
                    })
        
        time.sleep(1)
    
    print(f"   ✅ Сгенерировано {len(examples)} примеров")
    return examples

def generate_sphere_076_devops() -> List[Dict]:
    """Генерация примеров для сферы 076: DEVOPS"""
    print("🚀 Генерация примеров для Сферы 076: DEVOPS")
    
    prompts = [
        "Создай 10 примеров настройки CI/CD pipeline с Docker, Jenkins, GitLab CI.",
        "Создай 10 примеров настройки мониторинга и логирования (Prometheus, Grafana, ELK).",
        "Создай 10 примеров настройки инфраструктуры как код (Terraform, Ansible).",
        "Создай 10 примеров настройки Kubernetes и оркестрации контейнеров.",
        "Создай 10 примеров настройки безопасности и compliance в DevOps."
    ]
    
    examples = []
    for i, prompt in enumerate(prompts, 1):
        print(f"   📝 Генерация блока {i}/5...")
        response = call_openai_api(prompt)
        
        if "Ошибка" not in response:
            parts = response.split("###") if "###" in response else [response]
            for part in parts:
                if len(part.strip()) > 50:
                    examples.append({
                        "instruction": f"Настрой DevOps: {part.strip()[:100]}...",
                        "input": "",
                        "output": part.strip(),
                        "sphere": "076",
                        "role": "devops",
                        "source": "gpt4_high_quality"
                    })
        
        time.sleep(1)
    
    print(f"   ✅ Сгенерировано {len(examples)} примеров")
    return examples

def generate_sphere_077_qa_tester() -> List[Dict]:
    """Генерация примеров для сферы 077: QA_TESTER"""
    print("🧪 Генерация примеров для Сферы 077: QA_TESTER")
    
    prompts = [
        "Создай 10 примеров написания unit тестов на Python (pytest, unittest) с полными тестами.",
        "Создай 10 примеров интеграционного тестирования API и веб-приложений.",
        "Создай 10 примеров тестирования производительности и нагрузочного тестирования.",
        "Создай 10 примеров автоматизации тестирования с Selenium, Playwright.",
        "Создай 10 примеров тестирования безопасности и penetration testing."
    ]
    
    examples = []
    for i, prompt in enumerate(prompts, 1):
        print(f"   📝 Генерация блока {i}/5...")
        response = call_openai_api(prompt)
        
        if "Ошибка" not in response:
            parts = response.split("###") if "###" in response else [response]
            for part in parts:
                if len(part.strip()) > 50:
                    examples.append({
                        "instruction": f"Напиши тесты: {part.strip()[:100]}...",
                        "input": "",
                        "output": part.strip(),
                        "sphere": "077",
                        "role": "qa_tester",
                        "source": "gpt4_high_quality"
                    })
        
        time.sleep(1)
    
    print(f"   ✅ Сгенерировано {len(examples)} примеров")
    return examples

def generate_sphere_078_tech_writer() -> List[Dict]:
    """Генерация примеров для сферы 078: TECH_WRITER"""
    print("📝 Генерация примеров для Сферы 078: TECH_WRITER")
    
    prompts = [
        "Создай 10 примеров технической документации для API с полными описаниями.",
        "Создай 10 примеров README файлов для проектов с подробными инструкциями.",
        "Создай 10 примеров архитектурной документации и диаграмм.",
        "Создай 10 примеров пользовательской документации и руководств.",
        "Создай 10 примеров документации по развертыванию и настройке систем."
    ]
    
    examples = []
    for i, prompt in enumerate(prompts, 1):
        print(f"   📝 Генерация блока {i}/5...")
        response = call_openai_api(prompt)
        
        if "Ошибка" not in response:
            parts = response.split("###") if "###" in response else [response]
            for part in parts:
                if len(part.strip()) > 50:
                    examples.append({
                        "instruction": f"Напиши документацию: {part.strip()[:100]}...",
                        "input": "",
                        "output": part.strip(),
                        "sphere": "078",
                        "role": "tech_writer",
                        "source": "gpt4_high_quality"
                    })
        
        time.sleep(1)
    
    print(f"   ✅ Сгенерировано {len(examples)} примеров")
    return examples

def main():
    print("==================================================================================")
    print("🌟 ГЕНЕРАЦИЯ ВЫСОКОКАЧЕСТВЕННОГО ДАТАСЕТА ДЛЯ СФЕР РАЗРАБОТКИ")
    print("==================================================================================")
    print()
    
    # Проверка API ключа
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Ошибка: OPENAI_API_KEY не установлен!")
        print("💡 Установите переменную окружения: export OPENAI_API_KEY='your-key'")
        return
    
    all_examples = []
    
    # Генерация для каждой сферы
    spheres = [
        ("073", generate_sphere_073_developer),
        ("074", generate_sphere_074_code_reviewer),
        ("075", generate_sphere_075_architect),
        ("076", generate_sphere_076_devops),
        ("077", generate_sphere_077_qa_tester),
        ("078", generate_sphere_078_tech_writer)
    ]
    
    for sphere_num, generator_func in spheres:
        print(f"\n{'='*60}")
        print(f"🎯 СФЕРА {sphere_num}")
        print(f"{'='*60}")
        
        examples = generator_func()
        all_examples.extend(examples)
        
        print(f"✅ Сфера {sphere_num}: {len(examples)} примеров")
    
    # Сохранение датасета
    output_file = "../datasets/developers_high_quality.jsonl"
    print(f"\n💾 Сохранение датасета в {output_file}...")
    
    with open(output_file, "w", encoding="utf-8") as f:
        for example in all_examples:
            f.write(json.dumps(example, ensure_ascii=False) + "\n")
    
    # Статистика
    print(f"\n📊 ИТОГОВАЯ СТАТИСТИКА:")
    print(f"   📝 Всего примеров: {len(all_examples)}")
    
    sphere_counts = {}
    for example in all_examples:
        sphere = example["sphere"]
        sphere_counts[sphere] = sphere_counts.get(sphere, 0) + 1
    
    for sphere, count in sorted(sphere_counts.items()):
        print(f"   🎯 Сфера {sphere}: {count} примеров")
    
    print(f"\n✅ Высококачественный датасет создан!")
    print(f"📁 Файл: {output_file}")
    print(f"🚀 Готов для переобучения моделей!")

if __name__ == "__main__":
    main()
