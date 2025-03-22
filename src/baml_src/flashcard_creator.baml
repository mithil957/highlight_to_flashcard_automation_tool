class StudyInput {
    text string
    highlights string[]
    notes string[]
}

class Flashcard {
    type FlashcardType
    front string
    back string
}

enum FlashcardType {
    BASIC_FACT
    EXPLANATION
    APPLICATION
    CONTEXT
}

function GenerateFlashcardsDetailed(input: StudyInput) -> Flashcard[] {
    client Gemma3

    prompt #"
        Generate focused flashcards from the following text, highlighted sections, and notes. 
        Each card should target one discrete concept or fact.

        Text:
        ---
        {{ input.text }}
        ---

        Highlighted Sections:
        {% for highlight in input.highlights %}
        - {{ highlight }}
        {% endfor %}

        Notes:
        {% for note in input.notes %}
        - {{ note }}
        {% endfor %}

        Create flashcards following these formats:

        1. Basic Fact/Concept (type: BASIC_FACT)
        - Front: What is [concept]?
        - Back: [concise definition, avoiding question phrasing]

        2. Explanation/Understanding (type: EXPLANATION)
        - Front: Why does [concept/phenomenon] occur?
        - Back: [mechanism/rationale]

        3. Application (type: APPLICATION)
        - Front: How would you use [concept] to solve [specific scenario]?
        - Back: [concrete application steps]

        4. Context/Relationship (type: CONTEXT)
        - Front: How does [concept] relate to [related concept]?
        - Back: [key relationship/distinction]

        Guidelines:
        - Each card focuses on one specific detail
        - Questions are precise and unambiguous 
        - Answers don't repeat question phrasing
        - Include explanatory cards for important concepts
        - Add helpful cues that don't give away answers
        - Avoid cards requiring lists of items

        {{ ctx.output_format }}

        JSON:
    "#
}

function GenerateFlashcardsSimple(input: StudyInput) -> Flashcard[] {
    client Gemma3

    prompt #"
        Create concise, simple, straightforward and distinct Anki cards to study the following text, highlights, and notes. 
        Each with a front and back. Avoid repeating the content in the front on the back of the card. 
        In particular, if the front is a question and the back an answer, avoid repeating the phrasing of the question as the initial part of the answer. 
        Avoid explicitly referring to the author or the article in the cards, and instead treat the article as factual and independent of the author.
        
        Text:
        ---
        {{ input.text }}
        ---

        Highlighted Sections:
        {% for highlight in input.highlights %}
        - {{ highlight }}
        {% endfor %}

        Notes:
        {% for note in input.notes %}
        - {{ note }}
        {% endfor %}

        {{ ctx.output_format }}

        JSON:
    "#
}


test TestFlashcards {
    functions [GenerateFlashcardsSimple]
    args {
        input {
            text #"
                Book text goes here when testing...
            "#
            highlights []
            notes []
        }
    }
}