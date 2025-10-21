#!/usr/bin/env python3
"""
Оптимизированный файнтюнинг для M4 MacBook Pro за ночь

Стратегия:
- Маленькая модель (TinyLlama 1.1B)
- LoRA (rank=8) для минимальных вычислений
- MPS acceleration (Apple Silicon)
- Оптимизированные параметры для ~2 часа на сферу

© 2025 NativeMind - NativeMindNONC License
"""

import os
import sys
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, TaskType

def finetune_sphere_m4(
    sphere,
    dataset_path="../datasets/combined_legal_training.jsonl",
    output_dir=None,
    base_model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    max_steps=800,
    batch_size=8
):
    """
    Быстрый файнтюнинг для M4
    
    Оптимизации:
    - TinyLlama (1.1B параметров)
    - LoRA rank=8
    - MPS (Apple Silicon)
    - Ограниченные шаги (800 = ~2 часа)
    """
    
    sphere_names = {
        "047": "СЛЕДОВАТЕЛЬ",
        "048": "ПРОКУРОР",
        "049": "СУДЬЯ"
    }
    
    if output_dir is None:
        output_dir = f"../models/sphere_{sphere}_m4_overnight"
    
    print("="*80)
    print(f"⚖️  Файнтюнинг Сферы {sphere}: {sphere_names[sphere]}")
    print("="*80)
    print()
    print(f"💻 Устройство: Apple M4 (MPS)")
    print(f"📦 Базовая модель: {base_model}")
    print(f"📚 Датасет: {dataset_path}")
    print(f"🎯 Максимум шагов: {max_steps} (~2 часа)")
    print(f"💾 Выход: {output_dir}")
    print()
    
    # Создаем директорию
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Загрузка токенизатора
    print("📥 Загрузка токенизатора...")
    tokenizer = AutoTokenizer.from_pretrained(base_model)
    
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.pad_token_id = tokenizer.eos_token_id
    
    print("   ✅ Токенизатор загружен")
    
    # 2. Загрузка модели
    print("\n📥 Загрузка модели...")
    print("   🍎 Используем Apple Silicon MPS")
    
    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        torch_dtype=torch.float32,  # MPS лучше работает с FP32
        trust_remote_code=True,
        use_cache=False,  # Экономия памяти
    )
    
    # Gradient checkpointing для экономии памяти
    model.gradient_checkpointing_enable()
    
    model = model.to("mps")
    
    print("   ✅ Модель загружена на MPS")
    print(f"   📊 Параметров: {model.num_parameters():,}")
    
    # 3. LoRA - обучаем только 0.1% параметров!
    print("\n🔧 Настройка LoRA (минимальная версия для скорости)...")
    
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=8,  # Минимальный rank для скорости
        lora_alpha=16,
        lora_dropout=0.05,
        target_modules=["q_proj", "v_proj"],  # Только 2 модуля
        bias="none"
    )
    
    model = get_peft_model(model, lora_config)
    
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    
    print(f"   ✅ LoRA применен")
    print(f"   🎯 Обучаемых: {trainable:,} ({100*trainable/total:.2f}%)")
    print(f"   📊 Всего: {total:,}")
    
    # 4. Загрузка датасета
    print(f"\n📚 Загрузка датасета...")
    dataset = load_dataset('json', data_files=dataset_path, split='train')
    
    # Фильтруем по сфере (или берем все для диалога)
    role_map = {
        "047": "sphere_047_investigator",
        "048": "sphere_048_prosecutor",
        "049": "sphere_049_judge"
    }
    
    # Берем примеры сферы + общие примеры для диалога
    filtered = dataset.filter(
        lambda x: x.get('role') == role_map.get(sphere) or x.get('sphere') == 'general'
    )
    
    print(f"   📊 Примеров для Сферы {sphere}: {len(filtered)}")
    
    # 5. Токенизация
    print("\n🔤 Токенизация...")
    
    def format_prompt(example):
        """Формат Llama/Alpaca"""
        instruction = example.get('instruction', '')
        input_text = example.get('input', '')
        output_text = example.get('output', '')
        
        if input_text:
            prompt = f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Response:\n{output_text}"
        else:
            prompt = f"### Instruction:\n{instruction}\n\n### Response:\n{output_text}"
        
        return tokenizer(
            prompt,
            truncation=True,
            max_length=1024,  # Короче для скорости
            padding="max_length"
        )
    
    tokenized = filtered.map(
        format_prompt,
        remove_columns=filtered.column_names,
        desc="Токенизация"
    )
    
    print(f"   ✅ Токенизировано: {len(tokenized)} примеров")
    
    # 6. Training arguments - оптимизировано для M4!
    print("\n⚙️  Параметры обучения (оптимизировано для M4)...")
    
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=1,
        per_device_train_batch_size=1,  # Минимум для экономии памяти!
        gradient_accumulation_steps=16,  # Эффективный batch = 16
        learning_rate=5e-4,
        warmup_steps=50,
        logging_steps=20,
        save_steps=300,
        save_total_limit=1,  # Храним только последний checkpoint
        max_steps=max_steps,
        fp16=False,
        bf16=False,
        use_cpu=False,
        optim="adamw_torch",
        logging_dir=f"{output_dir}/logs",
        report_to=[],
        remove_unused_columns=False,
        gradient_checkpointing=True,  # Экономия памяти!
        dataloader_num_workers=0,  # Без параллельной загрузки
    )
    
    print("   ✅ Параметры:")
    print(f"      Эпох: 1")
    print(f"      Batch size: {batch_size}")
    print(f"      Градиент accumulation: 2")
    print(f"      Max steps: {max_steps}")
    print(f"      Эффективный batch: {batch_size * 2}")
    
    # 7. Trainer
    print("\n🏗️  Создание Trainer...")
    
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized,
        data_collator=data_collator
    )
    
    print("   ✅ Trainer готов")
    
    # 8. ОБУЧЕНИЕ
    print(f"\n{'='*80}")
    print(f"🏋️  НАЧИНАЕМ ОБУЧЕНИЕ Сферы {sphere}: {sphere_names[sphere]}")
    print(f"{'='*80}")
    print()
    print("🙏 Духовная миссия: Служение истине через обучение AI")
    print(f"⏱️  Ожидаемое время: ~2 часа")
    print()
    
    try:
        trainer.train()
        print("\n✅ Обучение завершено!")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 9. Сохранение
    print(f"\n💾 Сохранение модели...")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    # README
    readme = f"""# {sphere_names[sphere]} - Сфера {sphere} (M4 Overnight)

**Базовая модель:** {base_model}  
**Обучено на:** M4 MacBook Pro за ~2 часа  
**Метод:** LoRA (rank=8)  
**Датасет:** Реальное уголовное дело + Alpaca + Kene

## Использование

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

base = AutoModelForCausalLM.from_pretrained("{base_model}")
model = PeftModel.from_pretrained(base, "{output_dir}")
tokenizer = AutoTokenizer.from_pretrained("{output_dir}")

prompt = "Проанализируй документ..."
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_length=512)
print(tokenizer.decode(outputs[0]))
```

**⚖️ Истина восторжествует! 🕉️**
"""
    
    with open(os.path.join(output_dir, "README.md"), 'w', encoding='utf-8') as f:
        f.write(readme)
    
    print(f"\n{'='*80}")
    print(f"✅ СФЕРА {sphere} ОБУЧЕНА!")
    print(f"{'='*80}")
    print(f"\n📁 {output_dir}")
    print(f"🙏 Служение истине продолжается...")
    
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--sphere", required=True, choices=["047", "048", "049"])
    parser.add_argument("--dataset", default="../datasets/combined_legal_training.jsonl")
    parser.add_argument("--output", default=None)
    parser.add_argument("--steps", type=int, default=800)
    parser.add_argument("--batch-size", type=int, default=8)
    
    args = parser.parse_args()
    
    finetune_sphere_m4(
        sphere=args.sphere,
        dataset_path=args.dataset,
        output_dir=args.output,
        max_steps=args.steps,
        batch_size=args.batch_size
    )

