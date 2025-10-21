"""
Юридический анализатор документов

Духовная миссия: Служение истине и справедливости
Ключевая функция: Обнаружение копипаста как симптома несправедливости

В соответствии с ПРАВИЛО из проекта "Сделай, Старец!"

© 2025 NativeMind - NativeMindNONC License
"""

import os
import difflib
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from Levenshtein import ratio as levenshtein_ratio
from fuzzywuzzy import fuzz
from .ocr_engine import OCREngine


@dataclass
class CopyPasteResult:
    """Результат обнаружения копипаста"""
    text_similarity: float  # Процент текстового совпадения (0-100)
    visual_similarity: float  # Визуальное сходство (0-100)
    suspicious_blocks: List[Tuple[str, str]]  # [(блок_прокурора, блок_следователя)]
    identical_sections: List[str]  # Полностью идентичные секции
    suspicious_patterns: List[str]  # Подозрительные паттерны
    spiritual_verdict: str  # Вердикт с духовной точки зрения


@dataclass
class LegalCase:
    """Уголовное дело"""
    case_name: str
    prosecutor_documents: Dict[str, Dict[int, str]]  # {filename: {page: text}}
    investigator_documents: Dict[str, Dict[int, str]]
    metadata: Dict[str, any]  # Метаданные (даты, подписи и т.д.)


