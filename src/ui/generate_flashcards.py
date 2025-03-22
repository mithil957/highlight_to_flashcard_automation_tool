import streamlit as st
from baml_utils.baml_utils import generate_flashcards, format_for_obsidian

def display_generate_flashcards():
    st.title("Step 3: Generate Flashcards")
    
    # Check if section data is in session state
    if 'section_data' not in st.session_state or not st.session_state.section_data:
        st.error("No sections configured. Please go back and configure sections first.")
        if st.button("Back to Section Configuration"):
            st.session_state.current_step = "configure_sections"
        return
    
    st.markdown("### Generate flashcards for each section")
    
    # Initialize flashcards in session state if not already there
    if 'flashcards' not in st.session_state:
        st.session_state.flashcards = {}
    
    # Display each section with generation button
    for section_name, section_content in st.session_state.section_data.items():
        with st.expander(f"{section_name}", expanded=True):
            # Display section info
            st.markdown(f"**Text preview:** {section_content['text'][:100]}...")
            st.markdown(f"**Highlights:** {len(section_content['highlight_details'])} highlights found")
            
            # Check if flashcards already exist for this section
            if section_name in st.session_state.flashcards:
                st.success(f"{len(st.session_state.flashcards[section_name])} flashcards generated")
                
                # Display flashcards
                for i, card in enumerate(st.session_state.flashcards[section_name]):
                    st.markdown(f"**Card {i+1}:** {card['type']}")
                    st.markdown(f"**Front:** {card['front']}")
                    st.markdown(f"**Back:** {card['back']}")
                    st.markdown("---")
                
                # Display Obsidian export option
                st.markdown("### Export to Obsidian")
                if st.button("Format for Obsidian", key=f"btn_obsidian_{section_name}"):
                    obsidian_text = format_for_obsidian(
                        st.session_state.flashcards[section_name], 
                        format_type="single-line"
                    )
                    st.session_state[f"obsidian_{section_name}"] = obsidian_text
                
                # Show the formatted text if available
                if f"obsidian_{section_name}" in st.session_state:
                    st.markdown("### Obsidian Format")
                    st.code(st.session_state[f"obsidian_{section_name}"], language="markdown")
                    
                    # Copy button
                    if st.button("Copy to Clipboard", key=f"copy_{section_name}"):
                        st.toast("Copied to clipboard!")
                        # Note: actual clipboard functionality is limited in Streamlit
                
                # Regenerate button
                if st.button("Regenerate Flashcards", key=f"regen_{section_name}"):
                    # Clear existing flashcards for this section
                    if section_name in st.session_state.flashcards:
                        del st.session_state.flashcards[section_name]
                    # Also clear Obsidian format if it exists
                    if f"obsidian_{section_name}" in st.session_state:
                        del st.session_state[f"obsidian_{section_name}"]
                    st.rerun()
            
            else:
                # Show generate button
                if st.button(
                    "Generate Flashcards", 
                    key=f"gen_{section_name}",
                    type="primary"
                ):
                    try:
                        # Show a spinner while processing
                        with st.spinner(f"Generating flashcards for {section_name}..."):
                            # Get data for flashcard generation
                            chapter_data = {
                                'text': section_content['text'],
                                'highlights': section_content['highlight_details'],
                            }
                            
                            # Generate flashcards
                            flashcards = generate_flashcards(chapter_data, use_detailed=True)
                            
                            # Store in session state
                            st.session_state.flashcards[section_name] = flashcards
                            
                            st.success(f"Generated {len(flashcards)} flashcards!")
                            
                            # Rerun to update UI
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error generating flashcards: {e}")

    
    # Navigation button
    if st.button("Back to Sections", use_container_width=True):
        st.session_state.current_step = "configure_sections"