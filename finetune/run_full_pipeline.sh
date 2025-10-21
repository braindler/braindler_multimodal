#!/bin/bash
#
# Полный pipeline файнтюнинга и публикации юридических моделей
#
# Шаги:
# 1. Подготовка датасета из 107 томов
# 2. Файнтюнинг 6 моделей (Braindler x3 + Mozgach x3)
# 3. Публикация на HuggingFace
# 4. Публикация в Ollama
#
# © 2025 NativeMind - NativeMindNONC License

set -e  # Остановка при ошибке

echo "================================================================================"
echo "⚖️  ПОЛНЫЙ PIPELINE: Файнтюнинг юридических моделей"
echo "================================================================================"
echo ""
echo "🙏 Духовная миссия: Служение истине через AI"
echo ""
echo "📋 Этапы:"
echo "   1. Подготовка датасета (107 томов)"
echo "   2. Файнтюнинг Braindler: Сферы 047, 048, 049"
echo "   3. Файнтюнинг Mozgach108: Сферы 047, 048, 049"
echo "   4. Публикация на HuggingFace"
echo "   5. Публикация в Ollama"
echo ""
read -p "Продолжить? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Отменено"
    exit 1
fi

# Активируем venv
cd "$(dirname "$0")/.."
source venv/bin/activate

# ===============================================================================
# ЭТАП 1: Подготовка датасета
# ===============================================================================
echo ""
echo "================================================================================"
echo "📚 ЭТАП 1/5: Подготовка датасета"
echo "================================================================================"
echo ""

if [ -f "datasets/legal_case_viktor/legal_dataset.jsonl" ]; then
    read -p "Датасет уже существует. Пересоздать? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python finetune/prepare_legal_dataset.py --pages 10
    fi
else
    python finetune/prepare_legal_dataset.py --pages 10
fi

# Проверяем, что датасет создан
if [ ! -f "datasets/legal_case_viktor/legal_dataset.jsonl" ]; then
    echo "❌ Датасет не создан!"
    exit 1
fi

echo "✅ Датасет готов"

# ===============================================================================
# ЭТАП 2: Файнтюнинг Braindler (Сферы 047, 048, 049)
# ===============================================================================
echo ""
echo "================================================================================"
echo "🔥 ЭТАП 2/5: Файнтюнинг Braindler (3 сферы)"
echo "================================================================================"
echo ""

BASE_MODEL_BRAINDLER="nativemind/braindler_final_model"

for SPHERE in 047 048 049; do
    echo ""
    echo "--------------------------------------------------------------------------------"
    echo "⚖️  Braindler Сфера $SPHERE"
    echo "--------------------------------------------------------------------------------"
    
    OUTPUT_DIR="models/sphere_${SPHERE}_braindler"
    
    if [ -d "$OUTPUT_DIR" ]; then
        echo "⚠️  Модель уже существует: $OUTPUT_DIR"
        read -p "Переобучить? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Пропускаем..."
            continue
        fi
    fi
    
    python finetune/finetune_sphere.py \
        --sphere "$SPHERE" \
        --base-model "$BASE_MODEL_BRAINDLER" \
        --dataset "datasets/legal_case_viktor/legal_dataset.jsonl" \
        --output "$OUTPUT_DIR" \
        --epochs 3 \
        --batch-size 2 \
        --learning-rate 2e-4
    
    if [ $? -eq 0 ]; then
        echo "✅ Braindler Сфера $SPHERE обучена"
    else
        echo "❌ Ошибка обучения Braindler Сфера $SPHERE"
        exit 1
    fi
done

# ===============================================================================
# ЭТАП 3: Файнтюнинг Mozgach108 (Сферы 047, 048, 049)
# ===============================================================================
echo ""
echo "================================================================================"
echo "🔥 ЭТАП 3/5: Файнтюнинг Mozgach108 (3 сферы)"
echo "================================================================================"
echo ""

BASE_MODEL_MOZGACH="nativemind/mozgach_full_trained_model"