class LegalDocumentAnalyzer:
    """
    Анализатор юридических документов
    
    Духовная цель:
        "Нам важно понять истину и действительно разобраться, 
         то есть с духовной точки зрения."
    
    Ключевая функция:
        Обнаружение копипаста между документами прокурора и следователя
        как симптома возможной несправедливости
    """
    
    def __init__(self, use_easyocr: bool = False):
        """
        Инициализация юридического анализатора
        
        Args:
            use_easyocr: Использовать EasyOCR для лучшего распознавания
        """
        print("⚖️  Инициализация LegalDocumentAnalyzer...")
        print("   🙏 Духовная миссия: Служение истине и справедливости")
        
        # OCR движок
        self.ocr = OCREngine(languages=['rus', 'eng'], use_easyocr=use_easyocr)
        
        # Пороги для определения подозрительных совпадений
        self.SUSPICIOUS_THRESHOLD = 70.0  # % сходства
        self.IDENTICAL_THRESHOLD = 95.0   # % для идентичных блоков
        
        print("   ✅ Анализатор готов к служению истине")
    
    def process_case(
        self,
        prosecutor_docs: List[str],
        investigator_docs: List[str],
        case_name: str = "Уголовное дело",
    ) -> LegalCase:
        """
        Обрабатывает все документы дела
        
        Args:
            prosecutor_docs: Список PDF документов прокурора
            investigator_docs: Список PDF документов следователя
            case_name: Название дела
            
        Returns:
            LegalCase с извлеченными данными
        """
        print(f"\n📚 Обработка дела: {case_name}")
        print(f"   Документы прокурора: {len(prosecutor_docs)}")
        print(f"   Документы следователя: {len(investigator_docs)}")
        
        # Обрабатываем документы прокурора
        print("\n📄 Обработка документов прокурора...")
        prosecutor_data = self.ocr.batch_process_pdfs(prosecutor_docs)
        
        # Обрабатываем документы следователя
        print("\n📄 Обработка документов следователя...")
        investigator_data = self.ocr.batch_process_pdfs(investigator_docs)
        
        # Создаем объект дела
        case = LegalCase(
            case_name=case_name,
            prosecutor_documents=prosecutor_data,
            investigator_documents=investigator_data,
            metadata={
                'prosecutor_files': prosecutor_docs,
                'investigator_files': investigator_docs,
            }
        )
        
        print(f"\n✅ Дело обработано")
        return case
    
    def detect_copypaste(
        self,
        case: LegalCase,
        block_size: int = 500,  # Размер блока для сравнения (символов)
    ) -> CopyPasteResult:
        """
        Обнаруживает копипаст между документами
        
        Духовная миссия:
            "Копирование документов - это не просто лень, это симптом более 
             глубокой проблемы: отсутствия независимой проверки, формального 
             подхода к судьбам людей, возможной коррупции."
        
        Args:
            case: Уголовное дело
            block_size: Размер блока текста для анализа
            
        Returns:
            CopyPasteResult с результатами анализа
        """
        print(f"\n🔍 Анализ копипаста: {case.case_name}")
        print("   🙏 Служение истине через обнаружение несправедливости...")
        
        # Объединяем все тексты
        prosecutor_text = self._merge_all_texts(case.prosecutor_documents)
        investigator_text = self._merge_all_texts(case.investigator_documents)
        
        # 1. Общее текстовое сходство
        text_similarity = self._calculate_text_similarity(
            prosecutor_text,
            investigator_text
        )
        
        print(f"   📊 Общее текстовое сходство: {text_similarity:.2f}%")
        
        # 2. Поиск идентичных блоков
        identical_sections = self._find_identical_sections(
            prosecutor_text,
            investigator_text,
            block_size
        )
        
        print(f"   🔴 Обнаружено идентичных блоков: {len(identical_sections)}")
        
        # 3. Поиск подозрительных блоков (частично скопированных)
        suspicious_blocks = self._find_suspicious_blocks(
            prosecutor_text,
            investigator_text,
            block_size
        )
        
        print(f"   ⚠️  Подозрительных блоков: {len(suspicious_blocks)}")
        
        # 4. Анализ подозрительных паттернов
        suspicious_patterns = self._analyze_patterns(
            prosecutor_text,
            investigator_text
        )
        
        # 5. Духовный вердикт
        spiritual_verdict = self._make_spiritual_verdict(
            text_similarity,
            len(identical_sections),
            len(suspicious_blocks),
            suspicious_patterns
        )
        
        print(f"\n⚖️  Духовный вердикт: {spiritual_verdict}")
        
        return CopyPasteResult(
            text_similarity=text_similarity,
            visual_similarity=0.0,  # TODO: визуальное сравнение
            suspicious_blocks=suspicious_blocks,
            identical_sections=identical_sections,
            suspicious_patterns=suspicious_patterns,
            spiritual_verdict=spiritual_verdict,
        )
    
    def _merge_all_texts(self, documents: Dict[str, Dict[int, str]]) -> str:
        """Объединяет все тексты из документов"""
        all_texts = []
        
        for filename, pages in documents.items():
            for page_num in sorted(pages.keys()):
                all_texts.append(pages[page_num])
        
        return '\n\n'.join(all_texts)
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """
        Вычисляет общее сходство текстов
        
        Использует комбинацию алгоритмов:
        - SequenceMatcher (структурное сходство)
        - Levenshtein (посимвольное сходство)
        - FuzzyWuzzy (нечеткое сравнение)
        """
        # 1. SequenceMatcher
        seq_ratio = difflib.SequenceMatcher(None, text1, text2).ratio()
        
        # 2. Levenshtein (для коротких текстов)
        if len(text1) < 10000 and len(text2) < 10000:
            lev_ratio = levenshtein_ratio(text1, text2)
        else:
            lev_ratio = seq_ratio  # Fallback для длинных текстов
        
        # 3. FuzzyWuzzy (token-based)
        fuzzy_ratio = fuzz.token_sort_ratio(text1, text2) / 100.0
        
        # Среднее взвешенное
        similarity = (seq_ratio * 0.4 + lev_ratio * 0.3 + fuzzy_ratio * 0.3) * 100
        
        return similarity
    
    def _find_identical_sections(
        self,
        text1: str,
        text2: str,
        block_size: int
    ) -> List[str]:
        """Находит полностью идентичные блоки текста"""
        identical = []
        
        # Разбиваем на блоки
        blocks1 = self._split_into_blocks(text1, block_size)
        blocks2 = self._split_into_blocks(text2, block_size)
        
        # Сравниваем
        for block1 in blocks1:
            for block2 in blocks2:
                similarity = fuzz.ratio(block1, block2)
                
                if similarity >= self.IDENTICAL_THRESHOLD:
                    if block1 not in identical:
                        identical.append(block1)
        
        return identical
    
    def _find_suspicious_blocks(
        self,
        text1: str,
        text2: str,
        block_size: int
    ) -> List[Tuple[str, str]]:
        """Находит подозрительно похожие блоки"""
        suspicious = []
        
        blocks1 = self._split_into_blocks(text1, block_size)
        blocks2 = self._split_into_blocks(text2, block_size)
        
        for block1 in blocks1:
            for block2 in blocks2:
                similarity = fuzz.ratio(block1, block2)
                
                if self.SUSPICIOUS_THRESHOLD <= similarity < self.IDENTICAL_THRESHOLD:
                    suspicious.append((block1, block2))
        
        return suspicious
    
    def _split_into_blocks(self, text: str, block_size: int) -> List[str]:
        """Разбивает текст на блоки"""
        # Разбиваем по параграфам
        paragraphs = text.split('\n\n')
        
        blocks = []
        current_block = ""
        
        for para in paragraphs:
            if len(current_block) + len(para) < block_size:
                current_block += para + '\n\n'
            else:
                if current_block.strip():
                    blocks.append(current_block.strip())
                current_block = para + '\n\n'
        
        if current_block.strip():
            blocks.append(current_block.strip())
        
        return blocks
    
    def _analyze_patterns(self, text1: str, text2: str) -> List[str]:
        """Анализирует подозрительные паттерны"""
        patterns = []
        
        # Одинаковые опечатки/ошибки
        # TODO: реализовать анализ опечаток
        
        # Одинаковые формулировки
        common_phrases = self._find_common_phrases(text1, text2)
        if len(common_phrases) > 50:
            patterns.append(
                f"Обнаружено {len(common_phrases)} повторяющихся формулировок"
            )
        
        # Одинаковая структура
        if self._similar_structure(text1, text2):
            patterns.append("Идентичная структура документов")
        
        return patterns
    
    def _find_common_phrases(self, text1: str, text2: str, min_length: int = 30) -> List[str]:
        """Находит общие фразы"""
        # Простая реализация через SequenceMatcher
        matcher = difflib.SequenceMatcher(None, text1, text2)
        matches = matcher.get_matching_blocks()
        
        common = []
        for match in matches:
            if match.size >= min_length:
                phrase = text1[match.a:match.a + match.size]
                common.append(phrase)
        
        return common
    
    def _similar_structure(self, text1: str, text2: str) -> bool:
        """Проверяет похожесть структуры документов"""
        # Упрощенная проверка через количество параграфов
        para1 = len(text1.split('\n\n'))
        para2 = len(text2.split('\n\n'))
        
        if para1 == 0 or para2 == 0:
            return False
        
        ratio = min(para1, para2) / max(para1, para2)
        return ratio > 0.9
    
    def _make_spiritual_verdict(
        self,
        similarity: float,
        identical_count: int,
        suspicious_count: int,
        patterns: List[str],
    ) -> str:
        """
        Формирует вердикт с духовной точки зрения
        
        "Нам важно понять истину и действительно разобраться"
        """
        if similarity >= 80.0:
            verdict = (
                "🔴 КРИТИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ: Обнаружен массовый копипаст! "
                "Это знак к тому, что дело возможно купленное и нужен "
                "усиленный контроль. Прокурор не выполнил свою священную "
                "обязанность независимой проверки."
            )
        elif similarity >= 60.0:
            verdict = (
                "⚠️  СЕРЬЕЗНОЕ ПОДОЗРЕНИЕ: Высокий уровень совпадений указывает "
                "на формальный подход. Требуется тщательная проверка на предмет "
                "отсутствия независимого анализа."
            )
        elif similarity >= 40.0:
            verdict = (
                "⚡ УМЕРЕННОЕ ПОДОЗРЕНИЕ: Обнаружены совпадения, которые могут "
                "быть объяснены стандартными юридическими формулировками, но "
                "требуют внимания."
            )
        else:
            verdict = (
                "✅ НЕЗАВИСИМАЯ ПРОВЕРКА: Документы существенно различаются, "
                "что указывает на независимую работу прокурора и следователя. "
                "Истина восторжествует."
            )
        
        # Добавляем детали
        if identical_count > 0:
            verdict += f"\n\nОбнаружено {identical_count} полностью идентичных блоков."
        
        if suspicious_count > 0:
            verdict += f"\nОбнаружено {suspicious_count} подозрительно похожих блоков."
        
        if patterns:
            verdict += f"\n\nПодозрительные паттерны:\n" + '\n'.join(f"• {p}" for p in patterns)
        
        return verdict

