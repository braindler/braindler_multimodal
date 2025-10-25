#!/bin/bash
"""
Скрипт для обучения всех сфер разработки (073-078)
с базовой моделью shridhar_8k_multimodal

© 2025 NativeMind - NativeMindNONC License
"""

set -e

echo "=================================================================================="
echo "💻 ОБУЧЕНИЕ ВСЕХ СФЕР РАЗРАБОТКИ (073-078)"
echo "=================================================================================="
echo ""
echo "📦 Базовая модель: nativemind/shridhar_8k_multimodal"
echo "📚 Датасет: developers_108_perfect.jsonl"
echo "🎯 Сферы: 073-078 (DEVELOPER, CODE_REVIEWER, ARCHITECT, DEVOPS, QA_TESTER, TECH_WRITER)"
echo ""

# Активация виртуального окружения
echo "🔧 Активация виртуального окружения..."
source ../venv/bin/activate
echo "✅ Окружение активировано"
echo ""

# Создание директории для моделей
echo "📁 Создание директории для моделей..."
mkdir -p ../models
echo "✅ Директория создана"
echo ""

# Функция для обучения одной сферы
train_sphere() {
    local sphere=$1
    local sphere_name=$2
    
    echo "=================================================================================="
    echo "💻 ОБУЧЕНИЕ СФЕРЫ $sphere: $sphere_name"
    echo "=================================================================================="
    echo ""
    
    # Запуск обучения
    python finetune_developers_spheres.py \
        --sphere $sphere \
        --dataset ../datasets/developers_108_perfect.jsonl \
        --output ../models \
        --base-model nativemind/shridhar_8k_multimodal \
        --epochs 3 \
        --batch-size 2 \
        --learning-rate 2e-4
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Сфера $sphere ($sphere_name) успешно обучена!"
        echo ""
    else
        echo ""
        echo "❌ Ошибка при обучении сферы $sphere ($sphere_name)"
        echo ""
        exit 1
    fi
}

# Обучение всех сфер
echo "🚀 Начинаем обучение всех сфер разработки..."
echo ""

# Сфера 073: DEVELOPER
train_sphere "073" "DEVELOPER"

# Сфера 074: CODE_REVIEWER
train_sphere "074" "CODE_REVIEWER"

# Сфера 075: ARCHITECT
train_sphere "075" "ARCHITECT"

# Сфера 076: DEVOPS
train_sphere "076" "DEVOPS"

# Сфера 077: QA_TESTER
train_sphere "077" "QA_TESTER"

# Сфера 078: TECH_WRITER
train_sphere "078" "TECH_WRITER"

echo "=================================================================================="
echo "🎉 ВСЕ СФЕРЫ РАЗРАБОТКИ УСПЕШНО ОБУЧЕНЫ!"
echo "=================================================================================="
echo ""
echo "📁 Модели сохранены в: ../models/"
echo "   - sphere_073_shridhar/"
echo "   - sphere_074_shridhar/"
echo "   - sphere_075_shridhar/"
echo "   - sphere_076_shridhar/"
echo "   - sphere_077_shridhar/"
echo "   - sphere_078_shridhar/"
echo ""
echo "🙏 Служение истине через обучение AI завершено!"
echo ""
