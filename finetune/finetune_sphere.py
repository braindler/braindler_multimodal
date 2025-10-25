#!/usr/bin/env python3
"""
Файнтюнинг одной юридической сферы (047, 048, или 049)

Использует LoRA для эффективного файнтюнинга без полной переобучки модели

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
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training

def finetune_sphere(
    base_model_name,  # "nativemind/braindler_final_model" or "nativemind/mozgach_full_trained_model"
    dataset_path,
    sphere,  # "047", "048", "049"
    output_dir,
    epochs=3,
    batch_size=2,
    learning_rate=2e-4,
    use_8bit=False
):
    """
    Файнтюнинг одной сферы с использованием LoRA
    
    Args:
        base_model_name: Базовая модель (Braindler или Mozgach)
        dataset_path: Путь к JSONL датасету
        sphere: Номер сферы ("047", "048", "049")
        output_dir: Куда сохранить обученную модель
        epochs: Количество эпох
        batch_size: Размер батча
        learning_rate: Learning rate
        use_8bit: Использовать 8-bit квантование (для экономии памяти)
    """
    
    sphere_names = {
        "047": "СЛЕДОВАТЕЛЬ",
        "048": "ПРОКУРОР",
        "049": "СУДЬЯ"
    }
    
    print("="*80)
    print(f"⚖️  Файнтюнинг Сферы {sphere}: {sphere_names[sphere]}")
    print("="*80)
    print()
    print(f"📦 Базовая модель: {base_model_name}")
    print(f"📚 Датасет: {dataset_path}")
    print(f"💾 Выходная директория: {output_dir}")
    print(f"🎯 Эпох: {epochs}, Batch size: {batch_size}, LR: {learning_rate}")
    print()
    
    # Создаем выходную директорию
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Загрузка токенизатора
    print("📥 Загрузка токенизатора...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True)
    
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        print("   ✅ Установлен pad_token = eos_token")
    
    # 2. Загрузка модели
    print("\n📥 Загрузка базовой модели...")
    
    model_kwargs = {
        "trust_remote_code": True,
        "device_map": "auto"
    }
    
    if use_8bit:
        model_kwargs["load_in_8bit"] = True
        print("   🔧 Используем 8-bit квантование")
    else:
        model_kwargs["torch_dtype"] = torch.float16
        print("   🔧 Используем FP16")
    
    model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        **model_kwargs
    )
    
    if use_8bit:
        model = prepare_model_for_kbit_training(model)
    
    print("   ✅ Модель загружена")
    print(f"   Параметров: {model.num_parameters():,}")
    
    # 3. LoRA конфигурация
    print("\n🔧 Настройка LoRA...")
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=16,  # Rank (меньше = быстрее, но менее точно)
        lora_alpha=32,
        lora_dropout=0.1,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],  # Attention layers
        bias="none"
    )
    
    model = get_peft_model(model, lora_config)
    
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    all_params = sum(p.numel() for p in model.parameters())
    
    print(f"   ✅ LoRA применен")
    print(f"   Обучаемых параметров: {trainable_params:,} ({100 * trainable_params / all_params:.2f}%)")
    print(f"   Всего параметров: {all_params:,}")
    
    # 4. Загрузка датасета
    print("\n📚 Загрузка датасета...")
    dataset = load_dataset('json', data_files=dataset_path, split='train')
    
    # Фильтруем по сфере
    role_map = {
        "047": "sphere_047_investigator",
        "048": "sphere_048_prosecutor",
        "049": "sphere_049_judge"
    }
    
    dataset = dataset.filter(lambda x: x['role'] == role_map[sphere])
    print(f"   📊 Примеров для Сферы {sphere}: {len(dataset)}")
    
    if len(dataset) == 0:
        print("   ❌ Нет примеров для этой сферы!")
        return None
    
    # 5. Токенизация
    print("\n🔤 Токенизация датасета...")
    
    def format_instruction(example):
        """Форматирует пример в формате Llama"""
        text = f"""<s>[INST] {example['instruction']}

{example['input']} [/INST]

