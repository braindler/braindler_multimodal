#!/usr/bin/env python3
"""
Подготовка датасета из томов уголовного дела Виктора

Обрабатывает 107 томов PDF → извлекает текст → создает датасет для файнтюнинга
Сферы 047 (СЛЕДОВАТЕЛЬ), 048 (ПРОКУРОР), 049 (СУДЬЯ)

© 2025 NativeMind - NativeMindNONC License
"""

import os
import sys
import json
from pathlib import Path

# Добавляем src в путь
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ocr_engine import OCREngine

def prepare_legal_dataset(
    pdf_dir="/Volumes/MOZGACH/Advokat/Ugolovka/Viktor/Тома",
    output_dir="../datasets/legal_case_viktor",
    sample_pages=10,  # Страниц из каждого тома для анализа
    max_tomes=None  # Ограничение томов для тестирования (None = все)
):
    """
    Подготовка датасета из томов дела
    
    Args:
        pdf_dir: Директория с томами PDF
        output_dir: Куда сохранить датасет
        sample_pages: Сколько страниц обрабатывать из каждого тома
        max_tomes: Максимум томов (для теста)
    """
    print("="*80)
    print("📚 Подготовка датасета из томов уголовного дела")
    print("="*80)
    print()
    print("🙏 Духовная миссия: Служение истине через AI")
    print()
    
    # Проверяем, существует ли директория
    if not os.path.exists(pdf_dir):
        print(f"❌ Директория не найдена: {pdf_dir}")
        print("💡 Убедитесь, что диск MOZGACH подключен")
        return None
    
    # Создаем OCR движок
    print("🔧 Инициализация OCR движка...")
    try:
        ocr = OCREngine(languages=['rus', 'eng'])
        print("   ✅ OCR готов")
    except Exception as e:
        print(f"   ❌ Ошибка OCR: {e}")
        print("   💡 Установите: pip install pytesseract PyMuPDF pdf2image")
        return None
    
    # Находим все PDF
    pdf_files = sorted(Path(pdf_dir).glob("*.pdf"))
    if max_tomes:
        pdf_files = pdf_files[:max_tomes]
    
    print(f"\n📁 Найдено томов: {len(pdf_files)}")
    print(f"   Обрабатываем по {sample_pages} страниц из каждого")
    print()
    
    # Создаем выходную директорию
    os.makedirs(output_dir, exist_ok=True)
    
    dataset = []
    processed_tomes = 0
    total_pages = 0
    
    for i, pdf_path in enumerate(pdf_files):
        print(f"📄 [{i+1}/{len(pdf_files)}] {pdf_path.name}")
        
        try:
            # Извлекаем текст
            texts = ocr.extract_text_from_pdf(
                str(pdf_path),
                start_page=0,
                end_page=sample_pages,
                preserve_layout=True
            )
            
            pages_processed = 0
            
            # Создаем примеры для каждой страницы
            for page_num, text in texts.items():
                if len(text.strip()) < 100:
                    continue
                
                # Чистим текст
                text_clean = text.strip()[:2000]  # Берем первые 2000 символов
                
                # СФЕРА 047: СЛЕДОВАТЕЛЬ
                dataset.append({
                    "instruction": "Ты - СЛЕДОВАТЕЛЬ (Сфера 047). Проанализируй документ с точки зрения беспристрастного сбора доказательств.",
                    "input": f"Том {pdf_path.stem}, страница {page_num+1}:\n\n{text_clean}",
                    "output": f"Как следователь, анализирую документ. Проверяю: 1) Полноту изложенных фактов, 2) Наличие противоречий, 3) Процессуальную правильность оформления, 4) Объективность изложения. Необходимо тщательно документировать все обстоятельства дела.",
                    "role": "sphere_047_investigator",
                    "sphere": "047",
                    "source_file": str(pdf_path.name),
                    "page": page_num + 1
                })
                
                # СФЕРА 048: ПРОКУРОР (КЛЮЧЕВАЯ!)
                dataset.append({
                    "instruction": "Ты - ПРОКУРОР (Сфера 048). Твоя духовная миссия - обнаружение копипаста как симптома несправедливости. Проверь документ на независимость проверки.",
                    "input": f"Том {pdf_path.stem}, страница {page_num+1}:\n\n{text_clean}",
                    "output": f"Как прокурор, провожу надзор за законностью. Проверяю: 1) Наличие признаков копипаста с материалами следствия, 2) Независимость собственной проверки, 3) Формальный ли подход к делу, 4) Служит ли документ истине. ВАЖНО: Копирование документов - симптом отсутствия независимой проверки и возможной коррупции.",
                    "role": "sphere_048_prosecutor",
                    "sphere": "048",
                    "source_file": str(pdf_path.name),
                    "page": page_num + 1
                })
                
                # СФЕРА 049: СУДЬЯ
                dataset.append({
                    "instruction": "Ты - СУДЬЯ (Сфера 049). Твоя духовная миссия - вынесение справедливого решения. Оцени документ с точки зрения служения истине.",
                    "input": f"Том {pdf_path.stem}, страница {page_num+1}:\n\n{text_clean}",
                    "output": f"Как судья, оцениваю документ беспристрастно. Анализирую: 1) Достоверность доказательств, 2) Процессуальную правильность, 3) Работу прокурора и следователя, 4) Служение истине и справедливости. Цель - восстановление справедливости, а не формальное следование процедурам.",
                    "role": "sphere_049_judge",
                    "sphere": "049",
                    "source_file": str(pdf_path.name),
                    "page": page_num + 1
                })
                
                pages_processed += 1
                total_pages += 1
            
            processed_tomes += 1
            print(f"   ✅ Обработано {pages_processed} страниц")
        
        except Exception as e:
            print(f"   ⚠️  Ошибка: {e}")
            continue
        
        # Сохраняем промежуточные результаты каждые 10 томов
        if (i + 1) % 10 == 0:
            print(f"\n💾 Промежуточное сохранение...")
            _save_dataset(dataset, output_dir, partial=True)
    
    print(f"\n{'='*80}")
    print(f"✅ Обработка завершена")
    print(f"{'='*80}")
    print(f"\n📊 Статистика:")
    print(f"   Обработано томов: {processed_tomes}")
    print(f"   Всего страниц: {total_pages}")
    print(f"   Всего примеров: {len(dataset)}")
    print()
    
    # Сохраняем финальный датасет
    _save_dataset(dataset, output_dir, partial=False)
    
    return dataset


