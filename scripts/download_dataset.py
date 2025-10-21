#!/usr/bin/env python3
"""
Загрузчик датасета kene_multimodal_gift

Загружает мультимодальный датасет для обучения моделей Braindler & Mozgach

© 2025 NativeMind - NativeMindNONC License
"""

import os
import sys
from pathlib import Path
from datasets import load_dataset


def download_kene_multimodal_gift(
    output_dir: str = "./datasets/kene_multimodal_gift",
    split: str = "train"
):
    """
    Загружает датасет kene_multimodal_gift
    
    Args:
        output_dir: Директория для сохранения
        split: Какой split загружать (train/test/validation)
    """
    print("=" * 80)
    print("🎁 Загрузка датасета kene_multimodal_gift")
    print("=" * 80)
    print()
    print("📊 Информация о датасете:")
    print("   - Размер: ~1 GB")
    print("   - Файлов: 50+")
    print("   - Модальности: Изображения, Аудио, Видео")
    print()
    print("📁 Категории:")
    print("   🎵 Духовная музыка (ИКАРОС, Джив Джаго)")
    print("   🧸 Детские игрушки")
    print("   🎨 Детские рисунки")
    print("   🌴 Фото природы (Таиланд)")
    print("   🎬 Видео контент")
    print()
    
    # Создаем директорию
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Загружаем датасет
        print(f"📥 Загрузка из HuggingFace: nativemind/kene_multimodal_gift")
        print(f"   Split: {split}")
        print()
        
        dataset = load_dataset(
            "nativemind/kene_multimodal_gift",
            split=split,
            cache_dir=output_dir
        )
        
        print(f"\n✅ Датасет успешно загружен!")
        print(f"   Примеров: {len(dataset)}")
        print(f"   Директория: {output_dir}")
        
        # Показываем примеры
        print("\n📝 Примеры из датасета:")
        for i, example in enumerate(dataset.select(range(min(3, len(dataset))))):
            print(f"\n   Пример {i+1}:")
            for key, value in example.items():
                if isinstance(value, (str, int, float, bool)):
                    print(f"      {key}: {value}")
                else:
                    print(f"      {key}: <{type(value).__name__}>")
        
        # Статистика по типам файлов
        print("\n📊 Статистика:")
        
        # Сохраняем информацию о датасете
        info_path = os.path.join(output_dir, "dataset_info.txt")
        with open(info_path, 'w', encoding='utf-8') as f:
            f.write("Kene Multimodal Gift Dataset\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Размер: {len(dataset)} примеров\n")
            f.write(f"Split: {split}\n")
            f.write(f"Загружен: {os.path.dirname(os.path.abspath(__file__))}\n")
            f.write("\nИсточник: https://huggingface.co/datasets/nativemind/kene_multimodal_gift\n")
        
        print(f"   💾 Информация сохранена: {info_path}")
        
        return dataset
    
    except Exception as e:
        print(f"\n❌ Ошибка загрузки датасета: {e}")
        print("\n💡 Возможные решения:")
        print("   1. Проверьте подключение к интернету")
        print("   2. Установите datasets: pip install datasets")
        print("   3. Войдите в HuggingFace: huggingface-cli login")
        sys.exit(1)


def download_all_datasets():
    """Загружает все доступные датасеты"""
    print("\n🎁 Загрузка всех мультимодальных датасетов")
    print()
    
    datasets = [
        ("kene_multimodal_gift", "./datasets/kene_multimodal_gift"),
    ]
    
    for name, output_dir in datasets:
        print(f"\n{'='*80}")
        print(f"📦 Загрузка: {name}")
        print(f"{'='*80}\n")
        
        try:
            download_kene_multimodal_gift(output_dir)
        except Exception as e:
            print(f"⚠️  Пропускаем {name}: {e}")
            continue
    
    print("\n" + "="*80)
    print("✅ Загрузка завершена!")
    print("="*80)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Загрузка мультимодального датасета kene_multimodal_gift"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./datasets/kene_multimodal_gift",
        help="Директория для сохранения датасета"
    )
    parser.add_argument(
        "--split",
        type=str,
        default="train",
        choices=["train", "test", "validation"],
        help="Какой split загружать"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Загрузить все доступные датасеты"
    )
    
    args = parser.parse_args()
    
    if args.all:
        download_all_datasets()
    else:
        download_kene_multimodal_gift(args.output_dir, args.split)

