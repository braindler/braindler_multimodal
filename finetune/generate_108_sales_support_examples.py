#!/usr/bin/env python3
"""
Генерация ровно 108 примеров для Sales & Support через Ollama

Использует локальную LLM для создания качественных синтетических примеров
для моделей продаж и поддержки клиентов

Духовное число: 108 примеров × 8 сфер + 1080 Alpaca = 1944 примера

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
        "Объясни значение истины в продажах",
        "Как служить клиентам с духовной точки зрения",
        "В чем духовный смысл честности в бизнесе",
        "Объясни карму в отношениях с клиентами",
        "Что значит истина в обещаниях клиентам",
        "Как духовность связана с продажами",
        "Объясни Дхарму менеджера по продажам",
        "Что такое Сатва в служении клиентам",
        "Как медитация помогает в переговорах",
        "Объясни Ахимсу в работе с возражениями"
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

def generate_sphere_019_sales_manager(target_count=108):
    """Генерация 108 примеров SALES MANAGER (Сфера 019)"""
    print("\n💼 Генерация Сферы 019: SALES MANAGER (108 примеров)")
    
    prompts_templates = [
        "Выяви потребность клиента",
        "Закрой возражение",
        "Проведи квалификацию лида",
        "Составь коммерческое предложение",
        "Проведи холодный звонок",
        "Закрой сделку",
        "Обработай отказ",
        "Выяви боль клиента",
        "Презентуй продукт через ценность",
        "Задай SPIN-вопросы"
    ]
    
    client_situations = [
        "Клиент говорит: 'Дорого'",
        "Клиент: 'Мне нужно подумать'",
        "Входящий лид без прогрева",
        "Клиент сравнивает с конкурентами",
        "Клиент не видит ценности",
        "Клиент хочет скидку 50%",
        "Клиент не отвечает на письма",
        "Клиент: 'У нас нет бюджета'",
        "Клиент просит отправить информацию",
        "Клиент на этапе выбора решения"
    ]
    
    examples = []
    
    for i in range(target_count):
        template = prompts_templates[i % len(prompts_templates)]
        situation = client_situations[i % len(client_situations)]
        
        print(f"\r   Генерация {i+1}/{target_count}...", end='', flush=True)
        
        full_prompt = f"""Ты - SALES MANAGER (Сфера 019).

Духовная миссия: Выявление истинных потребностей клиента и закрытие через ценность.

Задача: {template}

Ситуация: {situation}

Дай решение менеджера по продажам (3-4 предложения):"""
        
        response = call_ollama(full_prompt)
        
        examples.append({
            "instruction": f"Ты - SALES MANAGER. {template}",
            "input": situation,
            "output": response,
            "sphere": "019",
            "role": "sphere_019_sales_manager",
            "source": "synthetic_ollama"
        })
    
    print(f"\n   ✅ Сфера 019: {len(examples)} примеров")
    return examples

def generate_sphere_020_account_manager(target_count=108):
    """Генерация 108 примеров ACCOUNT MANAGER (Сфера 020)"""
    print("\n🤝 Генерация Сферы 020: ACCOUNT MANAGER (108 примеров)")
    
    prompts_templates = [
        "Проведи quarterly business review",
        "Найди возможность для upsell",
        "Предотврати отток клиента",
        "Составь план развития аккаунта",
        "Проведи cross-sell",
        "Укрепи отношения с ключевым клиентом",
        "Обработай escalation",
        "Увеличь lifetime value",
        "Найди новых stakeholders",
        "Продли контракт"
    ]
    
    account_situations = [
        "Клиент использует только 20% функционала",
        "Контракт заканчивается через месяц",
        "Клиент недоволен последним обновлением",
        "У клиента сменился decision maker",
        "Конкурент активно атакует вашего клиента",
        "Клиент хочет снизить стоимость",
        "Появилась новая потребность у клиента",
        "Клиент планирует расширение бизнеса",
        "Низкий NPS от этого клиента",
        "Клиент не отвечает на коммуникации"
    ]
    
    examples = []
    
    for i in range(target_count):
        template = prompts_templates[i % len(prompts_templates)]
        situation = account_situations[i % len(account_situations)]
        
        print(f"\r   Генерация {i+1}/{target_count}...", end='', flush=True)
        
        full_prompt = f"""Ты - ACCOUNT MANAGER (Сфера 020).

