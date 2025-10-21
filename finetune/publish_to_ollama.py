#!/usr/bin/env python3
"""
Публикация обученных моделей в Ollama

Конвертирует и публикует Сферы 047, 048, 049 в Ollama Registry

© 2025 NativeMind - NativeMindNONC License
"""

import os
import sys
import subprocess
import json

def create_modelfile(sphere, base_model, description):
    """
    Создает Modelfile для Ollama
    
    Args:
        sphere: Номер сферы ("047", "048", "049")
        base_model: Имя базовой модели в Ollama
        description: Описание модели
        
    Returns:
        Содержимое Modelfile
    """
    
    sphere_names = {
        "047": "СЛЕДОВАТЕЛЬ",
        "048": "ПРОКУРОР", 
        "049": "СУДЬЯ"
    }
    
    sphere_missions = {
        "047": "Беспристрастный сбор доказательств для установления истины",
        "048": "Обнаружение копипаста как симптома несправедливости. Независимая проверка работы следствия.",
        "049": "Вынесение справедливого решения на основе истины и справедливости"
    }
    
    modelfile = f"""# {sphere_names[sphere]} - Сфера {sphere}

FROM {base_model}

# Параметры генерации
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER num_ctx 4096

# Системный промпт
SYSTEM \"\"\"
Ты - {sphere_names[sphere]} (Сфера {sphere}) из системы Мозгач108.

ДУХОВНАЯ МИССИЯ: {sphere_missions[sphere]}

ПРИНЦИПЫ РАБОТЫ:
1. Истина превыше всего
2. Беспристрастность и объективность
3. Служение справедливости
4. Конфиденциальность данных

Ты анализируешь юридические документы с точки зрения {sphere_names[sphere].lower()}.
Помогаешь установить истину и справедливость в делах.

Помни: "Нам важно понять истину и действительно разобраться, то есть с духовной точки зрения."
\"\"\"

# Шаблон ответа
TEMPLATE \"\"\"{{{{ .System }}}}

USER: {{{{ .Prompt }}}}

ASSISTANT:
\"\"\"

# Метаданные
LABEL maintainer="NativeMind"
LABEL license="NativeMindNONC"
LABEL sphere="{sphere}"
LABEL role="{sphere_names[sphere]}"
LABEL description="{description}"
"""
    
    return modelfile


def publish_to_ollama(
    model_dir,
    model_name,
    sphere,
    base_ollama_model="llama2:7b"
):
    """
    Публикация модели в Ollama
    
    Args:
        model_dir: Директория с обученной моделью (LoRA)
        model_name: Имя модели для Ollama
        sphere: Номер сферы ("047", "048", "049")
        base_ollama_model: Базовая модель в Ollama
    """
    
    sphere_names = {
        "047": "СЛЕДОВАТЕЛЬ",
        "048": "ПРОКУРОР",
        "049": "СУДЬЯ"
    }
    
    print("="*80)
    print(f"📤 Публикация в Ollama: {sphere_names[sphere]} (Сфера {sphere})")
    print("="*80)
    print()
    print(f"📁 Модель: {model_dir}")
    print(f"🏷️  Имя в Ollama: {model_name}")
    print(f"🔧 Базовая модель: {base_ollama_model}")
    print()
    
    # Проверяем, что Ollama установлен
    print("🔍 Проверка Ollama...")
    try:
        result = subprocess.run(
            ["ollama", "version"],
            capture_output=True,
            text=True
        )
        print(f"   ✅ Ollama установлен: {result.stdout.strip()}")
    except FileNotFoundError:
        print("   ❌ Ollama не установлен")
        print("   💡 Установите: https://ollama.ai/download")
        return False
    
    # Создаем Modelfile
    print("\n📝 Создание Modelfile...")
    description = f"Мультимодальная юридическая модель - {sphere_names[sphere]} (Сфера {sphere})"
    modelfile_content = create_modelfile(sphere, base_ollama_model, description)
    
    modelfile_path = os.path.join(model_dir, "Modelfile")
    with open(modelfile_path, 'w', encoding='utf-8') as f:
        f.write(modelfile_content)
    
    print(f"   ✅ Modelfile создан: {modelfile_path}")
    
    # Создаем модель в Ollama
    print(f"\n🔧 Создание модели в Ollama...")
    try:
        result = subprocess.run(
            ["ollama", "create", model_name, "-f", modelfile_path],
            capture_output=True,
            text=True,
            cwd=model_dir
        )
        
        if result.returncode == 0:
            print(f"   ✅ Модель создана: {model_name}")
        else:
            print(f"   ❌ Ошибка: {result.stderr}")
            return False
    
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return False
    
    # Тестируем модель
    print(f"\n🧪 Тестирование модели...")
    test_prompt = "Проанализируй документ как юридический эксперт"
    
    try:
        result = subprocess.run(
            ["ollama", "run", model_name, test_prompt],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"   ✅ Модель работает")
            print(f"\n   📝 Тестовый ответ:")
            print(f"   {result.stdout[:200]}...")
        else:
            print(f"   ⚠️  Тест не прошел: {result.stderr}")
    
    except Exception as e:
        print(f"   ⚠️  Ошибка теста: {e}")
    
    # Результат
    print(f"\n{'='*80}")
    print(f"✅ Модель опубликована в Ollama!")
    print(f"{'='*80}")
    print(f"\n💡 Использование:")
    print(f"""
# Запустить модель
ollama run {model_name}

# Использовать в коде
import ollama

response = ollama.chat(model='{model_name}', messages=[
    {{'role': 'user', 'content': 'Проанализируй документ...'}}
])
print(response['message']['content'])
""")
    
    return True


