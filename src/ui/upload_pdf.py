import streamlit as st
import tempfile
from extractors.pdf_extractor import PDFExtractor

def display_upload_pdf():
    st.title("Step 1: Upload your PDF")
    
    st.markdown("""
    Upload a PDF file containing highlights that you want to convert into flashcards.
    """)
    
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Display file info
        st.success(f"Uploaded: {uploaded_file.name}")
        
        # Create a button to proceed
        if st.button("Next: Configure Sections", type="primary", use_container_width=True):
            # Initialize PDF extractor
            extractor = PDFExtractor()
            success = extractor.load_pdf(uploaded_file)
            
            if not success:
                st.error("Failed to load PDF. Please check if the file is valid.")
                return
            
            # Store the loaded PDF in session state for the next step
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp.write(uploaded_file.getvalue())
                temp_path = tmp.name
            
            # Save the path to session state
            st.session_state.pdf_path = temp_path
            st.session_state.pdf_filename = uploaded_file.name
            st.session_state.current_step = "configure_sections"
    
    # Add a back button
    if st.button("Back to Home"):
        st.session_state.current_step = "home"