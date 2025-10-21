#!/usr/bin/env python3
"""
Генерация ровно 108 примеров для каждой сферы через Ollama

Использует локальную LLM для создания качественных синтетических примеров

Духовное число: 108 примеров × 4 сферы + 1080 Alpaca = 1512 примеров

© 2025 NativeMind - NativeMindNONC License
"""

import json
import os
import subprocess
from pathlib import Path

def call_ollama(prompt, model="nativemind/mozgach108-light:latest"):
    """Вызывает Ollama для генерации"""
    try:
        result = subprocess.run(
            ["/opt/homebrew/bin/ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Ошибка: {e}"

def generate_sphere_001_spiritual(target_count=108):
    """Генерация 108 духовных примеров (Сфера 001)"""
    print("\n🕉️  Генерация Сферы 001: ДУХОВНАЯ (108 примеров)")
    
    spiritual_prompts = [
        "Объясни значение истины в духовном понимании",
        "Как служить справедливости с духовной точки зрения",
        "В чем духовный смысл беспристрастности",
        "Объясни карму и справедливость",
        "Что значит истина в Ведах",
        "Как духовность связана с законом",
        "Объясни Дхарму в юридическом контексте",
        "Что такое Сатва в служении истине",
        "Как медитация помогает судьям",
        "Объясни Ахимсу в правосудии"
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

def generate_sphere_047_investigator(base_texts, target_count=108):
    """Генерация 108 примеров СЛЕДОВАТЕЛЯ (Сфера 047)"""
    print("\n🔍 Генерация Сферы 047: СЛЕДОВАТЕЛЬ (108 примеров)")
    
    prompts_templates = [
        "Проанализируй доказательства",
        "Оцени показания свидетеля",
        "Проверь алиби подозреваемого",
        "Составь протокол допроса",
        "Оцени материальные доказательства",
        "Найди противоречия в показаниях",
        "Проверь хронологию событий",
        "Оцени достоверность улик",
        "Составь план следственных действий",
        "Оцени полноту расследования"
    ]
    
    examples = []
    
    for i in range(target_count):
        template = prompts_templates[i % len(prompts_templates)]
        
        # Берем базовый текст если есть
        if base_texts and i < len(base_texts):
            context = base_texts[i]['input'][:500]
        else:
            context = f"Документ #{i+1} по уголовному делу"
        
        print(f"\r   Генерация {i+1}/{target_count}...", end='', flush=True)
        
        full_prompt = f"""Ты - СЛЕДОВАТЕЛЬ (Сфера 047). 
        
Духовная миссия: Беспристрастный сбор доказательств.

Задача: {template}

Контекст: {context}

Дай краткий анализ следователя (3-4 предложения):"""
        
        response = call_ollama(full_prompt)
        
        examples.append({
            "instruction": f"Ты - СЛЕДОВАТЕЛЬ. {template}",
            "input": context,
            "output": response,
            "sphere": "047",
            "role": "sphere_047_investigator",
            "source": "synthetic_ollama"
        })
    
    print(f"\n   ✅ Сфера 047: {len(examples)} примеров")
    return examples

def generate_sphere_048_prosecutor(base_texts, target_count=108):
    """Генерация 108 примеров ПРОКУРОРА (Сфера 048) - КЛЮЧЕВАЯ!"""
    print("\n⚖️  Генерация Сферы 048: ПРОКУРОР (108 примеров) - КЛЮЧЕВАЯ!")
    
    prompts_templates = [
        "Обнаружь копипаст между документами",
        "Проверь независимость проверки прокурора",
        "Найди признаки формального подхода",
        "Оцени качество надзора за следствием",
        "Проверь законность обвинения",
        "Найди процессуальные нарушения",
        "Оцени обоснованность обвинительного заключения",
        "Проверь соблюдение прав подозреваемого",
        "Найди противоречия в материалах дела",
        "Оцени служение истине в документах"
    ]
    
    examples = []
    
    for i in range(target_count):
        template = prompts_templates[i % len(prompts_templates)]
        
        if base_texts and i < len(base_texts):
            context = base_texts[i]['input'][:500]
        else:
            context = f"Обвинительное заключение по делу №{i+1}"
        
        print(f"\r   Генерация {i+1}/{target_count}...", end='', flush=True)
        
        full_prompt = f"""Ты - ПРОКУРОР (Сфера 048).

Духовная миссия: Обнаружение копипаста как симптома несправедливости.

"Копирование документов - это симптом отсутствия независимой проверки, 
формального подхода к судьбам людей, возможной коррупции."

Задача: {template}

Документ: {context}

Дай заключение прокурора (3-4 предложения):"""
        
        response = call_ollama(full_prompt)
        
        examples.append({
            "instruction": f"Ты - ПРОКУРОР. {template}",
            "input": context,
            "output": response,
            "sphere": "048",
            "role": "sphere_048_prosecutor",
            "source": "synthetic_ollama"
        })
    
    print(f"\n   ✅ Сфера 048: {len(examples)} примеров")
    return examples

def generate_sphere_049_judge(base_texts, target_count=108):
    """Генерация 108 примеров СУДЬИ (Сфера 049)"""
    print("\n⚖️  Генерация Сферы 049: СУДЬЯ (108 примеров)")
    
    prompts_templates = [
        "Вынеси справедливое решение",
        "Оцени беспристрастность следствия",
        "Проверь законность процедуры",
        "Оцени достаточность доказательств",
        "Вынеси вердикт по делу",
        "Оцени соблюдение прав сторон",
        "Проверь процессуальную правильность",
        "Оцени служение истине в деле",
        "Вынеси решение о мере пресечения",
        "Оцени справедливость обвинения"
    ]
    
    examples = []
    
    for i in range(target_count):
        template = prompts_templates[i % len(prompts_templates)]
        
        if base_texts and i < len(base_texts):
            context = base_texts[i]['input'][:500]
        else:
            context = f"Материалы дела №{i+1}"
        
        print(f"\r   Генерация {i+1}/{target_count}...", end='', flush=True)
        
        full_prompt = f"""Ты - СУДЬЯ (Сфера 049).

Духовная миссия: Вынесение справедливого решения на основе истины.

Задача: {template}

Материалы: {context}

Дай решение судьи (3-4 предложения):"""
        
        response = call_ollama(full_prompt)
        
        examples.append({
            "instruction": f"Ты - СУДЬЯ. {template}",
            "input": context,
            "output": response,
            "sphere": "049",
            "role": "sphere_049_judge",
            "source": "synthetic_ollama"
        })
    
    print(f"\n   ✅ Сфера 049: {len(examples)} примеров")
    return examples

def main():
    """Главная функция генерации"""
    print("="*80)
    print("🌟 Генерация 108 примеров для каждой сферы")
    print("="*80)
    print()
    print("🙏 Священное число 108 в каждой сфере")
    print()
    
    # Проверяем Ollama
    try:
        result = subprocess.run(["/opt/homebrew/bin/ollama", "version"], capture_output=True, text=True)
        print(f"✅ Ollama доступен: {result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Ошибка Ollama: {e}")
        return
    
    # Загружаем базовые тексты
    legal_path = "../datasets/legal_case_viktor/legal_dataset.jsonl"
    base_texts = []
    
    if os.path.exists(legal_path):
        with open(legal_path, 'r', encoding='utf-8') as f:
            base_texts = [json.loads(line) for line in f]
        print(f"📚 Загружено базовых текстов: {len(base_texts)}")
    
    # Генерируем для каждой сферы
    all_examples = []
    
    # Сфера 001: Духовная (108)
    all_examples.extend(generate_sphere_001_spiritual(108))
    
    # Сфера 047: СЛЕДОВАТЕЛЬ (108)
    all_examples.extend(generate_sphere_047_investigator(base_texts, 108))
    
    # Сфера 048: ПРОКУРОР (108)
    all_examples.extend(generate_sphere_048_prosecutor(base_texts, 108))
    
    # Сфера 049: СУДЬЯ (108)
    all_examples.extend(generate_sphere_049_judge(base_texts, 108))
    
    # Загружаем Alpaca (1080 лучших примеров)
    print("\n🦙 Загрузка Alpaca (1080 примеров)...")
    alpaca_path = "/Volumes/MULTIMODAL/proj.datasets/alpaca_dataset/alpaca_data.json"
    
    with open(alpaca_path, 'r', encoding='utf-8') as f:
        alpaca_data = json.load(f)
    
    # Фильтруем аналитические примеры
    keywords = ['analyze', 'evaluate', 'review', 'compare', 'assess', 'examine']
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
    
    # Сохраняем
    output_path = "../datasets/legal_108_perfect.jsonl"
    
    print(f"\n💾 Сохранение датасета...")
    with open(output_path, 'w', encoding='utf-8') as f:
        for ex in all_examples:
            f.write(json.dumps(ex, ensure_ascii=False) + '\n')
    
    # Статистика
    stats = {
        "total": len(all_examples),
        "distribution": {
            "001_spiritual": len([e for e in all_examples if e['sphere'] == '001']),
            "047_investigator": len([e for e in all_examples if e['sphere'] == '047']),
            "048_prosecutor": len([e for e in all_examples if e['sphere'] == '048']),
            "049_judge": len([e for e in all_examples if e['sphere'] == '049']),
            "general_alpaca": len([e for e in all_examples if e['sphere'] == 'general'])
        }
    }
    
    stats_path = output_path.replace('.jsonl', '_stats.json')
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"   ✅ Сохранено: {output_path}")
    print()
    print("="*80)
    print("✅ ДАТАСЕТ ГОТОВ!")
    print("="*80)
    print()
    print("📊 Распределение (священное 108):")
    for sphere, count in stats['distribution'].items():
        print(f"   {sphere}: {count}")
    print()
    print(f"📦 Всего примеров: {stats['total']}")
    print()
    print("🙏 108 - священное число в каждой сфере!")
    print("⚖️  Готово к обучению!")

if __name__ == "__main__":
    main()