Духовная миссия: Долгосрочные отношения и рост аккаунта через партнёрство.

Задача: {template}

Ситуация: {situation}

Дай стратегию аккаунт-менеджера (3-4 предложения):"""
        
        response = call_ollama(full_prompt)
        
        examples.append({
            "instruction": f"Ты - ACCOUNT MANAGER. {template}",
            "input": situation,
            "output": response,
            "sphere": "020",
            "role": "sphere_020_account_manager",
            "source": "synthetic_ollama"
        })
    
    print(f"\n   ✅ Сфера 020: {len(examples)} примеров")
    return examples

def generate_sphere_021_presales_engineer(target_count=108):
    """Генерация 108 примеров PRESALES ENGINEER (Сфера 021)"""
    print("\n🔧 Генерация Сферы 021: PRESALES ENGINEER (108 примеров)")
    
    prompts_templates = [
        "Проведи техническую квалификацию",
        "Подготовь демо для клиента",
        "Составь план POC",
        "Ответь на RFP/RFI",
        "Проведи discovery сессию",
        "Подготовь техническую презентацию",
        "Оцени техническую feasibility",
        "Составь solution design",
        "Проведи benchmark тестирование",
        "Подготовь техническое обоснование ROI"
    ]
    
    technical_requests = [
        "Клиент спрашивает про интеграцию с SAP",
        "Нужно демо для CTO крупной компании",
        "Клиент требует on-premise решение",
        "Вопрос про масштабируемость до 1M пользователей",
        "Требования по безопасности SOC2, ISO27001",
        "Клиент хочет сравнить с конкурентом",
        "Нужно доказать производительность решения",
        "Клиент спрашивает про API и кастомизацию",
        "Требования по SLA 99.99%",
        "Вопрос про миграцию с legacy системы"
    ]
    
    examples = []
    
    for i in range(target_count):
        template = prompts_templates[i % len(prompts_templates)]
        request = technical_requests[i % len(technical_requests)]
        
        print(f"\r   Генерация {i+1}/{target_count}...", end='', flush=True)
        
        full_prompt = f"""Ты - PRESALES ENGINEER (Сфера 021).

Духовная миссия: Техническая экспертиза и доказательство ценности решения.

Задача: {template}

Запрос: {request}

Дай техническое решение пресейлза (3-4 предложения):"""
        
        response = call_ollama(full_prompt)
        
        examples.append({
            "instruction": f"Ты - PRESALES ENGINEER. {template}",
            "input": request,
            "output": response,
            "sphere": "021",
            "role": "sphere_021_presales_engineer",
            "source": "synthetic_ollama"
        })
    
    print(f"\n   ✅ Сфера 021: {len(examples)} примеров")
    return examples

def generate_sphere_022_business_developer(target_count=108):
    """Генерация 108 примеров BUSINESS DEVELOPER (Сфера 022)"""
    print("\n🚀 Генерация Сферы 022: BUSINESS DEVELOPER (108 примеров)")
    
    prompts_templates = [
        "Найди новый канал продаж",
        "Построй партнёрскую программу",
        "Выйди на новый рынок",
        "Найди стратегических партнёров",
        "Составь go-to-market стратегию",
        "Оцени потенциал нового сегмента",
        "Подготовь pitch для инвесторов",
        "Найди возможности для M&A",
        "Построй реферальную программу",
        "Разработай новую бизнес-модель"
    ]
    
    business_contexts = [
        "Рынок B2B SaaS насыщен конкурентами",
        "Есть бюджет на экспансию в Европу",
        "Нужно увеличить MRR в 3 раза за год",
        "Появился запрос от крупного enterprise",
        "Конкуренты вышли на смежный рынок",
        "Есть возможность интеграции с маркетплейсом",
        "Инвесторы требуют ускорения роста",
        "Появилась технология для нового продукта",
        "Падает эффективность текущих каналов",
        "Клиенты запрашивают новую функциональность"
    ]
    
    examples = []
    
    for i in range(target_count):
        template = prompts_templates[i % len(prompts_templates)]
        context = business_contexts[i % len(business_contexts)]
        
        print(f"\r   Генерация {i+1}/{target_count}...", end='', flush=True)
        
        full_prompt = f"""Ты - BUSINESS DEVELOPER (Сфера 022).

Духовная миссия: Поиск новых возможностей и стратегическое развитие бизнеса.

Задача: {template}

Контекст: {context}

