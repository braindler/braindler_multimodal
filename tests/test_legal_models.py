#!/usr/bin/env python3
"""
Тесты мультимодальных юридических моделей

Тестирование Сфер 047, 048, 049 - служение истине

© 2025 NativeMind - NativeMindNONC License
"""

import sys
import os

# Добавляем src в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from legal_models import (
    MozgachSphere047_Investigator,
    MozgachSphere048_Prosecutor,
    MozgachSphere049_Judge,
    LegalModelsFactory
)


def test_investigator():
    """Тест СЛЕДОВАТЕЛЬ (Сфера 047)"""
    print("\n" + "="*80)
    print("ТЕСТ: МОЗГАЧ108 - СФЕРА 047 (СЛЕДОВАТЕЛЬ)")
    print("="*80)
    
    # Создаем модель
    investigator = MozgachSphere047_Investigator(device="cpu")
    
    # Тестовый сценарий
    print("\n📋 Тестовый сценарий: Сбор доказательств")
    
    test_prompt = """
Представь, что у тебя есть показания свидетеля:

"Я видел подозреваемого около магазина в 18:00. Он был в черной куртке.
Через 10 минут я услышал крики и вызвал полицию."

Проанализируй эти показания с точки зрения следователя.
"""
    
    response = investigator.chat(test_prompt)
    
    print("\n📊 Ответ СЛЕДОВАТЕЛЯ:")
    print(response)
    print("\n✅ Тест СЛЕДОВАТЕЛЯ пройден")


def test_prosecutor():
    """Тест ПРОКУРОР (Сфера 048)"""
    print("\n" + "="*80)
    print("ТЕСТ: МОЗГАЧ108 - СФЕРА 048 (ПРОКУРОР)")
    print("="*80)
    print("🙏 Духовная миссия: Обнаружение копипаста")
    
    # Создаем модель
    prosecutor = MozgachSphere048_Prosecutor(device="cpu")
    
    # Тестовый сценарий
    print("\n📋 Тестовый сценарий: Проверка документов на копипаст")
    
    test_prompt = """
У тебя есть два документа:

ДОКУМЕНТ СЛЕДОВАТЕЛЯ:
"На основании проведенного расследования установлено, что подозреваемый 
находился на месте преступления в указанное время. Свидетели подтверждают 
его присутствие. Материальные доказательства соответствуют обвинению."

ДОКУМЕНТ ПРОКУРОРА:
"На основании проведенного расследования установлено, что подозреваемый 
находился на месте преступления в указанное время. Свидетели подтверждают 
его присутствие. Материальные доказательства соответствуют обвинению."

Проанализируй эти документы. Есть ли признаки копипаста?
"""
    
    response = prosecutor.chat(test_prompt)
    
    print("\n⚖️  Ответ ПРОКУРОРА:")
    print(response)
    print("\n✅ Тест ПРОКУРОРА пройден")


def test_judge():
    """Тест СУДЬЯ (Сфера 049)"""
    print("\n" + "="*80)
    print("ТЕСТ: МОЗГАЧ108 - СФЕРА 049 (СУДЬЯ)")
    print("="*80)
    print("⚖️  Духовная миссия: Вынесение справедливого решения")
    
    # Создаем модель
    judge = MozgachSphere049_Judge(device="cpu")
    
    # Тестовый сценарий
    print("\n📋 Тестовый сценарий: Судебное решение")
    
    test_prompt = """
Перед тобой дело:

МАТЕРИАЛЫ СЛЕДСТВИЯ:
- Показания 3 свидетелей
- Видеозапись с камер наблюдения
- Заключение экспертизы

ЗАКЛЮЧЕНИЕ ПРОКУРОРА:
Обнаружен копипаст между документами следователя и прокурора на 87%.
Это указывает на формальный подход и отсутствие независимой проверки.
Дело требует пересмотра.

Вынеси справедливое судебное решение.
"""
    
    response = judge.chat(test_prompt)
    
    print("\n⚖️  РЕШЕНИЕ СУДЬИ:")
    print(response)
    print("\n✅ Тест СУДЬИ пройден")


def test_full_legal_system():
    """Тест полной юридической системы"""
    print("\n" + "="*80)
    print("ТЕСТ: ПОЛНАЯ ЮРИДИЧЕСКАЯ СИСТЕМА (СФЕРЫ 047-049)")
    print("="*80)
    print("🙏 Три сферы служения истине")
    
    # Создаем полную систему
    legal_system = LegalModelsFactory.create_full_legal_system(device="cpu")
    
    print("\n✅ Система успешно создана:")
    print(f"   - СЛЕДОВАТЕЛЬ (Сфера 047): {type(legal_system['investigator']).__name__}")
    print(f"   - ПРОКУРОР (Сфера 048): {type(legal_system['prosecutor']).__name__}")
    print(f"   - СУДЬЯ (Сфера 049): {type(legal_system['judge']).__name__}")
    
    print("\n✅ Тест полной системы пройден")
    print("   🕉️  Харе Кришна!")


def run_all_tests():
    """Запускает все тесты"""
    print("\n" + "="*80)
    print("🧪 ЗАПУСК ВСЕХ ТЕСТОВ ЮРИДИЧЕСКИХ МОДЕЛЕЙ")
    print("="*80)
    print("⚖️  Служение истине через AI технологии")
    
    try:
        # Тест 1: Следователь
        test_investigator()
        
        # Тест 2: Прокурор
        test_prosecutor()
        
        # Тест 3: Судья
        test_judge()
        
        # Тест 4: Полная система
        test_full_legal_system()
        
        print("\n" + "="*80)
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("="*80)
        print("🙏 Истина восторжествовала")
        print("🕉️  Харе Кришна!")
        
    except Exception as e:
        print(f"\n❌ Ошибка в тестах: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Тестирование юридических мультимодальных моделей"
    )
    parser.add_argument(
        "--test",
        type=str,
        choices=["investigator", "prosecutor", "judge", "system", "all"],
        default="all",
        help="Какой тест запустить"
    )
    
    args = parser.parse_args()
    
    if args.test == "investigator":
        test_investigator()
    elif args.test == "prosecutor":
        test_prosecutor()
    elif args.test == "judge":
        test_judge()
    elif args.test == "system":
        test_full_legal_system()
    else:
        run_all_tests()



