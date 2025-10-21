#!/bin/bash
set -e
cd "$(dirname "$0")/.."
source venv/bin/activate

echo "🌙 Начало: $(date '+%H:%M')"
echo "⏰ ~8 часов до завершения"
echo ""

# Сфера 047
echo "🔍 Сфера 047..."
python finetune/finetune_overnight_m4.py --sphere 047 --dataset datasets/legal_108_perfect.jsonl --steps 600 --batch-size 8

# Сфера 048 (КЛЮЧЕВАЯ!)
echo "⚖️ Сфера 048..."
python finetune/finetune_overnight_m4.py --sphere 048 --dataset datasets/legal_108_perfect.jsonl --steps 600 --batch-size 8

# Сфера 049
echo "⚖️ Сфера 049..."
python finetune/finetune_overnight_m4.py --sphere 049 --dataset datasets/legal_108_perfect.jsonl --steps 600 --batch-size 8

echo "✅ Завершено: $(date '+%H:%M')"
echo "⚖️ Истина восторжествовала! 🕉️"