Дай стратегию бизнес-девелопера (3-4 предложения):"""
        
        response = call_ollama(full_prompt)
        
        examples.append({
            "instruction": f"Ты - BUSINESS DEVELOPER. {template}",
            "input": context,
            "output": response,
            "sphere": "022",
            "role": "sphere_022_business_developer",
            "source": "synthetic_ollama"
        })
    
    print(f"\n   ✅ Сфера 022: {len(examples)} примеров")
    return examples

def generate_sphere_023_customer_support(target_count=108):
    """Генерация 108 примеров CUSTOMER SUPPORT (Сфера 023)"""
    print("\n💬 Генерация Сферы 023: CUSTOMER SUPPORT (108 примеров)")
    
    prompts_templates = [
        "Помоги клиенту решить проблему",
        "Обработай жалобу клиента",
        "Объясни как работает функция",
        "Успокой разозлённого клиента",
        "Эскалируй проблему корректно",
        "Найди решение в базе знаний",
        "Собери информацию для баг-репорта",
        "Помоги с onboarding",
        "Восстанови доступ к аккаунту",
        "Обработай запрос на возврат"
    ]
    
    support_tickets = [
        "Клиент: 'Не могу войти в систему, срочно!'",
        "Клиент: 'Это не работает! Верните деньги!'",
        "Клиент: 'Где найти функцию экспорта данных?'",
        "Клиент: 'Третий день жду ответа от техподдержки'",
        "Клиент: 'Система зависла посреди работы'",
        "Клиент: 'Не понимаю как пользоваться вашим продуктом'",
        "Клиент: 'Удалил данные по ошибке, можно восстановить?'",
        "Клиент: 'Почему списали деньги дважды?'",
        "Клиент: 'Интеграция с API не работает'",
        "Клиент: 'Когда исправите этот баг?'"
    ]
    
    examples = []
    
    for i in range(target_count):
        template = prompts_templates[i % len(prompts_templates)]
        ticket = support_tickets[i % len(support_tickets)]
        
        print(f"\r   Генерация {i+1}/{target_count}...", end='', flush=True)
        
        full_prompt = f"""Ты - CUSTOMER SUPPORT (Сфера 023).

Духовная миссия: Быстрое решение проблем клиента с эмпатией и заботой.

Задача: {template}

Тикет: {ticket}

Дай ответ службы поддержки (3-4 предложения):"""
        
        response = call_ollama(full_prompt)
        
        examples.append({
            "instruction": f"Ты - CUSTOMER SUPPORT. {template}",
            "input": ticket,
            "output": response,
            "sphere": "023",
            "role": "sphere_023_customer_support",
            "source": "synthetic_ollama"
        })
    
    print(f"\n   ✅ Сфера 023: {len(examples)} примеров")
    return examples

def generate_sphere_024_technical_support(target_count=108):
    """Генерация 108 примеров TECHNICAL SUPPORT (Сфера 024)"""
    print("\n🔍 Генерация Сферы 024: TECHNICAL SUPPORT (108 примеров)")
    
    prompts_templates = [
        "Проанализируй логи ошибки",
        "Помоги настроить интеграцию",
        "Найди причину performance issue",
        "Помоги с конфигурацией системы",
        "Разбери сложный технический кейс",
        "Помоги с миграцией данных",
        "Отладь проблему в production",
        "Помоги настроить SSO",
        "Разбери проблему с API",
        "Помоги оптимизировать запросы"
    ]
    
    technical_issues = [
        "Error 500 при попытке загрузить файл больше 10MB",
        "API возвращает 429 Too Many Requests",
        "Webhook не срабатывает на production",
        "Запросы к БД выполняются 30+ секунд",
        "SAML SSO не работает с Azure AD",
        "WebSocket connection постоянно дропается",
        "Импорт 100K записей занимает 6 часов",
        "CORS ошибки при запросах с frontend",
        "Memory leak в долгоживущих процессах",
        "Rate limiting блокирует легитимных пользователей"
    ]
    
    examples = []
    
    for i in range(target_count):
        template = prompts_templates[i % len(prompts_templates)]
        issue = technical_issues[i % len(technical_issues)]
        
        print(f"\r   Генерация {i+1}/{target_count}...", end='', flush=True)
        
        full_prompt = f"""Ты - TECHNICAL SUPPORT (Сфера 024).

Духовная миссия: Глубокая техническая экспертиза для решения сложных проблем.

