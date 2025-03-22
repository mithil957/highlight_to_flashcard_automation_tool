import streamlit as st
import fitz
from extractors.pdf_extractor import PDFExtractor

def display_configure_sections():
    st.title("Step 2: Configure Sections")
    
    st.markdown("""
    Define the starting page numbers for each section in your PDF.
    
    For example, if you enter `25, 40, 70, 98, 134, 158`:
    - Section 1: Pages 1-25
    - Section 2: Pages 26-40
    - Section 3: Pages 41-70
    - And so on...
    
    The last number will be the last page processed.
    """)
    
    # Check if PDF path is in session state
    if 'pdf_path' not in st.session_state:
        st.error("No PDF uploaded. Please go back and upload a PDF first.")
        if st.button("Back to PDF Upload"):
            st.session_state.current_step = "upload_pdf"
        return
    
    # Get total page count to help user
    try:
        doc = fitz.open(st.session_state.pdf_path)
        total_pages = doc.page_count
        doc.close()
        st.info(f"Your PDF has {total_pages} pages in total.")
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        if st.button("Back to PDF Upload"):
            st.session_state.current_step = "upload_pdf"
        return
    
    # Input for section starting pages
    section_input = st.text_input(
        "Enter the starting page numbers for each section (comma-separated):",
        help="Enter page numbers where each section starts, separated by commas (e.g., 10, 25, 40, 60)"
    )
    
    # Initialize section_data in session state if not already there
    if 'section_data' not in st.session_state:
        st.session_state.section_data = None
    
    # Process button
    if st.button("Preview Sections", type="primary"):
        if not section_input.strip():
            st.warning("Please enter at least one page number.")
            return
        
        try:
            # Parse the input
            section_pages = [int(page.strip()) for page in section_input.split(',')]
            
            # Sort the pages
            section_pages.sort()
            
            # Validate pages are in range
            if section_pages[-1] > total_pages:
                st.warning(f"Last page number ({section_pages[-1]}) exceeds total pages in PDF ({total_pages}). Capping at {total_pages}.")
                section_pages = [p for p in section_pages if p <= total_pages]
            
            # Extract sections
            extractor = PDFExtractor()
            extractor.load_pdf(open(st.session_state.pdf_path, 'rb'))
            section_data = extractor.extract_by_sections(section_pages)
            
            # Store the data in session state
            st.session_state.section_data = section_data
            st.session_state.section_pages = section_pages
            
            st.success(f"Successfully processed {len(section_data)} sections!")
            
        except ValueError:
            st.error("Invalid input. Please enter numbers separated by commas.")
            return
        except Exception as e:
            st.error(f"Error processing sections: {e}")
            return
    
    # Display section previews if available
    if st.session_state.section_data:
        st.markdown("### Section Previews")
        
        # Convert to list for safe iteration while potentially removing items
        section_items = list(st.session_state.section_data.items())
        
        for section_name, section_content in section_items:
            with st.expander(f"{section_name}"):
                # Preview of text
                text_preview = section_content['text'][:100] + "..." if len(section_content['text']) > 100 else section_content['text']
                st.markdown(f"**Text Preview:** {text_preview}")
                
                # Preview of highlights
                if section_content['highlight_details']:
                    st.markdown("**Highlights:**")
                    for i, highlight in enumerate(section_content['highlight_details']):
                        highlight_preview = highlight[:20] + "..." if len(highlight) > 20 else highlight
                        st.markdown(f"- {highlight_preview}")
                else:
                    st.markdown("*No highlights found in this section*")
                
                # Add a remove button for this section
                if st.button(f"Remove {section_name}", key=f"remove_{section_name}", icon="🗑️"):
                    # Remove this section from session state
                    del st.session_state.section_data[section_name]
                    st.rerun()
    
    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back", use_container_width=True):
            st.session_state.current_step = "upload_pdf"
            
    with col2:
        if st.session_state.section_data:
            if st.button("Next: Generate Flashcards", type="primary", use_container_width=True):
                st.session_state.current_step = "generate_flashcards"