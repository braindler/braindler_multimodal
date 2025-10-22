#!/usr/bin/env python3
"""
Генерация ровно 108 примеров для разработчиков через Ollama

Использует локальную LLM для создания качественных синтетических примеров
для стандартного набора continue.ai

Духовное число: 108 примеров × 6 сфер + 1080 Alpaca = 1728 примеров

© 2025 NativeMind - NativeMindNONC License
"""

import json
import os
import subprocess
from pathlib import Path

def _ollama_bin():
    return os.environ.get("OLLAMA_BIN", "/opt/homebrew/bin/ollama")

def call_ollama(prompt, model="mozgach108:latest"):
    """Вызывает Ollama для генерации"""
    try:
        selected_model = os.environ.get("OLLAMA_MODEL", model)
        result = subprocess.run(
            [_ollama_bin(), "run", selected_model, prompt],
            capture_output=True,
            text=True,
            timeout=120
        )
        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()
        if result.returncode != 0:
            return f"Ошибка ollama (code {result.returncode}): {stderr or stdout}"
        return stdout or stderr
    except Exception as e:
        return f"Ошибка: {e}"

def generate_sphere_001_spiritual(target_count=108):
    """Генерация 108 духовных примеров (Сфера 001)"""
    print("\n🕉️  Генерация Сферы 001: ДУХОВНАЯ (108 примеров)")
    
    spiritual_prompts = [
        "Объясни значение истины в программировании",
        "Как служить справедливости через код",
        "В чем духовный смысл чистого кода",
        "Объясни карму технического долга",
        "Что значит истина в тестировании",
        "Как духовность связана с разработкой",
        "Объясни Дхарму программиста",
        "Что такое Сатва в служении пользователям",
        "Как медитация помогает разработчикам",
        "Объясни Ахимсу в code review"
    ]
    
    examples = []
    
    for i in range(target_count):
        prompt_template = spiritual_prompts[i % len(spiritual_prompts)]
        
        print(f"\r   Генерация {i+1}/{target_count}...", end='', flush=True)
        
        response = call_ollama(f"{prompt_template}. Ответь кратко, 2-3 предложения.")
        
        examples.append({
            "instruction": prompt_template,
            "input": "",
            "output": response,
            "sphere": "001",
            "role": "spiritual",
            "source": "synthetic_ollama"
        })
    
    print(f"\n   ✅ Сфера 001: {len(examples)} примеров")
    return examples

def generate_sphere_073_developer(target_count=108):
    """Генерация 108 примеров ПРОГРАММИСТА (Сфера 073)"""
    print("\n💻 Генерация Сферы 073: ПРОГРАММИСТ (108 примеров)")
    
    prompts_templates = [
        "Напиши функцию для обработки данных",
        "Оптимизируй этот алгоритм",
        "Исправь баг в коде",
        "Добавь обработку ошибок",
        "Рефактори этот код",
        "Реализуй паттерн проектирования",
        "Напиши unit-тест",
        "Улучши читаемость кода",
        "Оптимизируй производительность",
        "Добавь валидацию входных данных"
    ]
    
    code_contexts = [
        "def process_data(data): return data",
        "for i in range(len(arr)): print(arr[i])",
        "if x == True: return y",
        "try: do_something() except: pass",
        "class MyClass: pass",
        "def calculate(a, b): return a + b",
        "result = [x for x in range(100)]",
        "while True: continue",
        "import *",
        "global variable = 10"
    ]
    
    examples = []
    
    for i in range(target_count):
        template = prompts_templates[i % len(prompts_templates)]
        context = code_contexts[i % len(code_contexts)]
        
        print(f"\r   Генерация {i+1}/{target_count}...", end='', flush=True)
        
        full_prompt = f"""Ты - ПРОГРАММИСТ (Сфера 073).

Духовная миссия: Создание чистого, эффективного кода.

Задача: {template}

Код: {context}

Дай решение программиста (2-3 предложения + код если нужно):"""
        
        response = call_ollama(full_prompt)
        
        examples.append({
            "instruction": f"Ты - ПРОГРАММИСТ. {template}",
            "input": context,
            "output": response,
            "sphere": "073",
            "role": "sphere_073_developer",
            "source": "synthetic_ollama"
        })
    
    print(f"\n   ✅ Сфера 073: {len(examples)} примеров")
    return examples

