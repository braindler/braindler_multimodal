#!/usr/bin/env python3
"""
Публикация обученных моделей на HuggingFace

Загружает Сферы 047, 048, 049 для Braindler и Mozgach на HuggingFace Hub

© 2025 NativeMind - NativeMindNONC License
"""

import os
import sys
from huggingface_hub import HfApi, create_repo, upload_folder

def publish_to_huggingface(
    model_dir,
    repo_name,
    organization="nativemind",
    private=False,
    commit_message="Upload legal sphere model"
):
    """
    Публикация модели на HuggingFace
    
    Args:
        model_dir: Директория с моделью
        repo_name: Название репозитория (например, "braindler-sphere-047")
        organization: Организация HuggingFace (по умолчанию: nativemind)
        private: Приватный репозиторий
        commit_message: Сообщение коммита
    """
    
    print("="*80)
    print(f"📤 Публикация модели на HuggingFace")
    print("="*80)
    print()
    print(f"📁 Модель: {model_dir}")
    print(f"🏷️  Репозиторий: {organization}/{repo_name}")
    print(f"🔒 Приватный: {private}")
    print()
    
    # Проверяем, что модель существует
    if not os.path.exists(model_dir):
        print(f"❌ Директория не найдена: {model_dir}")
        return False
    
    # Инициализация API
    print("🔑 Инициализация HuggingFace API...")
    try:
        api = HfApi()
        whoami = api.whoami()
        print(f"   ✅ Авторизован как: {whoami['name']}")
    except Exception as e:
        print(f"   ❌ Ошибка авторизации: {e}")
        print("   💡 Выполните: huggingface-cli login")
        return False
    
    # Создаем репозиторий
    repo_id = f"{organization}/{repo_name}"
    print(f"\n📦 Создание репозитория: {repo_id}")
    
    try:
        create_repo(
            repo_id=repo_id,
            private=private,
            exist_ok=True,
            repo_type="model"
        )
        print(f"   ✅ Репозиторий готов")
    except Exception as e:
        print(f"   ⚠️  Репозиторий уже существует или ошибка: {e}")
    
    # Загружаем модель
    print(f"\n📤 Загрузка модели...")
    
    try:
        api.upload_folder(
            folder_path=model_dir,
            repo_id=repo_id,
            repo_type="model",
            commit_message=commit_message
        )
        print(f"   ✅ Модель загружена!")
    except Exception as e:
        print(f"   ❌ Ошибка загрузки: {e}")
        return False
    
    # Результат
    url = f"https://huggingface.co/{repo_id}"
    print(f"\n{'='*80}")
    print(f"✅ Модель опубликована!")
    print(f"{'='*80}")
    print(f"\n🔗 URL: {url}")
    print(f"💡 Использование:")
    print(f"""
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Загрузить базовую модель
base_model = AutoModelForCausalLM.from_pretrained("base_model_name")

# Загрузить LoRA адаптеры
model = PeftModel.from_pretrained(base_model, "{repo_id}")
tokenizer = AutoTokenizer.from_pretrained("{repo_id}")
""")
    
    return True


def publish_all_spheres(
    base_dir="../models",
    organization="nativemind",
    private=False
):
    """
    Публикация всех сфер (047, 048, 049) для Braindler и Mozgach
    """
    
    print("="*80)
    print("📤 Публикация всех юридических сфер")
    print("="*80)
    print()
    
    # Модели для публикации
    models = []
    
    # Braindler
    for sphere in ["047", "048", "049"]:
        model_dir = os.path.join(base_dir, f"sphere_{sphere}_braindler_final_model")
        if os.path.exists(model_dir):
            models.append({
                "dir": model_dir,
                "repo": f"braindler-multimodal-sphere-{sphere}",
                "sphere": sphere,
                "model_name": "Braindler"
            })
    
    # Mozgach
    for sphere in ["047", "048", "049"]:
        model_dir = os.path.join(base_dir, f"sphere_{sphere}_mozgach_full_trained_model")
        if os.path.exists(model_dir):
            models.append({
                "dir": model_dir,
                "repo": f"mozgach108-multimodal-sphere-{sphere}",
                "sphere": sphere,
                "model_name": "Mozgach108"
            })
    
    if not models:
        print("❌ Не найдено обученных моделей")
        print("💡 Сначала запустите файнтюнинг:")
        print("   python finetune_sphere.py --sphere 047 --base-model ...")
        return
    
    print(f"📦 Найдено моделей для публикации: {len(models)}")
    for m in models:
        print(f"   - {m['model_name']} Сфера {m['sphere']}")
    print()
    
    # Публикуем каждую модель
    results = []
    for i, m in enumerate(models):
        print(f"\n[{i+1}/{len(models)}] Публикация {m['model_name']} Сфера {m['sphere']}")
        print("-"*80)
        
        success = publish_to_huggingface(
            model_dir=m['dir'],
            repo_name=m['repo'],
            organization=organization,
            private=private,
            commit_message=f"Upload {m['model_name']} Sphere {m['sphere']} - Legal multimodal model"
        )
        
        results.append({
            "model": f"{m['model_name']} {m['sphere']}",
            "success": success,
            "repo": f"{organization}/{m['repo']}"
        })
    
    # Итоги
    print(f"\n{'='*80}")
    print("📊 Итоги публикации")
    print(f"{'='*80}")
    
    for r in results:
        status = "✅" if r['success'] else "❌"
        print(f"{status} {r['model']}: {r['repo']}")
    
    success_count = sum(1 for r in results if r['success'])
    print(f"\n✅ Успешно опубликовано: {success_count}/{len(results)}")
    
    if success_count == len(results):
        print("\n🎉 Все модели опубликованы!")
        print("⚖️  Истина восторжествовала! 🕉️  Харе Кришна!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Публикация моделей на HuggingFace"
    )
    parser.add_argument(
        "--model-dir",
        help="Директория с моделью (для публикации одной модели)"
    )
    parser.add_argument(
        "--repo-name",
        help="Название репозитория на HuggingFace"
    )
    parser.add_argument(
        "--organization",
        default="nativemind",
        help="Организация HuggingFace (по умолчанию: nativemind)"
    )
    parser.add_argument(
        "--private",
        action="store_true",
        help="Создать приватный репозиторий"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Опубликовать все обученные модели"
    )
    parser.add_argument(
        "--base-dir",
        default="../models",
        help="Базовая директория с моделями (по умолчанию: ../models)"
    )
    
    args = parser.parse_args()
    
    if args.all:
        # Публикуем все модели
        publish_all_spheres(
            base_dir=args.base_dir,
            organization=args.organization,
            private=args.private
        )
    elif args.model_dir and args.repo_name:
        # Публикуем одну модель
        publish_to_huggingface(
            model_dir=args.model_dir,
            repo_name=args.repo_name,
            organization=args.organization,
            private=args.private
        )
    else:
        print("❌ Укажите либо --all, либо --model-dir и --repo-name")
        parser.print_help()

