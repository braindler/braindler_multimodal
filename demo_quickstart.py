#!/usr/bin/env python3
"""
Демонстрация quickstart для мультимодального Braindler & Mozgach

Простая демонстрация без загрузки тяжелых моделей

© 2025 NativeMind - NativeMindNONC License
"""

import sys
import os

# Добавляем src в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("="*80)
print("🚀 QUICKSTART: Мультимодальный Braindler & Mozgach")
print("="*80)
print()

# Проверка 1: Импорты
print("📦 Шаг 1: Проверка импортов...")
print("   📋 Проверяем наличие всех модулей...")

# Проверяем, что файлы существуют
required_files = [
    'src/multimodal_model.py',
    'src/vision_encoder.py', 
    'src/ocr_engine.py',
    'src/legal_analyzer.py',
    'src/legal_models.py'
]

for file in required_files:
    if os.path.exists(file):
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} не найден")

# Импортируем без загрузки тяжелых моделей
try:
    # Проверяем, что torch доступен
    import torch
    print("   ✅ PyTorch установлен")
    
    # Проверяем transformers
    import transformers
    print("   ✅ Transformers установлен")
    
    # Проверяем PIL
    from PIL import Image
    print("   ✅ PIL (Pillow) установлен")
    
    # Проверяем datasets
    from datasets import load_dataset
    print("   ✅ Datasets установлен")
    
    print("\n   ✅ Все базовые зависимости установлены")
    
except ImportError as e:
    print(f"   ❌ Ошибка импорта: {e}")
    print("\n💡 Установите зависимости: pip install -r requirements.txt")
    sys.exit(1)

# Проверка 2: Структура проекта
print("\n🔍 Шаг 2: Проверка структуры проекта...")

structure = {
    'src/': ['multimodal_model.py', 'vision_encoder.py', 'ocr_engine.py', 
             'legal_analyzer.py', 'legal_models.py', 'projection.py', '__init__.py'],
    'scripts/': ['download_dataset.py'],
    'tests/': ['test_legal_models.py'],
    'examples/': ['legal_case_example.py'],
    '': ['README.md', 'LEGAL_MODELS.md', 'QUICKSTART.md', 'requirements.txt']
}

for dir_name, files in structure.items():
    for file in files:
        path = os.path.join(dir_name, file)
        if os.path.exists(path):
            print(f"   ✅ {path}")
        else:
            print(f"   ⚠️  {path} отсутствует")

print("\n   ✅ Структура проекта проверена")

# Проверка 3: Зависимости для OCR
print("\n📝 Шаг 3: Проверка зависимостей OCR...")
try:
    import pytesseract
    print("   ✅ pytesseract установлен")
except ImportError:
    print("   ⚠️  pytesseract не установлен")
    print("   💡 pip install pytesseract")

try:
    import PyMuPDF
    print("   ✅ PyMuPDF установлен")
except ImportError:
    print("   ⚠️  PyMuPDF не установлен (опционально)")
    print("   💡 pip install PyMuPDF")

# Проверка 4: Алгоритмы сравнения
print("\n⚖️  Шаг 4: Проверка алгоритмов сравнения...")
try:
    from Levenshtein import ratio as levenshtein_ratio
    print("   ✅ python-Levenshtein установлен")
    
    from fuzzywuzzy import fuzz
    print("   ✅ fuzzywuzzy установлен")
    
    import difflib
    print("   ✅ difflib (встроенный)")
except ImportError as e:
    print(f"   ❌ Ошибка: {e}")

