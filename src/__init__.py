"""
Мультимодальный Braindler & Mozgach

Базовая мультимодальная система для моделей Braindler и Mozgach
с поддержкой изображений, OCR и видео.

Юридические модели (Сферы 047-049) для служения истине:
- Сфера 047: СЛЕДОВАТЕЛЬ - сбор доказательств
- Сфера 048: ПРОКУРОР - обнаружение копипаста (духовная миссия!)
- Сфера 049: СУДЬЯ - вынесение справедливого решения

© 2025 NativeMind - NativeMindNONC License
"""

__version__ = "1.0.0"
__author__ = "NativeMind"

from .multimodal_model import MultimodalBraindler, MultimodalMozgach
from .vision_encoder import VisionEncoder
from .ocr_engine import OCREngine
from .legal_analyzer import LegalDocumentAnalyzer
from .legal_models import (
    MozgachSphere047_Investigator,
    MozgachSphere048_Prosecutor,
    MozgachSphere049_Judge,
    LegalModelsFactory
)

__all__ = [
    "MultimodalBraindler",
    "MultimodalMozgach",
    "VisionEncoder",
    "OCREngine",
    "LegalDocumentAnalyzer",
    # Юридические модели - Служение истине
    "MozgachSphere047_Investigator",
    "MozgachSphere048_Prosecutor",
    "MozgachSphere049_Judge",
    "LegalModelsFactory",
]