def generate_sphere_074_code_reviewer(target_count=108):
    """Генерация 108 примеров CODE REVIEWER (Сфера 074)"""
    print("\n🔍 Генерация Сферы 074: CODE REVIEWER (108 примеров)")
    
    prompts_templates = [
        "Проверь безопасность кода",
        "Найди потенциальные баги",
        "Оцени читаемость кода",
        "Проверь соответствие стандартам",
        "Найди проблемы производительности",
        "Оцени тестовое покрытие",
        "Проверь обработку ошибок",
        "Найди code smells",
        "Оцени архитектурные решения",
        "Проверь документацию"
    ]
    
    code_samples = [
        "def login(user, pwd): return user == 'admin' and pwd == '123'",
        "data = json.loads(request.body); db.execute(f'SELECT * FROM users WHERE id={data['id']}')",
        "def process(): global result; result = complicated_calculation()",
        "try: file = open('data.txt'); data = file.read() except: pass",
        "class UserManager: def __init__(self): self.users = []; self.admins = []; self.guests = []",
        "def calculate(x, y, z, a, b, c, d, e, f): return x+y+z+a+b+c+d+e+f",
        "password = request.GET['password']; user.password = password",
        "while True: try: process(); break; except: continue",
        "def func(x): return func(x-1) if x > 0 else 0",
        "data = None; if data: print(data.value)"
    ]
    
    examples = []
    
    for i in range(target_count):
        template = prompts_templates[i % len(prompts_templates)]
        code = code_samples[i % len(code_samples)]
        
        print(f"\r   Генерация {i+1}/{target_count}...", end='', flush=True)
        
        full_prompt = f"""Ты - CODE REVIEWER (Сфера 074).

Духовная миссия: Обеспечение качества и безопасности кода.

Задача: {template}

Код на ревью:
```
{code}
```

Дай code review (3-4 предложения с замечаниями):"""
        
        response = call_ollama(full_prompt)
        
        examples.append({
            "instruction": f"Ты - CODE REVIEWER. {template}",
            "input": code,
            "output": response,
            "sphere": "074",
            "role": "sphere_074_code_reviewer",
            "source": "synthetic_ollama"
        })
    
    print(f"\n   ✅ Сфера 074: {len(examples)} примеров")
    return examples

def generate_sphere_075_architect(target_count=108):
    """Генерация 108 примеров АРХИТЕКТОРА (Сфера 075)"""
    print("\n🏗️  Генерация Сферы 075: АРХИТЕКТОР (108 примеров)")
    
    prompts_templates = [
        "Спроектируй микросервисную архитектуру",
        "Выбери подходящий паттерн проектирования",
        "Спроектируй базу данных",
        "Оцени масштабируемость решения",
        "Выбери технологический стек",
        "Спроектируй API",
        "Оцени надежность системы",
        "Спроектируй систему кеширования",
        "Выбери подход к аутентификации",
        "Спроектируй message queue архитектуру"
    ]
    
    requirements = [
        "Система должна обрабатывать 10000 запросов в секунду",
        "Нужна высокая доступность 99.99%",
        "Требуется real-time обработка данных",
        "Система должна хранить петабайты данных",
        "Нужна поддержка мобильных и веб-клиентов",
        "Требуется географическое распределение",
        "Система должна быть легко расширяемой",
        "Нужна изоляция сервисов",
        "Требуется асинхронная обработка",
        "Система должна быть fault-tolerant"
    ]
    
    examples = []
    
    for i in range(target_count):
        template = prompts_templates[i % len(prompts_templates)]
        requirement = requirements[i % len(requirements)]
        
        print(f"\r   Генерация {i+1}/{target_count}...", end='', flush=True)
        
        full_prompt = f"""Ты - АРХИТЕКТОР ПО (Сфера 075).

Духовная миссия: Проектирование надежных, масштабируемых систем.

Задача: {template}

Требования: {requirement}

Дай архитектурное решение (3-4 предложения):"""
        
        response = call_ollama(full_prompt)
        
        examples.append({
            "instruction": f"Ты - АРХИТЕКТОР. {template}",
            "input": requirement,
            "output": response,
            "sphere": "075",
            "role": "sphere_075_architect",
            "source": "synthetic_ollama"
        })
    
    print(f"\n   ✅ Сфера 075: {len(examples)} примеров")
    return examples

