import fitz  # PyMuPDF
from typing import List, Dict, Any, Optional, Tuple

class PDFExtractor:
    def __init__(self):
        self.doc = None
        self.filepath = None
        
    def load_pdf(self, pdf_file) -> bool:
        try:
            self.doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            return True
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return False
    
    def extract_by_sections(self, section_start_pages: List[int]) -> Dict[str, Any]:
        if not self.doc:
            return {}
            
        results = {}
        
        for idx, page_num in enumerate(section_start_pages):
            section_num = idx + 1
            start_page = 0 if idx == 0 else section_start_pages[idx-1]
            end_page = page_num + 1 if (idx == len(section_start_pages) - 1) else page_num
            
            section_text = ""
            section_highlights = []
            
            for page_num in range(start_page, end_page):
                page = self.doc[page_num]                
                section_text += page.get_text()
                annots = page.annots()

                if annots:
                    for annot in annots:
                        if annot.type[0] == 8:  # Highlight annotation type
                            highlight_rect = annot.rect
                            highlight_text = page.get_textbox(highlight_rect)
                            if len(highlight_text.strip()) != 0:
                                section_highlights.append(highlight_text.strip())

            results[f"Section {section_num}"] = {
                'text': section_text,
                'highlight_details': section_highlights
            }
        
        self.close()
        return results
    
    def close(self):
        if self.doc:
            self.doc.close()
            self.doc = None