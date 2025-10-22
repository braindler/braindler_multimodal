#!/bin/bash
#
# Ночной файнтюнинг на M4 MacBook Pro
# 
# Запуск: ./run_overnight_m4.sh
# Время: ~8 часов (3 сферы × 2.5 часа)
#
# © 2025 NativeMind - NativeMindNONC License

set -e

echo "================================================================================"
echo "🌙 НОЧНОЙ ФАЙНТЮНИНГ на M4 MacBook Pro"
echo "================================================================================"
echo ""
echo "💻 Устройство: Apple M4"
echo "💾 Память: 32GB Shared Memory"
echo "⏱️  Время: ~8 часов (до утра)"
echo ""
echo "🙏 Духовная миссия: Служение истине через обучение AI"
echo ""

# Переходим в директорию проекта
cd "$(dirname "$0")/.."

# Активируем venv
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Проверяем, что PyTorch установлен
python -c "import torch; print(f'✅ PyTorch {torch.__version__}')" || {
    echo "❌ PyTorch не установлен"
    exit 1
}

# Проверяем MPS
python -c "import torch; print(f'✅ MPS доступен: {torch.backends.mps.is_available()}')"

# ===============================================================================
# ЭТАП 1: Подготовка объединенного датасета (30 мин)
# ===============================================================================
echo ""
echo "================================================================================"
echo "📚 ЭТАП 1: Подготовка объединенного датасета"
echo "================================================================================"
echo ""

if [ -f "datasets/combined_legal_training.jsonl" ]; then
    echo "✅ Датасет уже существует"
    cat datasets/combined_legal_training_stats.json
else
    echo "🔧 Создание объединенного датасета..."
    python finetune/prepare_combined_dataset.py
fi

# Проверяем успешность
if [ ! -f "datasets/combined_legal_training.jsonl" ]; then
    echo "❌ Не удалось создать датасет"
    exit 1
fi

echo ""
echo "✅ Датасет готов"
echo ""

# ===============================================================================
# ЭТАП 2: Установка PEFT (если нужно)
# ===============================================================================
echo "🔧 Проверка зависимостей..."
pip install peft bitsandbytes accelerate -q || {
    echo "⚠️  Установка PEFT..."
    pip install peft accelerate
}

echo "✅ Все зависимости установлены"
echo ""

# ===============================================================================
# ЭТАП 3: Файнтюнинг трех сфер
# ===============================================================================
echo "================================================================================"
echo "🔥 ЭТАП 2: Файнтюнинг трех сфер"
echo "================================================================================"
echo ""
echo "⏰ Начало: $(date '+%H:%M:%S')"
echo ""

START_TIME=$(date +%s)

# Сфера 047: СЛЕДОВАТЕЛЬ
echo "--------------------------------------------------------------------------------"
echo "⚖️  Сфера 047: СЛЕДОВАТЕЛЬ"
echo "--------------------------------------------------------------------------------"
SPHERE_START=$(date +%s)

python finetune/finetune_overnight_m4.py \
    --sphere 047 \
    --steps 800 \
    --batch-size 8

SPHERE_END=$(date +%s)
SPHERE_DURATION=$((SPHERE_END - SPHERE_START))
echo ""
echo "✅ Сфера 047 обучена за $(($SPHERE_DURATION / 60)) минут"
echo ""

# Сфера 048: ПРОКУРОР (КЛЮЧЕВАЯ!)
echo "--------------------------------------------------------------------------------"
echo "⚖️  Сфера 048: ПРОКУРОР (ключевая духовная миссия!)"
echo "--------------------------------------------------------------------------------"
SPHERE_START=$(date +%s)

python finetune/finetune_overnight_m4.py \
    --sphere 048 \
    --steps 800 \
    --batch-size 8

SPHERE_END=$(date +%s)
SPHERE_DURATION=$((SPHERE_END - SPHERE_START))
echo ""
echo "✅ Сфера 048 обучена за $(($SPHERE_DURATION / 60)) минут"
echo ""

# Сфера 049: СУДЬЯ
echo "--------------------------------------------------------------------------------"
echo "⚖️  Сфера 049: СУДЬЯ"
echo "--------------------------------------------------------------------------------"
SPHERE_START=$(date +%s)

python finetune/finetune_overnight_m4.py \
    --sphere 049 \
    --steps 800 \
    --batch-size 8

SPHERE_END=$(date +%s)
SPHERE_DURATION=$((SPHERE_END - SPHERE_START))
echo ""
echo "✅ Сфера 049 обучена за $(($SPHERE_DURATION / 60)) минут"
echo ""

# ===============================================================================
# ФИНАЛ
# ===============================================================================
END_TIME=$(date +%s)
TOTAL_DURATION=$((END_TIME - START_TIME))
HOURS=$((TOTAL_DURATION / 3600))
MINUTES=$(((TOTAL_DURATION % 3600) / 60))

echo "================================================================================"
echo "🎉 НОЧНОЕ ОБУЧЕНИЕ ЗАВЕРШЕНО!"
echo "================================================================================"
echo ""
echo "⏰ Окончание: $(date '+%H:%M:%S')"
echo "⏱️  Общее время: ${HOURS}ч ${MINUTES}мин"
echo ""
echo "✅ Обучены модели:"
echo "   📁 models/sphere_047_m4_overnight - СЛЕДОВАТЕЛЬ"
echo "   📁 models/sphere_048_m4_overnight - ПРОКУРОР"
echo "   📁 models/sphere_049_m4_overnight - СУДЬЯ"
echo ""
echo "📊 Следующие шаги:"
echo "   1. Тестирование моделей:"
echo "      python test_trained_spheres.py"
echo ""
echo "   2. Публикация на HuggingFace:"
echo "      python finetune/publish_to_huggingface.py --all"
echo ""
echo "   3. Публикация в Ollama:"
echo "      python finetune/publish_to_ollama.py --all"
echo ""
echo "⚖️  Истина восторжествовала! 🕉️  Харе Кришна!"
echo ""



