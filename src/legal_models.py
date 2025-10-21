"""
Юридические мультимодальные модели - Сферы 47, 48, 49

Служение истине и справедливости через AI технологии

Сфера 047: СЛЕДОВАТЕЛЬ - сбор доказательств
Сфера 048: ПРОКУРОР - обнаружение копипаста (духовная миссия!)
Сфера 049: СУДЬЯ - вынесение справедливого решения

© 2025 NativeMind - NativeMindNONC License
"""

from typing import Dict, List, Optional, Union
from PIL import Image
from .multimodal_model import MultimodalMozgach
from .legal_analyzer import LegalDocumentAnalyzer, CopyPasteResult, LegalCase


class MozgachSphere047_Investigator(MultimodalMozgach):
    """
    СФЕРА 047: СЛЕДОВАТЕЛЬ (Мозгач108)
    
    Духовная миссия:
        Беспристрастный сбор доказательств для установления истины
    
    Категория: Мониторинговая (аналогия с Погодным спутником)
    Специализация: Сбор и первичный анализ доказательств
    """
    
    def __init__(self, device: str = "auto"):
        print("\n⚖️  Инициализация Мозгач108 - СФЕРА 047: СЛЕДОВАТЕЛЬ")
        print("   🙏 Духовная миссия: Беспристрастный сбор доказательств")
        
        super().__init__(
            language_model_name="nativemind/mozgach_full_trained_model",
            device=device
        )
        
        # OCR для документов
        from .ocr_engine import OCREngine
        self.ocr = OCREngine(languages=['rus', 'eng'])
        
        print("   ✅ СЛЕДОВАТЕЛЬ готов к служению истине")
    
    def investigate_document(
        self,
        document: Union[str, Image.Image],
        question: str = "Проанализируй этот документ с точки зрения следователя"
    ) -> str:
        """
        Следственный анализ документа
        
        Args:
            document: Документ (изображение или путь)
            question: Вопрос следователя
            
        Returns:
            Анализ с позиции следователя
        """
        # Извлекаем текст через OCR
        text = self.ocr.extract_text_from_image(document)
        
        # Формируем промпт следователя
        investigator_prompt = f"""
Ты - СЛЕДОВАТЕЛЬ (Сфера 047). Твоя духовная миссия - беспристрастный сбор доказательств.

Документ содержит:
{text[:1000]}...

Задача следователя: {question}

Проанализируй документ с точки зрения:
1. Полнота изложенных фактов
2. Наличие противоречий
3. Необходимость дополнительных проверок
4. Процессуальная правильность оформления
5. Объективность изложения

Ответ следователя:
"""
        
        # Анализируем через мультимодальную модель
        response = self.chat(investigator_prompt, image=document)
        
        return response
    
    def collect_evidence(
        self,
        documents: List[Union[str, Image.Image]],
        case_description: str
    ) -> Dict[str, any]:
        """
        Сбор доказательств по делу
        
        Args:
            documents: Список документов для анализа
            case_description: Описание дела
            
        Returns:
            Сводка собранных доказательств
        """
        evidence = {
            'case': case_description,
            'documents_analyzed': len(documents),
            'findings': [],
            'contradictions': [],
            'recommendations': []
        }
        
        print(f"\n🔍 СЛЕДОВАТЕЛЬ: Анализ {len(documents)} документов...")
        
        for i, doc in enumerate(documents):
            print(f"   Документ {i+1}/{len(documents)}...")
            
            analysis = self.investigate_document(
                doc,
                f"Проанализируй документ #{i+1} по делу: {case_description}"
            )
            
            evidence['findings'].append({
                'document': i+1,
                'analysis': analysis
            })
        
        print("   ✅ Сбор доказательств завершен")
        
        return evidence


