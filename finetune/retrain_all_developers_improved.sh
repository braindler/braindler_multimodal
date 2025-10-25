#!/bin/bash
"""
Полное переобучение всех сфер разработки (073-078) с улучшенным датасетом
на основе nativemind/mozgach_alpaca_gift

© 2025 NativeMind - NativeMindNONC License
"""

set -e

echo "=================================================================================="
echo "🚀 ПОЛНОЕ ПЕРЕОБУЧЕНИЕ СФЕР РАЗРАБОТКИ С УЛУЧШЕННЫМ ДАТАСЕТОМ"
echo "=================================================================================="
echo ""
echo "📦 Базовая модель: nativemind/shridhar_8k_multimodal"
echo "📚 Улучшенный датасет: mozgach_alpaca_gift + специализация"
echo "🎯 Сферы: 073-078 (DEVELOPER, CODE_REVIEWER, ARCHITECT, DEVOPS, QA_TESTER, TECH_WRITER)"
echo ""

# Активация виртуального окружения
echo "🔧 Активация виртуального окружения..."
source ../venv/bin/activate
echo "✅ Окружение активировано"
echo ""

# Создание улучшенного датасета
echo "📚 Создание улучшенного датасета на основе mozgach_alpaca_gift..."
python create_high_quality_developers_from_mozgach.py

if [ $? -ne 0 ]; then
    echo "❌ Ошибка при создании датасета!"
    exit 1
fi

echo "✅ Улучшенный датасет создан"
echo ""

# Создание директории для улучшенных моделей
echo "📁 Создание директории для улучшенных моделей..."
mkdir -p ../models_improved
echo "✅ Директория создана"
echo ""

# Функция для переобучения одной сферы
retrain_sphere() {
    local sphere=$1
    local sphere_name=$2
    
    echo "=================================================================================="
    echo "🚀 ПЕРЕОБУЧЕНИЕ СФЕРЫ $sphere: $sphere_name"
    echo "=================================================================================="
    echo ""
    
    # Запуск улучшенного обучения
    python finetune_developers_improved.py \
        --sphere $sphere \
        --dataset ../datasets/developers_high_quality_from_mozgach.jsonl \
        --output ../models_improved \
        --base-model nativemind/shridhar_8k_multimodal \
        --epochs 5 \
        --batch-size 4 \
        --learning-rate 1e-4
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Сфера $sphere ($sphere_name) успешно переобучена!"
        echo ""
    else
        echo ""
        echo "❌ Ошибка при переобучении сферы $sphere ($sphere_name)"
        echo ""
        exit 1
    fi
}

# Переобучение всех сфер
echo "🚀 Начинаем переобучение всех сфер разработки..."
echo ""

# Сфера 073: DEVELOPER
retrain_sphere "073" "DEVELOPER"

# Сфера 074: CODE_REVIEWER
retrain_sphere "074" "CODE_REVIEWER"

# Сфера 075: ARCHITECT
retrain_sphere "075" "ARCHITECT"

# Сфера 076: DEVOPS
retrain_sphere "076" "DEVOPS"

# Сфера 077: QA_TESTER
retrain_sphere "077" "QA_TESTER"

# Сфера 078: TECH_WRITER
retrain_sphere "078" "TECH_WRITER"

echo "=================================================================================="
echo "🎉 ВСЕ СФЕРЫ РАЗРАБОТКИ УСПЕШНО ПЕРЕОБУЧЕНЫ!"
echo "=================================================================================="
echo ""
echo "📁 Улучшенные модели сохранены в: ../models_improved/"
echo "   - sphere_073_improved/"
echo "   - sphere_074_improved/"
echo "   - sphere_075_improved/"
echo "   - sphere_076_improved/"
echo "   - sphere_077_improved/"
echo "   - sphere_078_improved/"
echo ""
echo "🧪 Запуск тестирования улучшенных моделей..."
echo ""

# Тестирование улучшенных моделей
python test_developer_models.py --models-dir ../models_improved

echo ""
echo "🙏 Служение истине через обучение AI завершено!"
echo ""
