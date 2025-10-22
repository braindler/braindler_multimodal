#!/usr/bin/env python3
"""
Подготовка объединенного датасета для ночного файнтюнинга

Объединяет:
1. Юридические тексты (897 примеров из 30 томов)
2. Alpaca dataset (инструкции для диалога)
3. Kene multimodal (духовные тексты)

© 2025 NativeMind - NativeMindNONC License
"""

import json
import os
from datasets import load_dataset, concatenate_datasets, Dataset

def load_legal_dataset(path):
    """Загружает юридический датасет"""
    print("📚 Загрузка юридического датасета...")
    dataset = load_dataset('json', data_files=path, split='train')
    print(f"   ✅ Юридических примеров: {len(dataset)}")
    return dataset

def load_alpaca_dataset(path, max_examples=5000):
    """Загружает и фильтрует Alpaca датасет"""
    print("\n🦙 Загрузка Alpaca датасета...")
    dataset = load_dataset('json', data_files=path, split='train')
    
    # Фильтруем релевантные примеры (аналитические, юридические)
    keywords = ['analyze', 'evaluate', 'review', 'compare', 'assess', 
                'examine', 'investigate', 'judge', 'legal', 'evidence']
    
    filtered = dataset.filter(
        lambda x: any(word in x['instruction'].lower() for word in keywords)
    )
    
    # Ограничиваем количество
    if len(filtered) > max_examples:
        filtered = filtered.select(range(max_examples))
    
    print(f"   ✅ Alpaca примеров (отфильтровано): {len(filtered)}")
    
    # Адаптируем формат
    def adapt_format(example):
        return {
            "instruction": example['instruction'],
            "input": example.get('input', ''),
            "output": example['output'],
            "sphere": "general",  # Общие примеры
            "source": "alpaca"
        }
    
    adapted = filtered.map(adapt_format)
    return adapted

def load_kene_spiritual_texts(path):
    """Загружает духовные тексты из Kene dataset"""
    print("\n🕉️  Загрузка духовных текстов Kene...")
    
    spiritual_texts = []
    
    # Читаем тексты Шридхара Махараджа
    spiritual_dir = os.path.join(path, "Книги/Духовное/Вайшнавизм/Шридхар Махарадж")
    
    if os.path.exists(spiritual_dir):
        for file in os.listdir(spiritual_dir):
            if file.endswith('.txt'):
                try:
                    with open(os.path.join(spiritual_dir, file), 'r', encoding='utf-8') as f:
                        text = f.read()
                        
                        # Разбиваем на параграфы
                        paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 100]
                        
                        for para in paragraphs[:10]:  # Первые 10 параграфов
                            spiritual_texts.append({
                                "instruction": "Объясни духовный смысл этого текста",
                                "input": para[:800],
                                "output": "С духовной точки зрения, этот текст учит нас служению истине и справедливости. Важно понимать глубинный смысл, а не только материальную форму.",
                                "sphere": "001",  # Духовная сфера
                                "source": "kene_spiritual"
                            })
                except Exception as e:
                    print(f"      ⚠️  {file}: {e}")
    
    print(f"   ✅ Духовных примеров: {len(spiritual_texts)}")
    
    return Dataset.from_list(spiritual_texts) if spiritual_texts else None

def prepare_combined_dataset(
    legal_path="../datasets/legal_case_viktor/legal_dataset.jsonl",
    alpaca_path="/Volumes/MULTIMODAL/proj.datasets/alpaca_dataset/alpaca_data.json",
    kene_path="/Volumes/MULTIMODAL/proj.datasets/kene_multimodal_gift",
    output_path="../datasets/combined_legal_training.jsonl"
):
    """
    Объединяет все датасеты
    """
    print("="*80)
    print("🔥 Подготовка объединенного датасета для M4")
    print("="*80)
    print()
    
    datasets_to_combine = []
    
    # 1. Юридический датасет
    try:
        legal = load_legal_dataset(legal_path)
        datasets_to_combine.append(legal)
    except Exception as e:
        print(f"   ⚠️  Ошибка юридического датасета: {e}")
    
    # 2. Alpaca датасет
    try:
        alpaca = load_alpaca_dataset(alpaca_path, max_examples=3000)
        datasets_to_combine.append(alpaca)
    except Exception as e:
        print(f"   ⚠️  Ошибка Alpaca датасета: {e}")
    
    # 3. Духовные тексты Kene
    try:
        kene = load_kene_spiritual_texts(kene_path)
        if kene:
            datasets_to_combine.append(kene)
    except Exception as e:
        print(f"   ⚠️  Ошибка Kene датасета: {e}")
    
    # Объединяем
    print(f"\n🔗 Объединение датасетов...")
    combined = concatenate_datasets(datasets_to_combine)
    
    print(f"   ✅ Всего примеров: {len(combined)}")
    print()
    print("   📊 Распределение:")
    
    # Статистика по сферам
    sphere_counts = {}
    for item in combined:
        sphere = item.get('sphere', 'unknown')
        sphere_counts[sphere] = sphere_counts.get(sphere, 0) + 1
    
    for sphere, count in sorted(sphere_counts.items()):
        sphere_name = {
            "001": "Духовная",
            "047": "СЛЕДОВАТЕЛЬ",
            "048": "ПРОКУРОР",
            "049": "СУДЬЯ",
            "general": "Alpaca общие"
        }.get(sphere, sphere)
        print(f"      Сфера {sphere} ({sphere_name}): {count}")
    
    # Сохраняем
    print(f"\n💾 Сохранение объединенного датасета...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # JSONL формат
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in combined:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"   ✅ Сохранено: {output_path}")
    
    # Статистика
    stats = {
        "total_examples": len(combined),
        "sphere_distribution": sphere_counts,
        "sources": list(set([item.get('source', 'unknown') for item in combined]))
    }
    
    stats_path = output_path.replace('.jsonl', '_stats.json')
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"   📊 Статистика: {stats_path}")
    
    print("\n✅ Объединенный датасет готов!")
    print(f"🙏 Примеров для обучения: {len(combined)}")
    
    return combined

if __name__ == "__main__":
    prepare_combined_dataset()





