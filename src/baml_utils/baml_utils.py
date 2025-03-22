import baml_client as client
from typing import List, Dict, Any

def generate_flashcards(chapter_data: Dict[str, Any], use_detailed: bool = True) -> List[Dict[str, str]]:
    try:
        # Create input object for BAML client
        study_input = client.types.StudyInput(
            text=chapter_data['text'],
            highlights=chapter_data['highlights'],
            notes=[]  # Empty for now, could add user notes in future
        )
        
        # Call the appropriate BAML function
        if use_detailed:
            flashcards = client.b.GenerateFlashcardsDetailed(input=study_input)
        else:
            flashcards = client.b.GenerateFlashcardsSimple(input=study_input)
        
        # Convert to serializable format
        serializable_cards = []
        for card in flashcards:
            serializable_cards.append({
                'type': card.type.value,
                'front': card.front,
                'back': card.back
            })
        
        return serializable_cards
    
    except Exception as e:
        print(f"Error generating flashcards: {e}")
        return []

def format_for_obsidian(flashcards: List[Dict[str, str]], format_type: str = "single-line") -> str:
    obsidian_text = f"# Flashcards\n\n"
    
    if format_type == "single-line":
        separator = "::"
        for card in flashcards:
            # Clean any newlines from front and back to ensure single-line format
            front = card['front'].replace('\n', ' ').strip()
            back = card['back'].replace('\n', ' ').strip()
            obsidian_text += f"{front}{separator}{back}\n\n"
    else:  # multi-line
        separator = "?"
        for card in flashcards:
            front = card['front'].strip()
            back = card['back'].strip()
            obsidian_text += f"{front}\n{separator}\n{back}\n\n"
    
    # Add tag to make it recognized as flashcard deck
    obsidian_text += "#flashcard"
    
    return obsidian_text