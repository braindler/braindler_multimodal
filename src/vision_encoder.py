"""
Vision Encoder на базе CLIP

Кодирует изображения в векторные представления для мультимодальной модели

© 2025 NativeMind - NativeMindNONC License
"""

import torch
from typing import Union
from PIL import Image
from transformers import CLIPVisionModel, CLIPImageProcessor


class VisionEncoder:
    """
    Vision Encoder на основе CLIP
    
    Преобразует изображения в векторные эмбеддинги
    """
    
    def __init__(self, model_name: str = "openai/clip-vit-large-patch14"):
        """
        Инициализация Vision Encoder
        
        Args:
            model_name: Название CLIP модели из HuggingFace
        """
        print(f"   📥 Загрузка CLIP vision model: {model_name}")
        
        self.model = CLIPVisionModel.from_pretrained(model_name)
        self.processor = CLIPImageProcessor.from_pretrained(model_name)
        
        # Переводим модель в eval режим
        self.model.eval()
        
        # Определяем размерность эмбеддинга
        self.embedding_dim = self.model.config.hidden_size
        
        print(f"   ✅ CLIP загружен, размерность эмбеддинга: {self.embedding_dim}")
    
    def get_embedding_dim(self) -> int:
        """Возвращает размерность эмбеддинга"""
        return self.embedding_dim
    
    def encode(self, image: Union[str, Image.Image]) -> torch.Tensor:
        """
        Кодирует изображение в эмбеддинг
        
        Args:
            image: Путь к изображению или PIL.Image
            
        Returns:
            Tensor эмбеддинга размерности [1, embedding_dim]
        """
        # Загружаем изображение, если это путь
        if isinstance(image, str):
            image = Image.open(image).convert("RGB")
        elif not isinstance(image, Image.Image):
            raise ValueError("image должен быть либо путём к файлу, либо PIL.Image")
        
        # Обрабатываем изображение
        inputs = self.processor(images=image, return_tensors="pt")
        
        # Получаем эмбеддинг
        with torch.no_grad():
            outputs = self.model(**inputs)
            # Используем pooler_output (CLS token)
            image_embedding = outputs.pooler_output
        
        return image_embedding
    
    def encode_batch(self, images: list) -> torch.Tensor:
        """
        Пакетное кодирование изображений
        
        Args:
            images: Список изображений (пути или PIL.Image)
            
        Returns:
            Tensor эмбеддингов размерности [batch_size, embedding_dim]
        """
        # Загружаем и конвертируем изображения
        pil_images = []
        for img in images:
            if isinstance(img, str):
                pil_images.append(Image.open(img).convert("RGB"))
            elif isinstance(img, Image.Image):
                pil_images.append(img)
            else:
                raise ValueError("Каждое изображение должно быть путём или PIL.Image")
        
        # Обрабатываем пакет
        inputs = self.processor(images=pil_images, return_tensors="pt")
        
        # Получаем эмбеддинги
        with torch.no_grad():
            outputs = self.model(**inputs)
            image_embeddings = outputs.pooler_output
        
        return image_embeddings
    
    def to(self, device: str):
        """Перемещает модель на устройство"""
        self.model = self.model.to(device)
        return self
    
    def __call__(self, image: Union[str, Image.Image]) -> torch.Tensor:
        """Позволяет использовать как функцию"""
        return self.encode(image)