def generate_sphere_076_devops(target_count=108):
    """Генерация 108 примеров DEVOPS (Сфера 076)"""
    print("\n⚙️  Генерация Сферы 076: DEVOPS ENGINEER (108 примеров)")
    
    prompts_templates = [
        "Настрой CI/CD pipeline",
        "Оптимизируй Docker образ",
        "Настрой мониторинг системы",
        "Автоматизируй деплой",
        "Настрой автоскейлинг",
        "Оптимизируй использование ресурсов",
        "Настрой логирование",
        "Реализуй blue-green deployment",
        "Настрой backup стратегию",
        "Оптимизируй сетевую конфигурацию"
    ]
    
    infrastructure = [
        "Kubernetes кластер на 50 нодах",
        "AWS инфраструктура с Lambda и ECS",
        "Docker Compose с 10 сервисами",
        "GitLab CI с множественными стейджами",
        "Terraform конфигурация для облака",
        "Ansible playbooks для деплоя",
        "Jenkins pipeline с тестами",
        "Prometheus + Grafana стек",
        "ELK stack для логов",
        "Redis кластер для кеширования"
    ]
    
    examples = []
    
    for i in range(target_count):
        template = prompts_templates[i % len(prompts_templates)]
        infra = infrastructure[i % len(infrastructure)]
        
        print(f"\r   Генерация {i+1}/{target_count}...", end='', flush=True)
        
        full_prompt = f"""Ты - DEVOPS ENGINEER (Сфера 076).

Духовная миссия: Автоматизация и надежность инфраструктуры.

Задача: {template}

Инфраструктура: {infra}

Дай DevOps решение (3-4 предложения):"""
        
        response = call_ollama(full_prompt)
        
        examples.append({
            "instruction": f"Ты - DEVOPS. {template}",
            "input": infra,
            "output": response,
            "sphere": "076",
            "role": "sphere_076_devops",
            "source": "synthetic_ollama"
        })
    
    print(f"\n   ✅ Сфера 076: {len(examples)} примеров")
    return examples

def generate_sphere_077_qa_tester(target_count=108):
    """Генерация 108 примеров QA TESTER (Сфера 077)"""
    print("\n🧪 Генерация Сферы 077: QA TESTER (108 примеров)")
    
    prompts_templates = [
        "Составь тест-план",
        "Найди edge cases",
        "Напиши автотесты",
        "Проверь граничные условия",
        "Составь тест-кейсы",
        "Проверь производительность",
        "Найди регрессии",
        "Проверь безопасность",
        "Составь тест-данные",
        "Проверь интеграции"
    ]
    
    features = [
        "Функция авторизации пользователей",
        "API endpoint для создания заказов",
        "Форма регистрации с валидацией",
        "Корзина покупок с промокодами",
        "Система поиска с фильтрами",
        "Загрузка и обработка файлов",
        "Real-time чат между пользователями",
        "Система уведомлений",
        "Экспорт данных в CSV/PDF",
        "Мультиязычный интерфейс"
    ]
    
    examples = []
    
    for i in range(target_count):
        template = prompts_templates[i % len(prompts_templates)]
        feature = features[i % len(features)]
        
        print(f"\r   Генерация {i+1}/{target_count}...", end='', flush=True)
        
        full_prompt = f"""Ты - QA TESTER (Сфера 077).

Духовная миссия: Обеспечение качества через тщательное тестирование.

Задача: {template}

Функционал: {feature}

Дай тестовое решение (3-4 предложения):"""
        
        response = call_ollama(full_prompt)
        
        examples.append({
            "instruction": f"Ты - QA TESTER. {template}",
            "input": feature,
            "output": response,
            "sphere": "077",
            "role": "sphere_077_qa_tester",
            "source": "synthetic_ollama"
        })
    
    print(f"\n   ✅ Сфера 077: {len(examples)} примеров")
    return examples

def generate_sphere_078_tech_writer(target_count=108):
    """Генерация 108 примеров TECHNICAL WRITER (Сфера 078)"""
    print("\n📝 Генерация Сферы 078: TECHNICAL WRITER (108 примеров)")
    
    prompts_templates = [
        "Напиши API документацию",
        "Создай README для проекта",
        "Напиши руководство пользователя",
        "Документируй архитектуру",
        "Напиши changelog",
        "Создай getting started guide",
        "Напиши troubleshooting секцию",
        "Документируй deployment процесс",
        "Напиши contributing guidelines",
        "Создай FAQ секцию"
    ]
    
    projects = [
        "REST API для e-commerce платформы",
        "Open-source библиотека для машинного обучения",
        "Микросервис для обработки платежей",
        "CLI инструмент для автоматизации",
        "React компонентная библиотека",
        "Python SDK для облачного сервиса",
        "GraphQL API сервер",
        "Docker образ с приложением",
        "CI/CD pipeline конфигурация",
        "Kubernetes оператор"
    ]
    
    examples = []
    
    for i in range(target_count):
        template = prompts_templates[i % len(prompts_templates)]
        project = projects[i % len(projects)]
        
        print(f"\r   Генерация {i+1}/{target_count}...", end='', flush=True)
        
        full_prompt = f"""Ты - TECHNICAL WRITER (Сфера 078).

Духовная миссия: Создание ясной, понятной документации.

Задача: {template}

Проект: {project}

Дай пример документации (3-4 предложения):"""
        
        response = call_ollama(full_prompt)
        
        examples.append({
            "instruction": f"Ты - TECHNICAL WRITER. {template}",
            "input": project,
            "output": response,
            "sphere": "078",
            "role": "sphere_078_tech_writer",
            "source": "synthetic_ollama"
        })
    
    print(f"\n   ✅ Сфера 078: {len(examples)} примеров")
    return examples

