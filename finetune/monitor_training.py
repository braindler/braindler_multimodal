#!/usr/bin/env python3
"""
Мониторинг прогресса переобучения сфер разработки

© 2025 NativeMind - NativeMindNONC License
"""

import os
import time
import subprocess
import json
from datetime import datetime

def check_training_progress():
    """Проверка прогресса обучения"""
    print("🔍 МОНИТОРИНГ ПЕРЕОБУЧЕНИЯ СФЕР РАЗРАБОТКИ")
    print("="*60)
    print(f"⏰ Время: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    # Проверка процессов обучения
    try:
        result = subprocess.run(
            ["ps", "aux"], 
            capture_output=True, 
            text=True
        )
        
        training_processes = []
        for line in result.stdout.split('\n'):
            if 'finetune_developers_improved.py' in line:
                training_processes.append(line)
        
        if training_processes:
            print("🚀 Активные процессы обучения:")
            for process in training_processes:
                parts = process.split()
                pid = parts[1]
                sphere = "Неизвестно"
                for part in parts:
                    if '--sphere' in part:
                        idx = parts.index(part)
                        if idx + 1 < len(parts):
                            sphere = parts[idx + 1]
                        break
                print(f"   📊 PID {pid}: Сфера {sphere}")
        else:
            print("❌ Нет активных процессов обучения")
        
        print()
        
    except Exception as e:
        print(f"❌ Ошибка проверки процессов: {e}")
    
    # Проверка директорий моделей
    models_dir = "../models_improved"
    if os.path.exists(models_dir):
        print("📁 Статус моделей:")
        spheres = ["073", "074", "075", "076", "077", "078"]
        
        for sphere in spheres:
            sphere_dir = f"{models_dir}/sphere_{sphere}_improved"
            if os.path.exists(sphere_dir):
                # Проверяем наличие файлов модели
                model_files = []
                for file in os.listdir(sphere_dir):
                    if file.endswith(('.bin', '.safetensors', '.json')):
                        model_files.append(file)
                
                if model_files:
                    status = "✅ ЗАВЕРШЕНА"
                    print(f"   Сфера {sphere}: {status} ({len(model_files)} файлов)")
                else:
                    status = "🔄 ОБУЧАЕТСЯ"
                    print(f"   Сфера {sphere}: {status}")
            else:
                status = "⏳ ОЖИДАНИЕ"
                print(f"   Сфера {sphere}: {status}")
        
        print()
        
        # Подсчет завершенных
        completed = 0
        for sphere in spheres:
            sphere_dir = f"{models_dir}/sphere_{sphere}_improved"
            if os.path.exists(sphere_dir):
                model_files = [f for f in os.listdir(sphere_dir) 
                             if f.endswith(('.bin', '.safetensors', '.json'))]
                if model_files:
                    completed += 1
        
        print(f"📊 Прогресс: {completed}/6 сфер завершено ({completed/6*100:.1f}%)")
        
    else:
        print("❌ Директория models_improved не найдена")
    
    print()

def main():
    """Основная функция мониторинга"""
    print("🔄 Запуск мониторинга...")
    print("Нажмите Ctrl+C для выхода")
    print()
    
    try:
        while True:
            check_training_progress()
            time.sleep(30)  # Проверка каждые 30 секунд
            
    except KeyboardInterrupt:
        print("\n👋 Мониторинг остановлен")

if __name__ == "__main__":
    main()