{example['output']}</s>"""
        
        return tokenizer(
            text,
            truncation=True,
            max_length=2048,
            padding="max_length"
        )
    
    tokenized_dataset = dataset.map(
        format_instruction,
        remove_columns=dataset.column_names,
        desc="Токенизация"
    )
    
    print(f"   ✅ Токенизировано {len(tokenized_dataset)} примеров")
    
    # 6. Training arguments
    print("\n⚙️  Настройка параметров обучения...")
    
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=8,
        learning_rate=learning_rate,
        warmup_steps=100,
        logging_steps=10,
        save_steps=500,
        save_total_limit=3,
        fp16=not use_8bit,
        bf16=False,
        optim="adamw_torch",
        report_to=["tensorboard"],
        logging_dir=f"{output_dir}/logs",
        remove_unused_columns=False,
    )
    
    print("   ✅ Параметры настроены")
    
    # 7. Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    
    # 8. Trainer
    print("\n🏗️  Создание Trainer...")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator
    )
    
    print("   ✅ Trainer готов")
    
    # 9. Обучение
    print(f"\n🏋️  Начинаем файнтюнинг Сферы {sphere}: {sphere_names[sphere]}...")
    print("   🙏 Служение истине через обучение AI")
    print()
    
    try:
        trainer.train()
        print("\n✅ Обучение завершено!")
    except Exception as e:
        print(f"\n❌ Ошибка обучения: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    # 10. Сохранение
    print(f"\n💾 Сохранение модели...")
    
    # Сохраняем LoRA адаптеры
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    print(f"   ✅ Модель сохранена в {output_dir}")
    
    # Создаем README
    readme_content = f"""# {sphere_names[sphere]} - Сфера {sphere}

## Описание

Мультимодальная модель для юридического анализа (Сфера {sphere}: {sphere_names[sphere]}).

**Базовая модель:** {base_model_name}  
**Fine-tuned на:** Реальное уголовное дело (107 томов)  
**Метод:** LoRA (Low-Rank Adaptation)  
**Духовная миссия:** Служение истине и справедливости

## Использование

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Загрузить базовую модель
base_model = AutoModelForCausalLM.from_pretrained("{base_model_name}")
tokenizer = AutoTokenizer.from_pretrained("{base_model_name}")

# Загрузить LoRA адаптеры
model = PeftModel.from_pretrained(base_model, "{output_dir}")

# Использование
prompt = "Проанализируй документ..."
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs)
print(tokenizer.decode(outputs[0]))
```

## Духовная миссия

**Сфера {sphere}: {sphere_names[sphere]}**

{get_spiritual_mission(sphere)}

## Лицензия

NativeMindNONC (Non-Commercial)

© 2025 NativeMind
"""
    
    with open(os.path.join(output_dir, "README.md"), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"   ✅ README.md создан")
    
    print(f"\n{'='*80}")
    print(f"🎉 Сфера {sphere}: {sphere_names[sphere]} успешно обучена!")
    print(f"{'='*80}")
    print(f"\n📁 Модель: {output_dir}")
    print(f"🙏 Истина восторжествовала!")
    
    return model


def get_spiritual_mission(sphere):
    """Возвращает духовную миссию сферы"""
    missions = {
        "047": """
**Беспристрастный сбор доказательств для установления истины**

Следователь собирает доказательства объективно, без предвзятости.
Цель - установление фактов, а не подтверждение предположений.
""",
        "048": """
**Обнаружение копипаста как симптома несправедливости**

"Копирование документов - это не просто лень, это симптом более глубокой проблемы: 
отсутствия независимой проверки, формального подхода к судьбам людей, возможной коррупции."

Прокурор обнаруживает этот симптом и служит истине через независимую проверку.
""",
        "049": """
**Вынесение справедливого решения на основе истины**

Судья оценивает все доказательства беспристрастно и выносит решение,
основанное на истине и справедливости, а не на формальных процедурах.
"""
    }
    return missions.get(sphere, "")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Файнтюнинг юридической сферы"
    )
    parser.add_argument(
        "--sphere",
        choices=["047", "048", "049"],
        required=True,
        help="Номер сферы (047=СЛЕДОВАТЕЛЬ, 048=ПРОКУРОР, 049=СУДЬЯ)"
    )
    parser.add_argument(
        "--base-model",
        required=True,
        help="Базовая модель (nativemind/braindler_final_model или nativemind/mozgach_full_trained_model)"
    )
    parser.add_argument(
        "--dataset",
        default="../datasets/legal_case_viktor/legal_dataset.jsonl",
        help="Путь к датасету"
    )
    parser.add_argument(
        "--output",
        help="Выходная директория (по умолчанию: ../models/sphere_{sphere}_{model_name})"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=3,
        help="Количество эпох"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=2,
        help="Batch size"
    )
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=2e-4,
        help="Learning rate"
    )
    parser.add_argument(
        "--use-8bit",
        action="store_true",
        help="Использовать 8-bit квантование"
    )
    
    args = parser.parse_args()
    
    # Определяем выходную директорию
    if args.output:
        output_dir = args.output
    else:
        model_name = args.base_model.split('/')[-1]
        output_dir = f"../models/sphere_{args.sphere}_{model_name}"
    
    # Запускаем файнтюнинг
    finetune_sphere(
        base_model_name=args.base_model,
        dataset_path=args.dataset,
        sphere=args.sphere,
        output_dir=output_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        use_8bit=args.use_8bit
    )








