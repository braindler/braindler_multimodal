#!/usr/bin/env python3
"""
Тестирование улучшенных сфер разработки (073-078)

Расширенное тестирование с метриками качества

© 2025 NativeMind - NativeMindNONC License
"""

import os
import sys
import torch
import argparse
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import json
import time

def test_sphere_model_improved(sphere, model_path, test_prompts):
    """
    Расширенное тестирование одной сферы с метриками качества
    
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
    print(f"🧪 РАСШИРЕННОЕ ТЕСТИРОВАНИЕ СФЕРЫ {sphere}: {sphere_names[sphere]}")
    print(f"{'='*80}")
    
    if not os.path.exists(model_path):
        print(f"❌ Модель не найдена: {model_path}")
        return {"success": False, "metrics": {}}
    
    try:
        # Загрузка токенизатора
        print("📥 Загрузка токенизатора...")
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        print("   ✅ Токенизатор загружен")
        
        # Загрузка базовой модели
        print("📥 Загрузка базовой модели...")
        base_model = AutoModelForCausalLM.from_pretrained(
            "nativemind/shridhar_8k_multimodal",
            torch_dtype=torch.float32,
            device_map=None
        )
        
        # Загрузка LoRA адаптера
        print("📥 Загрузка LoRA адаптера...")
        model = PeftModel.from_pretrained(base_model, model_path)
        print("   ✅ Модель загружена")
        
        # Тестирование с метриками
        print(f"\n🧪 Тестирование {len(test_prompts)} промптов...")
        
        results = []
        total_time = 0
        
        for i, prompt in enumerate(test_prompts, 1):
            print(f"\n--- Тест {i} ---")
            print(f"Промпт: {prompt}")
            
            start_time = time.time()
            
            # Токенизация
            inputs = tokenizer(prompt, return_tensors="pt")
            
            # Генерация
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=300,  # Увеличено с 200 до 300
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id,
                    eos_token_id=tokenizer.eos_token_id,
                    repetition_penalty=1.1  # Добавлен penalty для повторений
                )
            
            generation_time = time.time() - start_time
            total_time += generation_time
            
            # Декодирование
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = response[len(prompt):].strip()
            
            print(f"Ответ: {response[:200]}{'...' if len(response) > 200 else ''}")
            print(f"Время генерации: {generation_time:.2f}s")
            
            # Анализ качества ответа
            quality_score = analyze_response_quality(prompt, response, sphere)
            print(f"Оценка качества: {quality_score}/10")
            
            results.append({
                "prompt": prompt,
                "response": response,
                "generation_time": generation_time,
                "quality_score": quality_score
            })
            
            print("-" * 50)
        
        # Расчет метрик
        avg_quality = sum(r["quality_score"] for r in results) / len(results)
        avg_time = total_time / len(results)
        
        metrics = {
            "avg_quality": avg_quality,
            "avg_generation_time": avg_time,
            "total_tests": len(results),
            "successful_tests": len([r for r in results if r["quality_score"] >= 6])
        }
        
        print(f"\n📊 МЕТРИКИ СФЕРЫ {sphere}:")
        print(f"   🎯 Средняя оценка качества: {avg_quality:.1f}/10")
        print(f"   ⏱️  Среднее время генерации: {avg_time:.2f}s")
        print(f"   ✅ Успешных тестов: {metrics['successful_tests']}/{metrics['total_tests']}")
        
        print(f"\n✅ Сфера {sphere} ({sphere_names[sphere]}) протестирована успешно!")
        return {"success": True, "metrics": metrics, "results": results}
        
    except Exception as e:
        print(f"\n❌ Ошибка при тестировании сферы {sphere}: {e}")
        return {"success": False, "metrics": {}, "error": str(e)}

def analyze_response_quality(prompt, response, sphere):
    """
    Анализ качества ответа с учетом специфики сферы
    """
    
    # Базовые метрики
    relevance_score = 0
    technical_accuracy = 0
    completeness = 0
    clarity = 0
    
    # Проверка релевантности
    if len(response) > 50:  # Не пустой ответ
        relevance_score += 3
    if any(keyword in response.lower() for keyword in ["код", "программирование", "разработка", "технический"]):
        relevance_score += 2
    
    # Проверка технической точности
    if any(keyword in response.lower() for keyword in ["python", "javascript", "java", "функция", "класс", "метод"]):
        technical_accuracy += 2
    if "```" in response or "код" in response.lower():
        technical_accuracy += 2
    
    # Проверка полноты
    if len(response) > 100:
        completeness += 2
    if len(response) > 300:
        completeness += 1
    
    # Проверка ясности
    if len(response.split()) > 10:  # Не слишком короткий
        clarity += 2
    if not response.endswith("..."):  # Полный ответ
        clarity += 1
    
    # Специфичные проверки для каждой сферы
    sphere_bonus = 0
    if sphere == "073" and any(word in response.lower() for word in ["def ", "class ", "import ", "return"]):
        sphere_bonus += 2
    elif sphere == "074" and any(word in response.lower() for word in ["ошибка", "проблема", "улучшение", "рефакторинг"]):
        sphere_bonus += 2
    elif sphere == "075" and any(word in response.lower() for word in ["архитектура", "система", "микросервисы", "паттерн"]):
        sphere_bonus += 2
    elif sphere == "076" and any(word in response.lower() for word in ["docker", "kubernetes", "ci/cd", "devops"]):
        sphere_bonus += 2
    elif sphere == "077" and any(word in response.lower() for word in ["тест", "проверка", "qa", "баг"]):
        sphere_bonus += 2
    elif sphere == "078" and any(word in response.lower() for word in ["документация", "readme", "api", "руководство"]):
        sphere_bonus += 2
    
    total_score = min(10, relevance_score + technical_accuracy + completeness + clarity + sphere_bonus)
    return total_score

def main():
    parser = argparse.ArgumentParser(description="Тестирование улучшенных сфер разработки")
    parser.add_argument("--models-dir", default="../models_improved",
                       help="Директория с улучшенными моделями")
    
    args = parser.parse_args()
    
    # Тестовые промпты для каждой сферы
    test_prompts = {
        "073": [
            "Напиши функцию на Python для сортировки массива",
            "Создай класс для работы с базой данных",
            "Оптимизируй производительность этого кода",
            "Реализуй паттерн Singleton на Python",
            "Создай REST API с использованием Flask"
        ],
        "074": [
            "Проверь этот код на наличие ошибок",
            "Найди проблемы производительности в этом коде",
            "Проверь соответствие стандартам кодирования",
            "Выяви уязвимости безопасности",
            "Предложи улучшения архитектуры"
        ],
        "075": [
            "Спроектируй архитектуру микросервисов",
            "Создай масштабируемую систему для 1M пользователей",
            "Спроектируй систему реального времени",
            "Выбери подходящие технологии для проекта",
            "Создай архитектуру для высоконагруженной системы"
        ],
        "076": [
            "Настрой CI/CD pipeline для Python проекта",
            "Создай Docker контейнер для приложения",
            "Настрой мониторинг производительности",
            "Автоматизируй развертывание в Kubernetes",
            "Настрой безопасность инфраструктуры"
        ],
        "077": [
            "Напиши unit тесты для этой функции",
            "Создай план тестирования для API",
            "Автоматизируй тестирование UI",
            "Проверь покрытие кода тестами",
            "Создай тесты производительности"
        ],
        "078": [
            "Напиши техническую документацию для API",
            "Создай README для проекта",
            "Напиши руководство пользователя",
            "Создай архитектурную документацию",
            "Напиши инструкцию по развертыванию"
        ]
    }
    
    print("==================================================================================")
    print("🧪 РАСШИРЕННОЕ ТЕСТИРОВАНИЕ УЛУЧШЕННЫХ СФЕР РАЗРАБОТКИ")
    print("==================================================================================")
    print()
    
    # Проверка доступности моделей
    available_spheres = []
    
    for sphere in ["073", "074", "075", "076", "077", "078"]:
        model_path = f"{args.models_dir}/sphere_{sphere}_improved"
        if os.path.exists(model_path):
            available_spheres.append(sphere)
            print(f"✅ Сфера {sphere}: {model_path}")
        else:
            print(f"❌ Сфера {sphere}: не найдена")
    
    print(f"\n📊 Найдено {len(available_spheres)} улучшенных сфер")
    
    if not available_spheres:
        print("\n❌ Нет улучшенных моделей для тестирования!")
        return
    
    # Тестирование каждой доступной сферы
    results = {}
    overall_metrics = {
        "total_quality": 0,
        "total_tests": 0,
        "successful_tests": 0
    }
    
    for sphere in available_spheres:
        model_path = f"{args.models_dir}/sphere_{sphere}_improved"
        
        result = test_sphere_model_improved(
            sphere, 
            model_path, 
            test_prompts[sphere]
        )
        results[sphere] = result
        
        if result["success"]:
            metrics = result["metrics"]
            overall_metrics["total_quality"] += metrics["avg_quality"]
            overall_metrics["total_tests"] += metrics["total_tests"]
            overall_metrics["successful_tests"] += metrics["successful_tests"]
    
    # Итоговый отчет
    print("\n" + "="*80)
    print("📊 ИТОГОВЫЙ ОТЧЕТ ТЕСТИРОВАНИЯ УЛУЧШЕННЫХ МОДЕЛЕЙ")
    print("="*80)
    
    successful = sum(1 for result in results.values() if result["success"])
    total = len(results)
    
    print(f"✅ Успешно протестировано: {successful}/{total}")
    
    if overall_metrics["total_tests"] > 0:
        avg_quality = overall_metrics["total_quality"] / len([r for r in results.values() if r["success"]])
        success_rate = overall_metrics["successful_tests"] / overall_metrics["total_tests"] * 100
        
        print(f"🎯 Средняя оценка качества: {avg_quality:.1f}/10")
        print(f"📈 Процент успешных тестов: {success_rate:.1f}%")
    
    print()
    
    for sphere, result in results.items():
        if result["success"]:
            metrics = result["metrics"]
            status = f"✅ УСПЕШНО ({metrics['avg_quality']:.1f}/10)"
        else:
            status = "❌ ОШИБКА"
        print(f"Сфера {sphere}: {status}")
    
    print(f"\n🙏 Тестирование улучшенных моделей завершено!")

if __name__ == "__main__":
    main()