Задача: {template}

Проблема: {issue}

Дай техническое решение (3-4 предложения):"""
        
        response = call_ollama(full_prompt)
        
        examples.append({
            "instruction": f"Ты - TECHNICAL SUPPORT. {template}",
            "input": issue,
            "output": response,
            "sphere": "024",
            "role": "sphere_024_technical_support",
            "source": "synthetic_ollama"
        })
    
    print(f"\n   ✅ Сфера 024: {len(examples)} примеров")
    return examples

def generate_sphere_025_customer_success(target_count=108):
    """Генерация 108 примеров CUSTOMER SUCCESS (Сфера 025)"""
    print("\n🎯 Генерация Сферы 025: CUSTOMER SUCCESS (108 примеров)")
    
    prompts_templates = [
        "Проведи onboarding нового клиента",
        "Увеличь product adoption",
        "Докажи ROI клиенту",
        "Проведи success planning сессию",
        "Предотврати churn",
        "Обучи команду клиента",
        "Найди возможности для expansion",
        "Улучши health score клиента",
        "Проведи check-in call",
        "Помоги достичь success milestones"
    ]
    
    customer_situations = [
        "Клиент 3 месяца после покупки, использует 10% функций",
        "NPS = 4, клиент не видит ценности",
        "Клиент достиг initial goals, что дальше?",
        "Red health score: низкая активность",
        "Клиент жалуется на сложность продукта",
        "Команда клиента не прошла обучение",
        "Клиент просит case study для руководства",
        "Expansion opportunity: новый департамент",
        "Клиент месяц не логинился в систему",
        "Renewal через 60 дней, нет engagement"
    ]
    
    examples = []
    
    for i in range(target_count):
        template = prompts_templates[i % len(prompts_templates)]
        situation = customer_situations[i % len(customer_situations)]
        
        print(f"\r   Генерация {i+1}/{target_count}...", end='', flush=True)
        
        full_prompt = f"""Ты - CUSTOMER SUCCESS MANAGER (Сфера 025).

Духовная миссия: Проактивное обеспечение успеха клиента и достижение его целей.

Задача: {template}

Ситуация: {situation}

Дай стратегию CSM (3-4 предложения):"""
        
        response = call_ollama(full_prompt)
        
        examples.append({
            "instruction": f"Ты - CUSTOMER SUCCESS. {template}",
            "input": situation,
            "output": response,
            "sphere": "025",
            "role": "sphere_025_customer_success",
            "source": "synthetic_ollama"
        })
    
    print(f"\n   ✅ Сфера 025: {len(examples)} примеров")
    return examples

def generate_sphere_026_solution_architect(target_count=108):
    """Генерация 108 примеров SOLUTION ARCHITECT (Сфера 026)"""
    print("\n🏛️  Генерация Сферы 026: SOLUTION ARCHITECT (108 примеров)")
    
    prompts_templates = [
        "Спроектируй оптимальное решение",
        "Составь implementation roadmap",
        "Оптимизируй существующую архитектуру",
        "Спроектируй интеграционную схему",
        "Составь best practices guide",
        "Оцени текущую архитектуру клиента",
        "Спроектируй масштабируемое решение",
        "Помоги выбрать правильный подход",
        "Составь migration plan",
        "Оптимизируй использование продукта"
    ]
    
    client_requirements = [
        "Enterprise клиент: 10K пользователей, множество интеграций",
        "Клиент хочет мигрировать с legacy системы",
        "Требуется multi-tenant решение с изоляцией",
        "Клиент работает в регулируемой индустрии",
        "Нужна offline-first архитектура для mobile",
        "Клиент требует high availability 99.99%",
        "Сложная схема прав доступа и ролей",
        "Интеграция с 15+ внешними системами",
        "Требуется real-time синхронизация данных",
        "Клиент хочет hybrid cloud решение"
    ]
    
    examples = []
    
    for i in range(target_count):
        template = prompts_templates[i % len(prompts_templates)]
        requirement = client_requirements[i % len(client_requirements)]
        
        print(f"\r   Генерация {i+1}/{target_count}...", end='', flush=True)
        
        full_prompt = f"""Ты - SOLUTION ARCHITECT (Сфера 026).

Духовная миссия: Оптимальные решения под задачи клиента, best practices.

Задача: {template}

Требования: {requirement}

