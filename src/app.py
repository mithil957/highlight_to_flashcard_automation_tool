import streamlit as st
from ui.home_page import display_home
from ui.upload_pdf import display_upload_pdf
from ui.configure_sections import display_configure_sections
from ui.generate_flashcards import display_generate_flashcards


def main():
    # Initialize session state for navigation
    if 'current_step' not in st.session_state:
        st.session_state.current_step = "home"
    
    if st.session_state.current_step == "home":
        display_home()
    elif st.session_state.current_step == "upload_pdf":
        display_upload_pdf()
    elif st.session_state.current_step == "configure_sections":
        display_configure_sections()
    elif st.session_state.current_step == "generate_flashcards":
        display_generate_flashcards()
    

if __name__ == "__main__":
    st.set_page_config(
        page_title="Highlight-to-Flashcard",
        page_icon="📚",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    main()