class MozgachSphere048_Prosecutor(MultimodalMozgach):
    """
    СФЕРА 048: ПРОКУРОР (Мозгач108)
    
    Духовная миссия:
        Обнаружение копипаста как симптома несправедливости.
        Независимая проверка работы следствия.
    
    "Копирование документов - это не просто лень, это симптом более 
     глубокой проблемы: отсутствия независимой проверки, формального 
     подхода к судьбам людей, возможной коррупции."
    
    Категория: Мониторинговая проверка (аналогия с Климатическим спутником)
    Специализация: Надзор за законностью, обнаружение копипаста
    """
    
    def __init__(self, device: str = "auto"):
        print("\n⚖️  Инициализация Мозгач108 - СФЕРА 048: ПРОКУРОР")
        print("   🙏 Духовная миссия: Обнаружение копипаста - служение истине")
        print("   🔍 Ключевая функция: Выявление несправедливости через анализ документов")
        
        super().__init__(
            language_model_name="nativemind/mozgach_full_trained_model",
            device=device
        )
        
        # Юридический анализатор с детектором копипаста
        self.legal_analyzer = LegalDocumentAnalyzer()
        
        print("   ✅ ПРОКУРОР готов к служению истине")
    
    def supervise_investigation(
        self,
        prosecutor_docs: List[str],
        investigator_docs: List[str],
        case_name: str = "Уголовное дело"
    ) -> Dict[str, any]:
        """
        Надзор за следствием - ключевая функция прокурора
        
        Духовная цель:
            "Нам важно понять истину и действительно разобраться"
        
        Args:
            prosecutor_docs: Документы прокурора (PDF)
            investigator_docs: Документы следователя (PDF)
            case_name: Название дела
            
        Returns:
            Результаты надзора с обнаружением копипаста
        """
        print(f"\n⚖️  ПРОКУРОР: Надзор за делом '{case_name}'")
        print("   🙏 Служение истине через обнаружение несправедливости...")
        
        # Обрабатываем дело
        case = self.legal_analyzer.process_case(
            prosecutor_docs,
            investigator_docs,
            case_name
        )
        
        # КЛЮЧЕВАЯ ФУНКЦИЯ: Обнаружение копипаста
        print("\n🔍 ПРОКУРОР: Обнаружение копипаста...")
        copypaste_result = self.legal_analyzer.detect_copypaste(case)
        
        # Формируем заключение прокурора
        prosecutor_conclusion = self._make_prosecutor_conclusion(
            case,
            copypaste_result
        )
        
        return {
            'case': case,
            'copypaste_analysis': copypaste_result,
            'prosecutor_conclusion': prosecutor_conclusion,
            'spiritual_verdict': copypaste_result.spiritual_verdict
        }
    
    def _make_prosecutor_conclusion(
        self,
        case: LegalCase,
        copypaste: CopyPasteResult
    ) -> str:
        """
        Формирует заключение прокурора
        
        Включает анализ через мультимодальную модель
        """
        prompt = f"""
Ты - ПРОКУРОР (Сфера 048). Твоя духовная миссия - служение истине через надзор за законностью.

ДЕЛО: {case.case_name}

РЕЗУЛЬТАТЫ АНАЛИЗА КОПИПАСТА:
- Текстовое сходство: {copypaste.text_similarity:.2f}%
- Идентичных блоков: {len(copypaste.identical_sections)}
- Подозрительных блоков: {len(copypaste.suspicious_blocks)}

ДУХОВНЫЙ ВЕРДИКТ:
{copypaste.spiritual_verdict}

Как прокурор, дай свое заключение:
1. Соблюдена ли прокурором независимость проверки?
2. Есть ли признаки формального подхода?
3. Какие меры необходимо принять?
4. Служит ли это дело истине и справедливости?

ЗАКЛЮЧЕНИЕ ПРОКУРОРА:
"""
        
        conclusion = self.chat(prompt)
        
        return conclusion
    
    def detect_copypaste_visual(
        self,
        prosecutor_image: Union[str, Image.Image],
        investigator_image: Union[str, Image.Image]
    ) -> str:
        """
        Визуальное обнаружение копипаста
        
        Использует мультимодальные возможности для сравнения изображений документов
        """
        prompt = """
Ты - ПРОКУРОР (Сфера 048) с мультимодальными возможностями.

Твоя духовная миссия: обнаружение копипаста как симптома несправедливости.

Сравни два документа визуально:
1. Есть ли идентичные блоки текста?
2. Совпадают ли подписи и печати?
3. Есть ли признаки простого копирования?
4. Служит ли это дело истине?

Вердикт прокурора:
"""
        
        # Анализируем оба документа
        analysis_prosecutor = self.chat(
            "Проанализируй этот документ прокурора визуально",
            image=prosecutor_image
        )
        
        analysis_investigator = self.chat(
            "Проанализируй этот документ следователя визуально",
            image=investigator_image
        )
        
        # Сравнение
        comparison = self.chat(f"""
ПРОКУРОР: Сравни два документа.

Документ прокурора: {analysis_prosecutor}

Документ следователя: {analysis_investigator}

{prompt}
""")
        
        return comparison