Дай архитектурное решение (3-4 предложения):"""
        
        response = call_ollama(full_prompt)
        
        examples.append({
            "instruction": f"Ты - SOLUTION ARCHITECT. {template}",
            "input": requirement,
            "output": response,
            "sphere": "026",
            "role": "sphere_026_solution_architect",
            "source": "synthetic_ollama"
        })
    
    print(f"\n   ✅ Сфера 026: {len(examples)} примеров")
    return examples

def main():
    """Главная функция генерации"""
    print("="*80)
    print("🌟 Генерация 108 примеров для Sales & Support")
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
    
    # Сфера 019: SALES MANAGER (108)
    all_examples.extend(generate_sphere_019_sales_manager(108))
    
    # Сфера 020: ACCOUNT MANAGER (108)
    all_examples.extend(generate_sphere_020_account_manager(108))
    
    # Сфера 021: PRESALES ENGINEER (108)
    all_examples.extend(generate_sphere_021_presales_engineer(108))
    
    # Сфера 022: BUSINESS DEVELOPER (108)
    all_examples.extend(generate_sphere_022_business_developer(108))
    
    # Сфера 023: CUSTOMER SUPPORT (108)
    all_examples.extend(generate_sphere_023_customer_support(108))
    
    # Сфера 024: TECHNICAL SUPPORT (108)
    all_examples.extend(generate_sphere_024_technical_support(108))
    
    # Сфера 025: CUSTOMER SUCCESS (108)
    all_examples.extend(generate_sphere_025_customer_success(108))
    
    # Сфера 026: SOLUTION ARCHITECT (108)
    all_examples.extend(generate_sphere_026_solution_architect(108))
    
    # Загружаем Alpaca (1080 примеров)
    print("\n🦙 Загрузка Alpaca (1080 примеров)...")
    alpaca_path = "/Volumes/MULTIMODAL/proj.datasets/alpaca_dataset/alpaca_data.json"
    
    if os.path.exists(alpaca_path):
        with open(alpaca_path, 'r', encoding='utf-8') as f:
            alpaca_data = json.load(f)
        
        # Фильтруем примеры связанные с продажами и коммуникацией
        keywords = ['sell', 'customer', 'client', 'persuade', 'negotiate', 'communicate',
                   'support', 'service', 'explain', 'convince', 'present', 'pitch']
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
    
    # Сохраняем (абсолютный путь в рабочем пространстве)
    base_dir = Path(__file__).resolve().parent.parent / "datasets"
    base_dir.mkdir(parents=True, exist_ok=True)
    output_path = str(base_dir / "sales_support_108_perfect.jsonl")
    
    print(f"\n💾 Сохранение датасета...")
    with open(output_path, 'w', encoding='utf-8') as f:
        for ex in all_examples:
            f.write(json.dumps(ex, ensure_ascii=False) + '\n')
    
    # Статистика
    stats = {
        "total": len(all_examples),
        "distribution": {
            "001_spiritual": len([e for e in all_examples if e['sphere'] == '001']),
            "019_sales_manager": len([e for e in all_examples if e['sphere'] == '019']),
            "020_account_manager": len([e for e in all_examples if e['sphere'] == '020']),
            "021_presales_engineer": len([e for e in all_examples if e['sphere'] == '021']),
            "022_business_developer": len([e for e in all_examples if e['sphere'] == '022']),
            "023_customer_support": len([e for e in all_examples if e['sphere'] == '023']),
            "024_technical_support": len([e for e in all_examples if e['sphere'] == '024']),
            "025_customer_success": len([e for e in all_examples if e['sphere'] == '025']),
            "026_solution_architect": len([e for e in all_examples if e['sphere'] == '026']),
            "general_alpaca": len([e for e in all_examples if e['sphere'] == 'general'])
        }
    }
    
    stats_path = output_path.replace('.jsonl', '_stats.json')
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ Сохранено: {output_path}")
    print()
    print("="*80)
    print("✅ ДАТАСЕТ ДЛЯ SALES & SUPPORT ГОТОВ!")
    print("="*80)
    print()
    print("📊 Распределение (священное 108):")
    for sphere, count in stats['distribution'].items():
        print(f"   {sphere}: {count}")
    print()
    print(f"📦 Всего примеров: {stats['total']}")
    print()
    print("🙏 108 - священное число в каждой сфере продаж и поддержки!")
    print("💼 Готово для обучения моделей Sales & Support!")

if __name__ == "__main__":
    main()