for SPHERE in 047 048 049; do
    echo ""
    echo "--------------------------------------------------------------------------------"
    echo "⚖️  Mozgach108 Сфера $SPHERE"
    echo "--------------------------------------------------------------------------------"
    
    OUTPUT_DIR="models/sphere_${SPHERE}_mozgach"
    
    if [ -d "$OUTPUT_DIR" ]; then
        echo "⚠️  Модель уже существует: $OUTPUT_DIR"
        read -p "Переобучить? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Пропускаем..."
            continue
        fi
    fi
    
    python finetune/finetune_sphere.py \
        --sphere "$SPHERE" \
        --base-model "$BASE_MODEL_MOZGACH" \
        --dataset "datasets/legal_case_viktor/legal_dataset.jsonl" \
        --output "$OUTPUT_DIR" \
        --epochs 3 \
        --batch-size 2 \
        --learning-rate 2e-4
    
    if [ $? -eq 0 ]; then
        echo "✅ Mozgach108 Сфера $SPHERE обучена"
    else
        echo "❌ Ошибка обучения Mozgach108 Сфера $SPHERE"
        exit 1
    fi
done

# ===============================================================================
# ЭТАП 4: Публикация на HuggingFace
# ===============================================================================
echo ""
echo "================================================================================"
echo "📤 ЭТАП 4/5: Публикация на HuggingFace"
echo "================================================================================"
echo ""

read -p "Опубликовать на HuggingFace? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python finetune/publish_to_huggingface.py --all --base-dir models
    
    if [ $? -eq 0 ]; then
        echo "✅ Модели опубликованы на HuggingFace"
    else
        echo "⚠️  Ошибка публикации на HuggingFace"
    fi
else
    echo "Пропускаем HuggingFace"
fi

# ===============================================================================
# ЭТАП 5: Публикация в Ollama
# ===============================================================================
echo ""
echo "================================================================================"
echo "📤 ЭТАП 5/5: Публикация в Ollama"
echo "================================================================================"
echo ""

read -p "Опубликовать в Ollama? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python finetune/publish_to_ollama.py --all --base-dir models
    
    if [ $? -eq 0 ]; then
        echo "✅ Модели опубликованы в Ollama"
    else
        echo "⚠️  Ошибка публикации в Ollama"
    fi
else
    echo "Пропускаем Ollama"
fi

# ===============================================================================
# ФИНАЛ
# ===============================================================================
echo ""
echo "================================================================================"
echo "🎉 PIPELINE ЗАВЕРШЕН!"
echo "================================================================================"
echo ""
echo "📊 Результаты:"
echo ""
echo "Braindler Мультимодальный:"
echo "  ✅ Сфера 047 (СЛЕДОВАТЕЛЬ)"
echo "  ✅ Сфера 048 (ПРОКУРОР)"
echo "  ✅ Сфера 049 (СУДЬЯ)"
echo ""
echo "Mozgach108 Мультимодальный:"
echo "  ✅ Сфера 047 (СЛЕДОВАТЕЛЬ)"
echo "  ✅ Сфера 048 (ПРОКУРОР)"
echo "  ✅ Сфера 049 (СУДЬЯ)"
echo ""
echo "📦 Всего моделей: 6"
echo ""
echo "🔗 HuggingFace:"
echo "   https://huggingface.co/nativemind/braindler-multimodal-sphere-047"
echo "   https://huggingface.co/nativemind/braindler-multimodal-sphere-048"
echo "   https://huggingface.co/nativemind/braindler-multimodal-sphere-049"
echo "   https://huggingface.co/nativemind/mozgach108-multimodal-sphere-047"
echo "   https://huggingface.co/nativemind/mozgach108-multimodal-sphere-048"
echo "   https://huggingface.co/nativemind/mozgach108-multimodal-sphere-049"
echo ""
echo "🤖 Ollama:"
echo "   ollama run braindler-sphere-047"
echo "   ollama run braindler-sphere-048"
echo "   ollama run braindler-sphere-049"
echo "   ollama run mozgach108-sphere-047"
echo "   ollama run mozgach108-sphere-048"
echo "   ollama run mozgach108-sphere-049"
echo ""
echo "⚖️  Истина восторжествовала! 🕉️  Харе Кришна!"
echo ""