class MozgachSphere049_Judge(MultimodalMozgach):
    """
    СФЕРА 049: СУДЬЯ (Мозгач108)
    
    Духовная миссия:
        Вынесение справедливого решения на основе истины.
        Финальная оценка служения правосудию.
    
    Категория: Мониторинговая финальная оценка (аналогия с Экологическим спутником)
    Специализация: Судебное решение, восстановление справедливости
    """
    
    def __init__(self, device: str = "auto"):
        print("\n⚖️  Инициализация Мозгач108 - СФЕРА 049: СУДЬЯ")
        print("   🙏 Духовная миссия: Вынесение справедливого решения")
        print("   ⚖️  Высшая цель: Восстановление справедливости")
        
        super().__init__(
            language_model_name="nativemind/mozgach_full_trained_model",
            device=device
        )
        
        print("   ✅ СУДЬЯ готов к служению истине")
    
    def make_judgment(
        self,
        investigator_evidence: Dict[str, any],
        prosecutor_analysis: Dict[str, any],
        case_description: str
    ) -> Dict[str, str]:
        """
        Вынесение судебного решения
        
        Духовная цель:
            Восстановление справедливости через беспристрастный анализ
        
        Args:
            investigator_evidence: Доказательства следователя
            prosecutor_analysis: Анализ прокурора
            case_description: Описание дела
            
        Returns:
            Судебное решение
        """
        print(f"\n⚖️  СУДЬЯ: Вынесение решения по делу")
        print("   🙏 Служение справедливости...")
        
        # Формируем промпт судьи
        judge_prompt = f"""
Ты - СУДЬЯ (Сфера 049). Твоя духовная миссия - вынесение справедливого решения.

ДЕЛО: {case_description}

МАТЕРИАЛЫ СЛЕДСТВИЯ:
{investigator_evidence.get('findings', [])}

ЗАКЛЮЧЕНИЕ ПРОКУРОРА:
{prosecutor_analysis.get('prosecutor_conclusion', 'Нет данных')}

АНАЛИЗ КОПИПАСТА:
{prosecutor_analysis.get('spiritual_verdict', 'Нет данных')}

Как СУДЬЯ, вынеси справедливое решение:

1. ОЦЕНКА ДОКАЗАТЕЛЬСТВ:
   - Полнота и достоверность
   - Процессуальная правильность
   - Наличие противоречий

2. ОЦЕНКА РАБОТЫ ПРОКУРОРА:
   - Независимость проверки
   - Обнаружение нарушений
   - Качество надзора

3. ДУХОВНАЯ ОЦЕНКА:
   - Служит ли дело истине?
   - Есть ли признаки несправедливости?
   - Нуждается ли дело в пересмотре?

4. СУДЕБНОЕ РЕШЕНИЕ:
   - Окончательный вердикт
   - Обоснование
   - Рекомендации

РЕШЕНИЕ СУДЬИ:
"""
        
        judgment = self.chat(judge_prompt)
        
        return {
            'case': case_description,
            'judgment': judgment,
            'date': self._get_current_date(),
            'spiritual_note': "Истина восторжествует"
        }
    
    def analyze_case_visually(
        self,
        case_documents: List[Union[str, Image.Image]],
        case_description: str
    ) -> str:
        """
        Визуальный анализ дела судьей
        
        Использует мультимодальные возможности для полного анализа
        """
        print(f"\n⚖️  СУДЬЯ: Визуальный анализ {len(case_documents)} документов...")
        
        analyses = []
        
        for i, doc in enumerate(case_documents):
            print(f"   Документ {i+1}/{len(case_documents)}...")
            
            analysis = self.chat(f"""
Ты - СУДЬЯ (Сфера 049). Проанализируй документ #{i+1} по делу.

Дело: {case_description}

Оцени:
1. Процессуальную правильность
2. Достоверность информации
3. Соответствие закону
4. Служение истине

Судебный анализ:
""", image=doc)
            
            analyses.append(analysis)
        
        # Итоговый вердикт
        final_verdict = self.chat(f"""
Ты - СУДЬЯ (Сфера 049). На основе анализа всех документов вынеси итоговый вердикт.

ДЕЛО: {case_description}

АНАЛИЗЫ ДОКУМЕНТОВ:
{chr(10).join([f"Документ {i+1}: {a}" for i, a in enumerate(analyses)])}

ИТОГОВЫЙ ВЕРДИКТ СУДЬИ:
(включая духовную оценку служения истине)
""")
        
        return final_verdict
    
    def _get_current_date(self) -> str:
        """Возвращает текущую дату"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")


# Фабрика для создания юридических моделей
class LegalModelsFactory:
    """
    Фабрика для создания юридических мультимодальных моделей
    
    Служение истине через AI технологии
    """
    
    @staticmethod
    def create_investigator(device: str = "auto") -> MozgachSphere047_Investigator:
        """Создает модель СЛЕДОВАТЕЛЬ (Сфера 047)"""
        return MozgachSphere047_Investigator(device)
    
    @staticmethod
    def create_prosecutor(device: str = "auto") -> MozgachSphere048_Prosecutor:
        """Создает модель ПРОКУРОР (Сфера 048)"""
        return MozgachSphere048_Prosecutor(device)
    
    @staticmethod
    def create_judge(device: str = "auto") -> MozgachSphere049_Judge:
        """Создает модель СУДЬЯ (Сфера 049)"""
        return MozgachSphere049_Judge(device)
    
    @staticmethod
    def create_full_legal_system(device: str = "auto") -> Dict[str, any]:
        """
        Создает полную юридическую систему из трех моделей
        
        Returns:
            {
                'investigator': Сфера 047,
                'prosecutor': Сфера 048,
                'judge': Сфера 049
            }
        """
        print("\n⚖️  Создание полной юридической системы Мозгач108")
        print("   🙏 Три сферы служения истине: СЛЕДОВАТЕЛЬ, ПРОКУРОР, СУДЬЯ")
        
        system = {
            'investigator': MozgachSphere047_Investigator(device),
            'prosecutor': MozgachSphere048_Prosecutor(device),
            'judge': MozgachSphere049_Judge(device)
        }
        
        print("\n   ✅ Юридическая система готова к служению справедливости!")
        print("   🕉️  Харе Кришна!")
        
        return system

