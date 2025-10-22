"""
Основная мультимодальная модель для Braindler & Mozgach

Архитектура:
    Vision Encoder (CLIP) → Projection → Language Model (Braindler/Mozgach)

© 2025 NativeMind - NativeMindNONC License
"""

import torch
import torch.nn as nn
from typing import Optional, Union, List
from PIL import Image
from transformers import AutoModelForCausalLM, AutoTokenizer
from .vision_encoder import VisionEncoder
from .projection import ProjectionLayer


class MultimodalBraindler(nn.Module):
    """
    Мультимодальная версия Braindler
    
    Поддерживает:
    - Текстовые запросы
    - Изображения
    - Комбинированные запросы (текст + изображение)
    """
    
    def __init__(
        self,
        language_model_name: str = "nativemind/braindler_final_model",
        vision_model_name: str = "openai/clip-vit-large-patch14",
        device: str = "auto",
    ):
        super().__init__()
        
        print("🚀 Инициализация MultimodalBraindler...")
        
        # Определяем устройство
        if device == "auto":
            if torch.cuda.is_available():
                self.device = "cuda"
            elif torch.backends.mps.is_available():
                self.device = "mps"
            else:
                self.device = "cpu"
        else:
            self.device = device
            
        print(f"   📱 Устройство: {self.device}")
        
        # Загружаем vision encoder
        print(f"   👁️  Загрузка Vision Encoder: {vision_model_name}")
        self.vision_encoder = VisionEncoder(vision_model_name)
        
        # Загружаем языковую модель
        print(f"   🧠 Загрузка Language Model: {language_model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(language_model_name)
        self.language_model = AutoModelForCausalLM.from_pretrained(
            language_model_name,
            torch_dtype=torch.float32 if self.device == "cpu" else torch.float16,
            device_map=self.device if self.device != "mps" else None,
        )
        
        if self.device == "mps":
            self.language_model = self.language_model.to("mps")
        
        # Проекционный слой: CLIP embedding → Language model embedding
        vision_dim = self.vision_encoder.get_embedding_dim()
        language_dim = self.language_model.config.hidden_size
        
        print(f"   🔗 Создание проекционного слоя: {vision_dim} → {language_dim}")
        self.projection = ProjectionLayer(vision_dim, language_dim)
        self.projection = self.projection.to(self.device)
        
        # Pad token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.language_model.config.pad_token_id = self.language_model.config.eos_token_id
        
        print("   ✅ MultimodalBraindler готов к работе!")
    
    def encode_image(self, image: Union[str, Image.Image]) -> torch.Tensor:
        """
        Кодирует изображение в эмбеддинг
        
        Args:
            image: Путь к изображению или PIL.Image
            
        Returns:
            Tensor эмбеддинга изображения
        """
        # Получаем CLIP эмбеддинг
        vision_embedding = self.vision_encoder.encode(image)
        vision_embedding = vision_embedding.to(self.device)
        
        # Проецируем в пространство языковой модели
        language_embedding = self.projection(vision_embedding)
        
        return language_embedding
    
    def chat(
        self,
        prompt: str,
        image: Optional[Union[str, Image.Image]] = None,
        max_length: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ) -> str:
        """
        Мультимодальный чат
        
        Args:
            prompt: Текстовый запрос
            image: Опциональное изображение
            max_length: Максимальная длина ответа
            temperature: Температура генерации
            top_p: Top-p sampling
            
        Returns:
            Сгенерированный ответ
        """
        # Формируем входные данные
        if image is not None:
            # Мультимодальный режим
            image_embedding = self.encode_image(image)
            
            # Создаем префикс для изображения
            image_prefix = "[ИЗОБРАЖЕНИЕ] "
            full_prompt = image_prefix + prompt
        else:
            # Только текст
            full_prompt = prompt
        
        # Токенизация
        inputs = self.tokenizer(
            full_prompt,
            return_tensors="pt",
            padding=True,
            truncation=True,
        )
        
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Генерация
        with torch.no_grad():
            outputs = self.language_model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
            )
        
        # Декодируем ответ
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Убираем исходный промпт из ответа
        if response.startswith(full_prompt):
            response = response[len(full_prompt):].strip()
        
        return response
    
    def batch_encode_images(self, images: List[Union[str, Image.Image]]) -> torch.Tensor:
        """
        Пакетное кодирование изображений
        
        Args:
            images: Список изображений
            
        Returns:
            Tensor эмбеддингов
        """
        embeddings = []
        
        for image in images:
            emb = self.encode_image(image)
            embeddings.append(emb)
        
        return torch.stack(embeddings)
    
    @classmethod
    def from_pretrained(cls, model_path: str, **kwargs):
        """
        Загрузка предобученной мультимодальной модели
        
        Args:
            model_path: Путь к модели
            **kwargs: Дополнительные параметры
            
        Returns:
            Экземпляр MultimodalBraindler
        """
        # TODO: Реализовать загрузку fine-tuned projection layer
        return cls(language_model_name=model_path, **kwargs)
    
    def save_pretrained(self, save_path: str):
        """
        Сохранение мультимодальной модели
        
        Args:
            save_path: Путь для сохранения
        """
        import os
        os.makedirs(save_path, exist_ok=True)
        
        # Сохраняем языковую модель
        self.language_model.save_pretrained(os.path.join(save_path, "language_model"))
        self.tokenizer.save_pretrained(os.path.join(save_path, "language_model"))
        
        # Сохраняем проекционный слой
        torch.save(
            self.projection.state_dict(),
            os.path.join(save_path, "projection.pt")
        )
        
        print(f"✅ Модель сохранена в {save_path}")


class MultimodalMozgach(MultimodalBraindler):
    """
    Мультимодальная версия Mozgach
    
    Расширяет MultimodalBraindler с дополнительными возможностями
    для универсального AI-ассистента
    """
    
    def __init__(
        self,
        language_model_name: str = "nativemind/mozgach_full_trained_model",
        vision_model_name: str = "openai/clip-vit-large-patch14",
        device: str = "auto",
    ):
        print("🚀 Инициализация MultimodalMozgach...")
        super().__init__(language_model_name, vision_model_name, device)
        print("   ✅ MultimodalMozgach готов к работе!")
    
    def analyze_code_screenshot(self, image: Union[str, Image.Image]) -> str:
        """
        Специализированная функция для анализа скриншотов кода
        
        Args:
            image: Скриншот кода
            
        Returns:
            Анализ кода
        """
        prompt = "Проанализируй код на этом изображении. Опиши, что он делает, и предложи улучшения."
        return self.chat(prompt, image=image)
    
    def analyze_diagram(self, image: Union[str, Image.Image]) -> str:
        """
        Анализ диаграмм и схем
        
        Args:
            image: Диаграмма или схема
            
        Returns:
            Описание диаграммы
        """
        prompt = "Опиши эту диаграмму или схему. Объясни её смысл и компоненты."
        return self.chat(prompt, image=image)



