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
            
    def get_page_count(self) -> int:
        if self.doc:
            return self.doc.page_count
        return 0
    
    def extract_by_sections(self, section_start_pages: List[int]) -> Dict[str, Any]:
        if not self.doc:
            return {}
            
        results = {}
        
        # Convert 1-indexed page numbers to 0-indexed
        section_start_pages_0idx = [page - 1 for page in section_start_pages]
        
        # Add document end as the last boundary
        section_boundaries = section_start_pages_0idx + [self.doc.page_count]
        
        for i in range(len(section_start_pages)):
            section_num = i + 1
            start_page = section_boundaries[i]
            end_page = section_boundaries[i + 1] - 1  # Exclude the start of the next section
            
            section_text = ""
            section_highlights = []
            
            # Extract text and highlights for each page in the section
            for page_num in range(start_page, end_page + 1):
                page = self.doc[page_num]
                
                # Extract text
                section_text += page.get_text()
                
                # Extract highlights
                annots = page.annots()
                if annots:
                    for annot in annots:
                        if annot.type[0] == 8:  # Highlight annotation type
                            highlight_rect = annot.rect
                            highlight_text = page.get_textbox(highlight_rect)
                            if highlight_text.strip():  # Only add non-empty highlights
                                section_highlights.append({
                                    "text": highlight_text.strip(),
                                    "page": page_num + 1  # Convert back to 1-indexed
                                })
            
            results[f"Section {section_num}"] = {
                'text': section_text,
                'highlights': [h["text"] for h in section_highlights],
                'highlight_details': section_highlights
            }
        
        return results
    
    def close(self):
        if self.doc:
            self.doc.close()
            self.doc = None