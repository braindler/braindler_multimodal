#!/usr/bin/env python3
"""
Файнтюнинг сфер разработки (073-078) с базовой моделью shridhar_8k_multimodal

Сферы:
- 073: DEVELOPER
- 074: CODE_REVIEWER  
- 075: ARCHITECT
- 076: DEVOPS
- 077: QA_TESTER
- 078: TECH_WRITER

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

def finetune_developer_sphere(
    sphere,
    dataset_path,
    output_dir,
    base_model="nativemind/shridhar_8k_multimodal",
    epochs=3,
    batch_size=2,
    learning_rate=2e-4,
    use_8bit=False
):
    """
    Файнтюнинг одной сферы разработки
    
    Args:
        sphere: Номер сферы ("073", "074", "075", "076", "077", "078")
        dataset_path: Путь к JSONL датасету
        output_dir: Куда сохранить обученную модель
        base_model: Базовая модель
        epochs: Количество эпох
        batch_size: Размер батча
        learning_rate: Learning rate
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
    print(f"💻 Файнтюнинг Сферы {sphere}: {sphere_names[sphere]}")
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
    
    # Настройка LoRA
    print("\n🔧 Настройка LoRA...")
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.1,
        target_modules=["c_attn", "c_proj"],
        task_type=TaskType.CAUSAL_LM,
    )
    
    if use_8bit and device == "cuda":
        model = prepare_model_for_kbit_training(model)
    
    model = get_peft_model(model, lora_config)
    print("   ✅ LoRA применен")
    print(f"   🎯 Обучаемых параметров: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}")
    
    # Загрузка датасета
    print(f"\n📚 Загрузка датасета...")
    dataset = load_dataset('json', data_files=dataset_path, split='train')
    
    # Фильтрация по сфере
    def filter_sphere(example):
        return example.get('sphere') == sphere
    
    filtered_dataset = dataset.filter(filter_sphere)
    print(f"   📊 Примеров для Сферы {sphere}: {len(filtered_dataset)}")
    
    # Токенизация
    def tokenize_function(examples):
        texts = []
        for i in range(len(examples['instruction'])):
            instruction = examples['instruction'][i]
            input_text = examples['input'][i] if examples['input'][i] else ""
            output = examples['output'][i]
            
            if input_text:
                text = f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Response:\n{output}"
            else:
                text = f"### Instruction:\n{instruction}\n\n### Response:\n{output}"
            
            texts.append(text)
        
        return tokenizer(
            texts,
            truncation=True,
            padding=True,
            max_length=2048,
            return_tensors="pt"
        )
    
    print("   🔤 Токенизация...")
    tokenized_dataset = filtered_dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=filtered_dataset.column_names
    )
    print(f"   ✅ Токенизировано: {len(tokenized_dataset)} примеров")
    
    # Параметры обучения
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=4,
        learning_rate=learning_rate,
        warmup_steps=100,
        logging_steps=10,
        save_steps=100,
        save_strategy="steps",
        load_best_model_at_end=False,
        report_to=None,
        remove_unused_columns=False,
        dataloader_pin_memory=False if device == "mps" else True,
    )
    
    print(f"\n⚙️  Параметры обучения:")
    print(f"   ✅ Эпох: {epochs}")
    print(f"   ✅ Batch size: {batch_size}")
    print(f"   ✅ Градиент accumulation: 4")
    print(f"   ✅ Learning rate: {learning_rate}")
    print(f"   ✅ Эффективный batch: {batch_size * 4}")
    
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
    print("   ✅ Trainer готов")
    
    # Обучение
    print("\n" + "="*80)
    print(f"🏋️  НАЧИНАЕМ ОБУЧЕНИЕ Сферы {sphere}: {sphere_names[sphere]}")
    print("="*80)
    print()
    print("🙏 Духовная миссия: Служение истине через обучение AI")
    print(f"⏱️  Ожидаемое время: ~{epochs * len(tokenized_dataset) // (batch_size * 4) // 60} минут")
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
        print(f"✅ СФЕРА {sphere} ОБУЧЕНА!")
        print("="*80)
        print(f"📁 {output_dir}")
        print("🙏 Служение истине продолжается...")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Файнтюнинг сфер разработки")
    parser.add_argument("--sphere", required=True, choices=["073", "074", "075", "076", "077", "078"],
                       help="Номер сферы для обучения")
    parser.add_argument("--dataset", default="../datasets/developers_108_perfect.jsonl",
                       help="Путь к датасету")
    parser.add_argument("--output", default="../models",
                       help="Базовая директория для сохранения")
    parser.add_argument("--base-model", default="nativemind/shridhar_8k_multimodal",
                       help="Базовая модель")
    parser.add_argument("--epochs", type=int, default=3, help="Количество эпох")
    parser.add_argument("--batch-size", type=int, default=2, help="Размер батча")
    parser.add_argument("--learning-rate", type=float, default=2e-4, help="Learning rate")
    parser.add_argument("--use-8bit", action="store_true", help="Использовать 8-bit квантование")
    
    args = parser.parse_args()
    
    # Создание выходной директории
    output_dir = f"{args.output}/sphere_{args.sphere}_shridhar"
    os.makedirs(output_dir, exist_ok=True)
    
    # Запуск обучения
    success = finetune_developer_sphere(
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
        print(f"\n🎉 Сфера {args.sphere} успешно обучена!")
        sys.exit(0)
    else:
        print(f"\n💥 Ошибка при обучении сферы {args.sphere}")
        sys.exit(1)

if __name__ == "__main__":
    main()
