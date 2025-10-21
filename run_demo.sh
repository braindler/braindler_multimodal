#!/bin/bash
# Быстрый запуск демонстрации мультимодального Braindler & Mozgach

echo "⚖️  Мультимодальный Braindler & Mozgach"
echo "🙏 Служение истине через AI технологии"
echo ""

# Активация виртуального окружения
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Виртуальное окружение активировано"
else
    echo "❌ Виртуальное окружение не найдено"
    echo "💡 Запустите: python3 -m venv venv"
    exit 1
fi

# Запуск демонстрации
echo ""
echo "🚀 Запуск quickstart демонстрации..."
echo ""
python demo_quickstart.py

echo ""
echo "✅ Демонстрация завершена!"
echo "🕉️  Харе Кришна!"
