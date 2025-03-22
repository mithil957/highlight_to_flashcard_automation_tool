import streamlit as st
from extractors.pdf_extractor import PDFExtractor
from baml_utils.baml_utils import generate_flashcards, format_for_obsidian
import json

def main():
    # Set up page config
    st.set_page_config(page_title="Highlight to Flashcard", layout="wide")
    
    # Initialize session state for multi-step process
    if 'step' not in st.session_state:
        st.session_state.step = 1
        
    if 'pdf_data' not in st.session_state:
        st.session_state.pdf_data = None
        
    if 'extracted_data' not in st.session_state:
        st.session_state.extracted_data = None
        
    if 'flashcards' not in st.session_state:
        st.session_state.flashcards = None
        
    # Display header
    st.title("Highlight to Flashcard Converter")
    
    # Multi-step process using steps in sidebar
    st.sidebar.title("Steps")
    steps = [
        "1. Upload PDF",
        "2. Extract Highlights",
        "3. Generate Flashcards",
        "4. Edit Flashcards",
        "5. Export"
    ]
    
    for i, step in enumerate(steps, 1):
        if i < st.session_state.step:
            st.sidebar.success(step)
        elif i == st.session_state.step:
            st.sidebar.info(step)
        else:
            st.sidebar.text(step)
    
    # Step 1: Upload PDF
    if st.session_state.step == 1:
        st.header("Upload PDF")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        if uploaded_file is not None:
            # Initialize PDF extractor
            extractor = PDFExtractor()
            if extractor.load_pdf(uploaded_file):
                # Store PDF data in session state
                st.session_state.pdf_data = {
                    'filename': uploaded_file.name,
                    'extractor': extractor,
                    'page_count': extractor.get_page_count()
                }
                
                st.success(f"PDF loaded successfully: {uploaded_file.name} ({extractor.get_page_count()} pages)")
                
                if st.button("Next: Extract Highlights"):
                    st.session_state.step = 2
                    st.experimental_rerun()
            else:
                st.error("Error loading PDF. Please try a different file.")
    
    # Step 2: Extract Highlights
    elif st.session_state.step == 2:
        st.header("Extract Highlights")
        
        if not st.session_state.pdf_data:
            st.error("No PDF loaded. Please go back and upload a PDF.")
            if st.button("Back to Upload"):
                st.session_state.step = 1
                st.experimental_rerun()
        else:
            extractor = st.session_state.pdf_data['extractor']
            page_count = st.session_state.pdf_data['page_count']
            
            st.subheader(f"PDF: {st.session_state.pdf_data['filename']} ({page_count} pages)")
            
            st.write("Enter the starting page numbers for each section/chapter (comma-separated):")
            section_input = st.text_input("Page numbers", "1")
            
            if st.button("Extract Highlights"):
                try:
                    # Parse input page numbers
                    section_pages = [int(p.strip()) for p in section_input.split(",")]
                    
                    # Validate page numbers
                    if any(p < 1 or p > page_count for p in section_pages):
                        st.error(f"Page numbers must be between 1 and {page_count}")
                    else:
                        # Extract data
                        with st.spinner("Extracting highlights..."):
                            extracted_data = extractor.extract_by_sections(section_pages)
                            st.session_state.extracted_data = extracted_data
                        
                        # Display summary
                        st.success("Extraction complete!")
                        for section, data in extracted_data.items():
                            highlight_count = len(data['highlights'])
                            st.write(f"{section}: {highlight_count} highlights")
                        
                        # Allow proceeding to next step if highlights found
                        any_highlights = any(len(data['highlights']) > 0 for data in extracted_data.values())
                        if any_highlights:
                            if st.button("Next: Generate Flashcards"):
                                st.session_state.step = 3
                                st.experimental_rerun()
                        else:
                            st.warning("No highlights found in the PDF. Please try a different file or check if highlights are properly marked.")
                except ValueError:
                    st.error("Invalid page numbers. Please enter comma-separated numbers.")
            
            if st.button("Back to Upload"):
                st.session_state.step = 1
                st.experimental_rerun()
    
    # Step 3: Generate Flashcards
    elif st.session_state.step == 3:
        st.header("Generate Flashcards")
        
        if not st.session_state.extracted_data:
            st.error("No data extracted. Please go back and extract highlights first.")
            if st.button("Back to Extraction"):
                st.session_state.step = 2
                st.experimental_rerun()
        else:
            # Display sections and let user select which to generate flashcards for
            st.subheader("Select sections to generate flashcards")
            
            selected_sections = []
            for section, data in st.session_state.extracted_data.items():
                highlight_count = len(data['highlights'])
                if highlight_count > 0:
                    if st.checkbox(f"{section} ({highlight_count} highlights)", value=True):
                        selected_sections.append(section)
            
            use_detailed = st.checkbox("Generate detailed flashcards (more card types)", value=True)
            
            if st.button("Generate Flashcards"):
                all_flashcards = {}
                
                with st.spinner("Generating flashcards..."):
                    for section in selected_sections:
                        section_data = st.session_state.extracted_data[section]
                        cards = generate_flashcards(section_data, use_detailed)
                        all_flashcards[section] = cards
                
                st.session_state.flashcards = all_flashcards
                
                # Display summary
                total_cards = sum(len(cards) for cards in all_flashcards.values())
                st.success(f"Generated {total_cards} flashcards!")
                
                if st.button("Next: Edit Flashcards"):
                    st.session_state.step = 4
                    st.experimental_rerun()
            
            if st.button("Back to Extraction"):
                st.session_state.step = 2
                st.experimental_rerun()
    
    # Step 4: Edit Flashcards
    elif st.session_state.step == 4:
        st.header("Edit Flashcards")
        
        if not st.session_state.flashcards:
            st.error("No flashcards generated. Please go back and generate flashcards first.")
            if st.button("Back to Generation"):
                st.session_state.step = 3
                st.experimental_rerun()
        else:
            st.write("Review and edit your flashcards:")
            
            # For MVP, we'll use a simple editing interface
            # In a more advanced version, you could use more interactive components
            
            edited_flashcards = {}
            
            for section, cards in st.session_state.flashcards.items():
                st.subheader(section)
                
                edited_cards = []
                for i, card in enumerate(cards):
                    st.write(f"Card {i+1}")
                    
                    include = st.checkbox(f"Include card {i+1}", value=True, key=f"{section}_{i}_include")
                    
                    if include:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write("Front:")
                            front = st.text_area(f"Front {i+1}", card['front'], key=f"{section}_{i}_front")
                        
                        with col2:
                            st.write("Back:")
                            back = st.text_area(f"Back {i+1}", card['back'], key=f"{section}_{i}_back")
                        
                        card_type = st.selectbox(
                            f"Type {i+1}", 
                            options=["BASIC_FACT", "EXPLANATION", "APPLICATION", "CONTEXT"],
                            index=["BASIC_FACT", "EXPLANATION", "APPLICATION", "CONTEXT"].index(card['type']),
                            key=f"{section}_{i}_type"
                        )
                        
                        edited_cards.append({
                            'type': card_type,
                            'front': front,
                            'back': back
                        })
                
                edited_flashcards[section] = edited_cards
                st.divider()
            
            # Save edits
            if st.button("Save Edits"):
                st.session_state.flashcards = edited_flashcards
                st.success("Edits saved!")
            
            if st.button("Next: Export"):
                st.session_state.step = 5
                st.experimental_rerun()
            
            if st.button("Back to Generation"):
                st.session_state.step = 3
                st.experimental_rerun()
    
    # Step 5: Export
    elif st.session_state.step == 5:
        st.header("Export Flashcards")
        
        if not st.session_state.flashcards:
            st.error("No flashcards to export. Please go back and generate flashcards first.")
            if st.button("Back to Edit"):
                st.session_state.step = 4
                st.experimental_rerun()
        else:
            # Flatten all cards for export
            all_cards = []
            for section, cards in st.session_state.flashcards.items():
                all_cards.extend(cards)
            
            # Export options
            export_format = st.selectbox(
                "Export format",
                options=["Obsidian (single-line)", "Obsidian (multi-line)"]
            )
            
            # Generate export content
            if export_format == "Obsidian (single-line)":
                export_content = format_for_obsidian(all_cards, "single-line")
            else:
                export_content = format_for_obsidian(all_cards, "multi-line")
            
            # Display preview
            st.subheader("Preview")
            st.text_area("Export preview", export_content, height=300)
            
            # Download button
            st.download_button(
                label="Download Flashcards",
                data=export_content,
                file_name="flashcards.md",
                mime="text/markdown"
            )
            
            if st.button("Back to Edit"):
                st.session_state.step = 4
                st.experimental_rerun()

if __name__ == "__main__":
    main()