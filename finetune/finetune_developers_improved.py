#!/usr/bin/env python3
"""
Улучшенный файнтюнинг сфер разработки (073-078) с высококачественным датасетом

Улучшенные параметры обучения для лучшего качества

© 2025 NativeMind - NativeMindNONC License
"""

import os
import sys
import torch
import argparse
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training
import json

def finetune_developer_sphere_improved(
    sphere,
    dataset_path,
    output_dir,
    base_model="nativemind/shridhar_8k_multimodal",
    epochs=5,  # Увеличено с 3 до 5
    batch_size=4,  # Увеличено с 2 до 4
    learning_rate=1e-4,  # Уменьшено с 2e-4 до 1e-4
    use_8bit=False
):
    """
    Улучшенный файнтюнинг одной сферы разработки
    
    Args:
        sphere: Номер сферы ("073", "074", "075", "076", "077", "078")
        dataset_path: Путь к JSONL датасету
        output_dir: Куда сохранить обученную модель
        base_model: Базовая модель
        epochs: Количество эпох (увеличено до 5)
        batch_size: Размер батча (увеличено до 4)
        learning_rate: Learning rate (уменьшено до 1e-4)
        use_8bit: Использовать 8-bit квантование
    """
    
    sphere_names = {
        "073": "DEVELOPER",
        "074": "CODE_REVIEWER", 
        "075": "ARCHITECT",
        "076": "DEVOPS",
        "077": "QA_TESTER",
        "078": "TECH_WRITER"
    }
    
    print("="*80)
    print(f"🚀 УЛУЧШЕННЫЙ ФАЙНТЮНИНГ Сферы {sphere}: {sphere_names[sphere]}")
    print("="*80)
    print()
    print(f"📦 Базовая модель: {base_model}")
    print(f"📚 Датасет: {dataset_path}")
    print(f"💾 Выходная директория: {output_dir}")
    print(f"🎯 Эпох: {epochs}, Batch size: {batch_size}, LR: {learning_rate}")
    print()
    
    # Проверка устройства
    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"💻 Устройство: {device.upper()}")
    
    # Загрузка токенизатора
    print("\n📥 Загрузка токенизатора...")
    tokenizer = AutoTokenizer.from_pretrained(base_model)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    print("   ✅ Токенизатор загружен")
    
    # Загрузка модели
    print("\n📥 Загрузка модели...")
    model_kwargs = {
        "torch_dtype": torch.float16 if device == "cuda" else torch.float32,
        "device_map": "auto" if device == "cuda" else None,
    }
    
    if use_8bit and device == "cuda":
        model_kwargs["load_in_8bit"] = True
        model_kwargs["device_map"] = "auto"
    
    model = AutoModelForCausalLM.from_pretrained(base_model, **model_kwargs)
    
    if device == "mps":
        model = model.to("mps")
    elif device == "cpu":
        model = model.to("cpu")
    
    print(f"   ✅ Модель загружена на {device.upper()}")
    print(f"   📊 Параметров: {model.num_parameters():,}")
    
    # Улучшенная настройка LoRA
    print("\n🔧 Настройка LoRA (улучшенная)...")
    lora_config = LoraConfig(
        r=32,  # Увеличено с 16 до 32 для лучшего качества
        lora_alpha=64,  # Увеличено с 32 до 64
        lora_dropout=0.05,  # Уменьшено с 0.1 до 0.05
        target_modules=["c_attn", "c_proj", "c_fc"],  # Добавлен c_fc
        task_type=TaskType.CAUSAL_LM,
    )
    
    if use_8bit and device == "cuda":
        model = prepare_model_for_kbit_training(model)
    
    model = get_peft_model(model, lora_config)
    print("   ✅ LoRA применен (улучшенная конфигурация)")
    print(f"   🎯 Обучаемых параметров: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}")
    
    # Загрузка датасета
    print(f"\n📚 Загрузка датасета...")
    dataset = load_dataset('json', data_files=dataset_path, split='train')
    
    # Фильтрация по сфере
    def filter_sphere(example):
        return example.get('sphere') == sphere
    
    filtered_dataset = dataset.filter(filter_sphere)
    print(f"   📊 Примеров для Сферы {sphere}: {len(filtered_dataset)}")
    
    # Улучшенная токенизация
    def tokenize_function(examples):
        texts = []
        for i in range(len(examples['instruction'])):
            instruction = examples['instruction'][i]
            input_text = examples['input'][i] if examples['input'][i] else ""
            output = examples['output'][i]
            
            # Улучшенный формат промпта
            if input_text:
                text = f"### Роль: {sphere_names[sphere]}\n### Задача:\n{instruction}\n\n### Входные данные:\n{input_text}\n\n### Решение:\n{output}"
            else:
                text = f"### Роль: {sphere_names[sphere]}\n### Задача:\n{instruction}\n\n### Решение:\n{output}"
            
            texts.append(text)
        
        return tokenizer(
            texts,
            truncation=True,
            padding=True,
            max_length=4096,  # Увеличено с 2048 до 4096
            return_tensors="pt"
        )
    
    print("   🔤 Токенизация (улучшенная)...")
    tokenized_dataset = filtered_dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=filtered_dataset.column_names
    )
    print(f"   ✅ Токенизировано: {len(tokenized_dataset)} примеров")
    
    # Улучшенные параметры обучения
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=8,  # Увеличено с 4 до 8
        learning_rate=learning_rate,
        warmup_steps=200,  # Увеличено с 100 до 200
        logging_steps=5,  # Уменьшено с 10 до 5 для более частого логирования
        save_steps=50,  # Уменьшено с 100 до 50 для более частого сохранения
        save_strategy="steps",
        load_best_model_at_end=False,
        report_to=None,
        remove_unused_columns=False,
        dataloader_pin_memory=False if device == "mps" else True,
        # Новые параметры для улучшения качества
        fp16=torch.cuda.is_available(),  # Использовать fp16 на GPU
        dataloader_num_workers=0,  # Отключить многопоточность для стабильности
        seed=42,  # Фиксированный seed для воспроизводимости
        weight_decay=0.01,  # Добавить weight decay
        adam_beta1=0.9,
        adam_beta2=0.999,
        adam_epsilon=1e-8,
    )
    
    print(f"\n⚙️  Улучшенные параметры обучения:")
    print(f"   ✅ Эпох: {epochs} (увеличено)")
    print(f"   ✅ Batch size: {batch_size} (увеличено)")
    print(f"   ✅ Градиент accumulation: 8 (увеличено)")
    print(f"   ✅ Learning rate: {learning_rate} (уменьшено)")
    print(f"   ✅ Warmup steps: 200 (увеличено)")
    print(f"   ✅ Max length: 4096 (увеличено)")
    print(f"   ✅ Эффективный batch: {batch_size * 8}")
    
    # Создание Trainer
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator,
    )
    
    print("\n🏗️  Создание Trainer...")
    print("   ✅ Trainer готов (улучшенная конфигурация)")
    
    # Обучение
    print("\n" + "="*80)
    print(f"🏋️  НАЧИНАЕМ УЛУЧШЕННОЕ ОБУЧЕНИЕ Сферы {sphere}: {sphere_names[sphere]}")
    print("="*80)
    print()
    print("🙏 Духовная миссия: Служение истине через обучение AI")
    print(f"⏱️  Ожидаемое время: ~{epochs * len(tokenized_dataset) // (batch_size * 8) // 60} минут")
    print()
    
    try:
        trainer.train()
        print("\n✅ Обучение завершено!")
        
        # Сохранение модели
        print("\n💾 Сохранение модели...")
        trainer.save_model()
        tokenizer.save_pretrained(output_dir)
        print(f"   ✅ Модель сохранена в: {output_dir}")
        
        print("\n" + "="*80)
        print(f"✅ СФЕРА {sphere} УЛУЧШЕНА!")
        print("="*80)
        print(f"📁 {output_dir}")
        print("🙏 Служение истине продолжается...")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Улучшенный файнтюнинг сфер разработки")
    parser.add_argument("--sphere", required=True, choices=["073", "074", "075", "076", "077", "078"],
                       help="Номер сферы для обучения")
    parser.add_argument("--dataset", default="../datasets/developers_high_quality.jsonl",
                       help="Путь к улучшенному датасету")
    parser.add_argument("--output", default="../models",
                       help="Базовая директория для сохранения")
    parser.add_argument("--base-model", default="nativemind/shridhar_8k_multimodal",
                       help="Базовая модель")
    parser.add_argument("--epochs", type=int, default=5, help="Количество эпох (улучшено)")
    parser.add_argument("--batch-size", type=int, default=4, help="Размер батча (улучшено)")
    parser.add_argument("--learning-rate", type=float, default=1e-4, help="Learning rate (улучшено)")
    parser.add_argument("--use-8bit", action="store_true", help="Использовать 8-bit квантование")
    
    args = parser.parse_args()
    
    # Создание выходной директории
    output_dir = f"{args.output}/sphere_{args.sphere}_improved"
    os.makedirs(output_dir, exist_ok=True)
    
    # Запуск улучшенного обучения
    success = finetune_developer_sphere_improved(
        sphere=args.sphere,
        dataset_path=args.dataset,
        output_dir=output_dir,
        base_model=args.base_model,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        use_8bit=args.use_8bit
    )
    
    if success:
        print(f"\n🎉 Сфера {args.sphere} успешно улучшена!")
        sys.exit(0)
    else:
        print(f"\n💥 Ошибка при улучшении сферы {args.sphere}")
        sys.exit(1)

if __name__ == "__main__":
    main()