# Проверка 5: Юридические модели (информация)
print("\n🏭 Шаг 5: Юридические модели (Сферы 047-049)...")
print("   📋 Система 108 сфер Мозгач:")
print()
print("   СФЕРА 047: СЛЕДОВАТЕЛЬ 🔍")
print("      Духовная миссия: Беспристрастный сбор доказательств")
print("      Категория: Мониторинговая (аналогия с Погодным спутником)")
print()
print("   СФЕРА 048: ПРОКУРОР ⚖️")
print("      Духовная миссия: Обнаружение копипаста - служение истине")
print("      Ключевая функция: Выявление несправедливости")
print("      Категория: Мониторинговая проверка (Климатический спутник)")
print()
print("   СФЕРА 049: СУДЬЯ ⚖️")
print("      Духовная миссия: Вынесение справедливого решения")
print("      Категория: Мониторинговая финальная оценка")
print()
print("   ✅ Три сферы служения истине готовы")

# Проверка 6: Демонстрация детектора копипаста
print("\n🔍 Шаг 6: Демонстрация алгоритма детектора копипаста...")
print("   Тестовые документы:")

doc1 = """На основании проведенного расследования установлено, что подозреваемый 
находился на месте преступления в указанное время. Свидетели подтверждают 
его присутствие. Материальные доказательства соответствуют обвинению."""

doc2 = """На основании проведенного расследования установлено, что подозреваемый 
находился на месте преступления в указанное время. Свидетели подтверждают 
его присутствие. Материальные доказательства соответствуют обвинению."""

try:
    import difflib
    from Levenshtein import ratio as levenshtein_ratio
    from fuzzywuzzy import fuzz
    
    # Используем три алгоритма
    seq_ratio = difflib.SequenceMatcher(None, doc1, doc2).ratio() * 100
    lev_ratio = levenshtein_ratio(doc1, doc2) * 100
    fuzzy_ratio = fuzz.token_sort_ratio(doc1, doc2)
    
    # Среднее взвешенное
    similarity = (seq_ratio * 0.4 + lev_ratio * 0.3 + fuzzy_ratio * 0.3)
    
    print(f"\n   📊 Результаты анализа:")
    print(f"      SequenceMatcher: {seq_ratio:.2f}%")
    print(f"      Levenshtein: {lev_ratio:.2f}%")
    print(f"      FuzzyWuzzy: {fuzzy_ratio:.2f}%")
    print(f"   📊 Итоговое сходство: {similarity:.2f}%")
    
    if similarity >= 80:
        print("\n   🔴 КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ: Обнаружен копипаст!")
        print("   ⚠️  Это симптом возможной несправедливости:")
        print("      • Отсутствие независимой проверки")
        print("      • Формальный подход к судьбам людей")  
        print("      • Возможная коррупция")
    elif similarity >= 60:
        print("\n   ⚠️  СЕРЬЕЗНОЕ ПОДОЗРЕНИЕ: Высокий уровень совпадений")
    else:
        print("\n   ✅ Независимая проверка подтверждена")
    
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()

# Итоговая информация
print("\n" + "="*80)
print("✅ QUICKSTART ЗАВЕРШЕН")
print("="*80)
print()
print("📚 Следующие шаги:")
print()
print("1. Изучите документацию:")
print("   • README.md - Полный обзор")
print("   • LEGAL_MODELS.md - Юридические модели (Сферы 047-049)")
print("   • QUICKSTART.md - Подробный гайд")
print()
print("2. Загрузите датасет:")
print("   python scripts/download_dataset.py")
print()
print("3. Запустите тесты (требуют моделей):")
print("   python tests/test_legal_models.py --test all")
print()
print("4. Попробуйте примеры:")
print("   python examples/legal_case_example.py --example copypaste")
print()
print("⚠️  ВНИМАНИЕ: Для работы моделей нужно:")
print("   • Установить transformers, torch, PIL")
print("   • Загрузить модели Braindler/Mozgach")
print("   • ~8GB RAM (минимум), 16GB+ (рекомендуется)")
print()
print("🙏 Духовная миссия:")
print('   "Нам важно понять истину и действительно разобраться"')
print()
print("⚖️  Истина восторжествует! 🕉️  Харе Кришна!")
print()