def main():
    """Главная функция генерации"""
    print("="*80)
    print("🌟 Генерация 108 примеров для разработчиков (continue.ai набор)")
    print("="*80)
    print()
    print("🙏 Священное число 108 в каждой сфере")
    print()
    
    # Проверяем Ollama
    try:
        result = subprocess.run([_ollama_bin(), "--version"], capture_output=True, text=True)
        ver = (result.stdout or result.stderr or "").strip()
        print(f"✅ Ollama доступен: {ver}")
        print(f"🧠 Модель: {os.environ.get('OLLAMA_MODEL', 'mozgach108:latest')}")
    except Exception as e:
        print(f"❌ Ошибка Ollama: {e}")
        return
    
    # Генерируем для каждой сферы
    all_examples = []
    
    # Сфера 001: Духовная (108)
    all_examples.extend(generate_sphere_001_spiritual(108))
    
    # Сфера 073: ПРОГРАММИСТ (108)
    all_examples.extend(generate_sphere_073_developer(108))
    
    # Сфера 074: CODE REVIEWER (108)
    all_examples.extend(generate_sphere_074_code_reviewer(108))
    
    # Сфера 075: АРХИТЕКТОР (108)
    all_examples.extend(generate_sphere_075_architect(108))
    
    # Сфера 076: DEVOPS (108)
    all_examples.extend(generate_sphere_076_devops(108))
    
    # Сфера 077: QA TESTER (108)
    all_examples.extend(generate_sphere_077_qa_tester(108))
    
    # Сфера 078: TECHNICAL WRITER (108)
    all_examples.extend(generate_sphere_078_tech_writer(108))
    
    # Загружаем Alpaca (1080 примеров)
    print("\n🦙 Загрузка Alpaca (1080 примеров)...")
    alpaca_path = "/Volumes/MULTIMODAL/proj.datasets/alpaca_dataset/alpaca_data.json"
    
    if os.path.exists(alpaca_path):
        with open(alpaca_path, 'r', encoding='utf-8') as f:
            alpaca_data = json.load(f)
        
        # Фильтруем примеры связанные с программированием
        keywords = ['code', 'program', 'function', 'algorithm', 'debug', 'optimize', 
                   'design', 'implement', 'develop', 'software', 'api', 'test']
        alpaca_filtered = [ex for ex in alpaca_data 
                          if any(kw in ex['instruction'].lower() for kw in keywords)][:1080]
        
        for ex in alpaca_filtered:
            all_examples.append({
                "instruction": ex['instruction'],
                "input": ex.get('input', ''),
                "output": ex['output'],
                "sphere": "general",
                "role": "general",
                "source": "alpaca"
            })
        
        print(f"   ✅ Alpaca: {len(alpaca_filtered)} примеров")
    else:
        print(f"   ⚠️  Alpaca датасет не найден по пути: {alpaca_path}")
    
    # Сохраняем
    output_path = "../datasets/developers_108_perfect.jsonl"
    
    print(f"\n💾 Сохранение датасета...")
    with open(output_path, 'w', encoding='utf-8') as f:
        for ex in all_examples:
            f.write(json.dumps(ex, ensure_ascii=False) + '\n')
    
    # Статистика
    stats = {
        "total": len(all_examples),
        "distribution": {
            "001_spiritual": len([e for e in all_examples if e['sphere'] == '001']),
            "073_developer": len([e for e in all_examples if e['sphere'] == '073']),
            "074_code_reviewer": len([e for e in all_examples if e['sphere'] == '074']),
            "075_architect": len([e for e in all_examples if e['sphere'] == '075']),
            "076_devops": len([e for e in all_examples if e['sphere'] == '076']),
            "077_qa_tester": len([e for e in all_examples if e['sphere'] == '077']),
            "078_tech_writer": len([e for e in all_examples if e['sphere'] == '078']),
            "general_alpaca": len([e for e in all_examples if e['sphere'] == 'general'])
        }
    }
    
    stats_path = output_path.replace('.jsonl', '_stats.json')
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ Сохранено: {output_path}")
    print()
    print("="*80)
    print("✅ ДАТАСЕТ ДЛЯ РАЗРАБОТЧИКОВ ГОТОВ!")
    print("="*80)
    print()
    print("📊 Распределение (священное 108):")
    for sphere, count in stats['distribution'].items():
        print(f"   {sphere}: {count}")
    print()
    print(f"📦 Всего примеров: {stats['total']}")
    print()
    print("🙏 108 - священное число в каждой сфере разработки!")
    print("💻 Готово для continue.ai!")

if __name__ == "__main__":
    main()



