"""
OCR Engine для распознавания текста в документах

Особый фокус на юридические документы (сканы уголовных дел)
Служение истине через технологии

© 2025 NativeMind - NativeMindNONC License
"""

import os
from typing import Union, List, Dict, Optional
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import fitz  # PyMuPDF


class OCREngine:
    """
    OCR движок для распознавания текста
    
    Духовная миссия: 
        Извлечение истины из документов для служения справедливости
    """
    
    def __init__(
        self,
        languages: List[str] = None,
        dpi: int = 300,
        use_easyocr: bool = False,
    ):
        """
        Инициализация OCR Engine
        
        Args:
            languages: Список языков для распознавания (по умолчанию: ['rus', 'eng'])
            dpi: DPI для конвертации PDF в изображения
            use_easyocr: Использовать EasyOCR (нейросетевой, лучше для рукописного текста)
        """
        if languages is None:
            languages = ['rus', 'eng']  # Русский и английский по умолчанию
        
        self.languages = '+'.join(languages)
        self.dpi = dpi
        self.use_easyocr = use_easyocr
        
        if use_easyocr:
            try:
                import easyocr
                self.easyocr_reader = easyocr.Reader(languages)
                print("   ✅ EasyOCR инициализирован")
            except ImportError:
                print("   ⚠️  EasyOCR не установлен, используем Tesseract")
                self.use_easyocr = False
        
        print(f"   ✅ OCR Engine готов (языки: {', '.join(languages)})")
    
    def extract_text_from_image(
        self,
        image: Union[str, Image.Image],
        preserve_layout: bool = True,
    ) -> str:
        """
        Извлекает текст из изображения
        
        Args:
            image: Путь к изображению или PIL.Image
            preserve_layout: Сохранять ли структуру документа
            
        Returns:
            Распознанный текст
        """
        # Загружаем изображение
        if isinstance(image, str):
            img = Image.open(image)
        else:
            img = image
        
        # OCR
        if self.use_easyocr:
            # EasyOCR (нейросетевой)
            results = self.easyocr_reader.readtext(img)
            text = '\n'.join([result[1] for result in results])
        else:
            # Tesseract OCR
            if preserve_layout:
                # Сохраняем структуру документа
                text = pytesseract.image_to_string(
                    img,
                    lang=self.languages,
                    config='--psm 6'  # Assume uniform block of text
                )
            else:
                # Простое распознавание
                text = pytesseract.image_to_string(img, lang=self.languages)
        
        return text.strip()
    
    def extract_text_from_pdf(
        self,
        pdf_path: str,
        preserve_layout: bool = True,
        start_page: int = 0,
        end_page: Optional[int] = None,
    ) -> Dict[int, str]:
        """
        Извлекает текст из PDF (сканированного или текстового)
        
        Args:
            pdf_path: Путь к PDF файлу
            preserve_layout: Сохранять структуру документа
            start_page: Начальная страница (0-indexed)
            end_page: Конечная страница (None = до конца)
            
        Returns:
            Словарь {номер_страницы: текст}
        """
        results = {}
        
        # Сначала пробуем извлечь текст напрямую (если PDF текстовый)
        try:
            doc = fitz.open(pdf_path)
            has_text = False
            
            for page_num in range(len(doc)):
                if end_page is not None and page_num >= end_page:
                    break
                if page_num < start_page:
                    continue
                
                page = doc[page_num]
                text = page.get_text()
                
                if text.strip():
                    has_text = True
                    results[page_num] = text
            
            doc.close()
            
            if has_text:
                print(f"   ✅ Извлечен текст из PDF напрямую ({len(results)} страниц)")
                return results
        
        except Exception as e:
            print(f"   ⚠️  Не удалось извлечь текст напрямую: {e}")
        
        # Если не получилось, OCR для сканированного PDF
        print(f"   📄 Конвертация PDF в изображения (DPI: {self.dpi})...")
        
        images = convert_from_path(
            pdf_path,
            dpi=self.dpi,
            first_page=start_page + 1,  # convert_from_path uses 1-indexed
            last_page=end_page if end_page else None,
        )
        
        print(f"   🔍 OCR распознавание {len(images)} страниц...")
        
        for i, image in enumerate(images):
            page_num = start_page + i
            text = self.extract_text_from_image(image, preserve_layout)
            results[page_num] = text
            
            if (i + 1) % 10 == 0:
                print(f"      Обработано {i + 1}/{len(images)} страниц")
        
        print(f"   ✅ OCR завершен ({len(results)} страниц)")
        
        return results
    
    def extract_structured_data(
        self,
        image: Union[str, Image.Image]
    ) -> Dict[str, any]:
        """
        Извлекает структурированные данные из документа
        
        Returns:
            {
                'text': полный текст,
                'lines': список строк,
                'words': список слов,
                'confidence': уровень уверенности
            }
        """
        # Загружаем изображение
        if isinstance(image, str):
            img = Image.open(image)
        else:
            img = image
        
        # Получаем детальные данные OCR
        data = pytesseract.image_to_data(
            img,
            lang=self.languages,
            output_type=pytesseract.Output.DICT
        )
        
        # Фильтруем пустые блоки
        words = []
        confidences = []
        
        for i in range(len(data['text'])):
            if data['text'][i].strip():
                words.append({
                    'text': data['text'][i],
                    'confidence': data['conf'][i],
                    'bbox': (
                        data['left'][i],
                        data['top'][i],
                        data['width'][i],
                        data['height'][i]
                    )
                })
                confidences.append(data['conf'][i])
        
        # Полный текст
        full_text = ' '.join([w['text'] for w in words])
        
        # Средняя уверенность
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        return {
            'text': full_text,
            'words': words,
            'confidence': avg_confidence,
        }
    
    def batch_process_pdfs(
        self,
        pdf_paths: List[str],
        output_dir: Optional[str] = None,
    ) -> Dict[str, Dict[int, str]]:
        """
        Пакетная обработка нескольких PDF файлов
        
        Args:
            pdf_paths: Список путей к PDF
            output_dir: Директория для сохранения результатов (опционально)
            
        Returns:
            {pdf_name: {page_num: text}}
        """
        all_results = {}
        
        for pdf_path in pdf_paths:
            pdf_name = os.path.basename(pdf_path)
            print(f"\n📄 Обработка: {pdf_name}")
            
            try:
                results = self.extract_text_from_pdf(pdf_path)
                all_results[pdf_name] = results
                
                # Сохраняем результаты если указана директория
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)
                    output_file = os.path.join(
                        output_dir,
                        f"{pdf_name}_ocr.txt"
                    )
                    
                    with open(output_file, 'w', encoding='utf-8') as f:
                        for page_num in sorted(results.keys()):
                            f.write(f"\n{'='*60}\n")
                            f.write(f"Страница {page_num + 1}\n")
                            f.write(f"{'='*60}\n\n")
                            f.write(results[page_num])
                            f.write('\n')
                    
                    print(f"   💾 Результаты сохранены в {output_file}")
            
            except Exception as e:
                print(f"   ❌ Ошибка обработки {pdf_name}: {e}")
                all_results[pdf_name] = {}
        
        return all_results

