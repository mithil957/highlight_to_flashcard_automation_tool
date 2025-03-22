import streamlit as st

def display_home():
    st.title("Highlight-to-Flashcard 📚")
    
    st.markdown("""
    ### Transform your PDF highlights into effective study flashcards
    
    This tool extracts highlighted text from your PDF files and uses an LLM to generate 
    flashcards for spaced repetition learning.
    
    **Features:**
    - Extract highlighted text from PDFs
    - Group extracted content by sections/chapters
    - Generate flashcards using Gemma 3 LLM
    - Edit and refine generated flashcards
    - Export to popular formats (Obsidian, Anki)
    
    Get started by clicking the button below:
    """)
    
    if st.button("Begin", type="primary", use_container_width=True):
        st.session_state.current_step = "upload_pdf"