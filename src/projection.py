"""
Проекционный слой для мультимодальной модели

Преобразует эмбеддинги из vision encoder в пространство языковой модели

© 2025 NativeMind - NativeMindNONC License
"""

import torch
import torch.nn as nn


class ProjectionLayer(nn.Module):
    """
    MLP проекция из vision space → language space
    
    Архитектура:
        Linear(vision_dim → hidden_dim) → GELU → Linear(hidden_dim → language_dim)
    """
    
    def __init__(
        self,
        vision_dim: int,
        language_dim: int,
        hidden_dim: int = None,
        dropout: float = 0.1,
    ):
        """
        Инициализация проекционного слоя
        
        Args:
            vision_dim: Размерность vision эмбеддинга (CLIP: 768/1024)
            language_dim: Размерность языковой модели
            hidden_dim: Размерность скрытого слоя (по умолчанию: среднее)
            dropout: Вероятность dropout
        """
        super().__init__()
        
        if hidden_dim is None:
            # Используем среднее между vision и language dimensions
            hidden_dim = (vision_dim + language_dim) // 2
        
        self.projection = nn.Sequential(
            # Первый слой
            nn.Linear(vision_dim, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            
            # Второй слой
            nn.Linear(hidden_dim, language_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            
            # Выходной слой
            nn.Linear(language_dim, language_dim),
        )
        
        # Layer normalization для стабильности
        self.layer_norm = nn.LayerNorm(language_dim)
        
        # Инициализация весов
        self._init_weights()
    
    def _init_weights(self):
        """Инициализация весов Xavier/Glorot"""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
    
    def forward(self, vision_embedding: torch.Tensor) -> torch.Tensor:
        """
        Прямой проход
        
        Args:
            vision_embedding: [batch_size, vision_dim] или [vision_dim]
            
        Returns:
            language_embedding: [batch_size, language_dim] или [language_dim]
        """
        # Добавляем batch dimension если нужно
        squeeze = False
        if vision_embedding.dim() == 1:
            vision_embedding = vision_embedding.unsqueeze(0)
            squeeze = True
        
        # Проекция
        projected = self.projection(vision_embedding)
        
        # Layer norm для стабильности
        output = self.layer_norm(projected)
        
        # Убираем batch dimension если добавляли
        if squeeze:
            output = output.squeeze(0)
        
        return output


class AdaptiveProjectionLayer(ProjectionLayer):
    """
    Адаптивный проекционный слой с attention механизмом
    
    Более продвинутая версия для будущего fine-tuning
    """
    
    def __init__(
        self,
        vision_dim: int,
        language_dim: int,
        num_heads: int = 8,
        hidden_dim: int = None,
        dropout: float = 0.1,
    ):
        super().__init__(vision_dim, language_dim, hidden_dim, dropout)
        
        # Multi-head attention для адаптивной проекции
        self.attention = nn.MultiheadAttention(
            embed_dim=language_dim,
            num_heads=num_heads,
            dropout=dropout,
            batch_first=True,
        )
        
        # Feedforward network
        self.ffn = nn.Sequential(
            nn.Linear(language_dim, hidden_dim or language_dim * 4),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim or language_dim * 4, language_dim),
        )
        
        # Layer norms
        self.norm1 = nn.LayerNorm(language_dim)
        self.norm2 = nn.LayerNorm(language_dim)
    
    def forward(self, vision_embedding: torch.Tensor) -> torch.Tensor:
        """
        Прямой проход с attention
        
        Args:
            vision_embedding: [batch_size, vision_dim]
            
        Returns:
            language_embedding: [batch_size, language_dim]
        """
        # Базовая проекция
        x = super().forward(vision_embedding)
        
        # Добавляем sequence dimension для attention
        if x.dim() == 2:
            x = x.unsqueeze(1)  # [batch, 1, dim]
        
        # Self-attention
        attn_out, _ = self.attention(x, x, x)
        x = self.norm1(x + attn_out)
        
        # Feedforward
        ffn_out = self.ffn(x)
        x = self.norm2(x + ffn_out)
        
        # Убираем sequence dimension
        if x.size(1) == 1:
            x = x.squeeze(1)
        
        return x