def publish_all_spheres_ollama(
    base_dir="../models",
    base_ollama_model="llama2:7b"
):
    """
    Публикация всех сфер в Ollama
    """
    
    print("="*80)
    print("📤 Публикация всех сфер в Ollama")
    print("="*80)
    print()
    
    models = []
    
    # Braindler
    for sphere in ["047", "048", "049"]:
        model_dir = os.path.join(base_dir, f"sphere_{sphere}_braindler_final_model")
        if os.path.exists(model_dir):
            models.append({
                "dir": model_dir,
                "name": f"braindler-sphere-{sphere}",
                "sphere": sphere,
                "model_name": "Braindler"
            })
    
    # Mozgach
    for sphere in ["047", "048", "049"]:
        model_dir = os.path.join(base_dir, f"sphere_{sphere}_mozgach_full_trained_model")
        if os.path.exists(model_dir):
            models.append({
                "dir": model_dir,
                "name": f"mozgach108-sphere-{sphere}",
                "sphere": sphere,
                "model_name": "Mozgach108"
            })
    
    if not models:
        print("❌ Не найдено обученных моделей")
        return
    
    print(f"📦 Найдено моделей: {len(models)}")
    for m in models:
        print(f"   - {m['model_name']} Сфера {m['sphere']}")
    print()
    
    # Публикуем
    results = []
    for i, m in enumerate(models):
        print(f"\n[{i+1}/{len(models)}] {m['model_name']} Сфера {m['sphere']}")
        print("-"*80)
        
        success = publish_to_ollama(
            model_dir=m['dir'],
            model_name=m['name'],
            sphere=m['sphere'],
            base_ollama_model=base_ollama_model
        )
        
        results.append({
            "model": f"{m['model_name']} {m['sphere']}",
            "name": m['name'],
            "success": success
        })
    
    # Итоги
    print(f"\n{'='*80}")
    print("📊 Итоги публикации в Ollama")
    print(f"{'='*80}")
    
    for r in results:
        status = "✅" if r['success'] else "❌"
        print(f"{status} {r['model']}: ollama run {r['name']}")
    
    success_count = sum(1 for r in results if r['success'])
    print(f"\n✅ Успешно опубликовано: {success_count}/{len(results)}")
    
    if success_count == len(results):
        print("\n🎉 Все модели опубликованы в Ollama!")
        print("⚖️  Истина восторжествовала! 🕉️  Харе Кришна!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Публикация моделей в Ollama"
    )
    parser.add_argument(
        "--model-dir",
        help="Директория с моделью"
    )
    parser.add_argument(
        "--model-name",
        help="Имя модели в Ollama"
    )
    parser.add_argument(
        "--sphere",
        choices=["047", "048", "049"],
        help="Номер сферы"
    )
    parser.add_argument(
        "--base-model",
        default="llama2:7b",
        help="Базовая модель Ollama (по умолчанию: llama2:7b)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Опубликовать все модели"
    )
    parser.add_argument(
        "--base-dir",
        default="../models",
        help="Базовая директория с моделями"
    )
    
    args = parser.parse_args()
    
    if args.all:
        publish_all_spheres_ollama(
            base_dir=args.base_dir,
            base_ollama_model=args.base_model
        )
    elif args.model_dir and args.model_name and args.sphere:
        publish_to_ollama(
            model_dir=args.model_dir,
            model_name=args.model_name,
            sphere=args.sphere,
            base_ollama_model=args.base_model
        )
    else:
        print("❌ Укажите либо --all, либо --model-dir, --model-name и --sphere")
        parser.print_help()