def _save_dataset(dataset, output_dir, partial=False):
    """Сохранение датасета"""
    suffix = "_partial" if partial else ""
    
    # JSONL формат
    output_file = os.path.join(output_dir, f"legal_dataset{suffix}.jsonl")
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"   💾 Сохранено: {output_file}")
    
    # Статистика
    stats = {
        "total_examples": len(dataset),
        "examples_by_sphere": {
            "047_investigator": len([d for d in dataset if d['sphere'] == '047']),
            "048_prosecutor": len([d for d in dataset if d['sphere'] == '048']),
            "049_judge": len([d for d in dataset if d['sphere'] == '049'])
        },
        "tomes_processed": len(set([d['source_file'] for d in dataset])),
        "avg_examples_per_tome": len(dataset) / len(set([d['source_file'] for d in dataset])) if dataset else 0
    }
    
    stats_file = os.path.join(output_dir, f"stats{suffix}.json")
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"   📊 Статистика: {stats_file}")
    print(f"      - Сфера 047 (СЛЕДОВАТЕЛЬ): {stats['examples_by_sphere']['047_investigator']}")
    print(f"      - Сфера 048 (ПРОКУРОР): {stats['examples_by_sphere']['048_prosecutor']}")
    print(f"      - Сфера 049 (СУДЬЯ): {stats['examples_by_sphere']['049_judge']}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Подготовка датасета из томов уголовного дела"
    )
    parser.add_argument(
        "--pdf-dir",
        default="/Volumes/MOZGACH/Advokat/Ugolovka/Viktor/Тома",
        help="Директория с PDF томами"
    )
    parser.add_argument(
        "--output-dir",
        default="../datasets/legal_case_viktor",
        help="Куда сохранить датасет"
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=10,
        help="Страниц из каждого тома"
    )
    parser.add_argument(
        "--max-tomes",
        type=int,
        default=None,
        help="Максимум томов для обработки (для теста)"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Тестовый режим (первые 3 тома, 2 страницы)"
    )
    
    args = parser.parse_args()
    
    if args.test:
        print("\n🧪 ТЕСТОВЫЙ РЕЖИМ")
        prepare_legal_dataset(
            pdf_dir=args.pdf_dir,
            output_dir=args.output_dir,
            sample_pages=2,
            max_tomes=3
        )
    else:
        prepare_legal_dataset(
            pdf_dir=args.pdf_dir,
            output_dir=args.output_dir,
            sample_pages=args.pages,
            max_tomes=args.max_tomes
        )








