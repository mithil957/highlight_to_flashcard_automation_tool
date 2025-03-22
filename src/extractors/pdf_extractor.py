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
        section_start_pages_0idx = [page - 1 for page in section_start_pages]
        section_boundaries = section_start_pages_0idx
        
        for i in range(len(section_start_pages)):
            section_num = i + 1
            start_page = section_boundaries[i]
            end_page = section_boundaries[i + 1] - 1
            
            section_text = ""
            section_highlights = []
            
            for page_num in range(start_page, end_page + 1):
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