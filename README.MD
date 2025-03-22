# Highlight-to-Flashcard

A simple tool to convert highlighted text from PDFs into flashcards for learning and review.

## Overview

Highlight-to-Flashcard automatically extracts highlighted text from PDF files and uses an LLM to generate high-quality flashcards for spaced repetition learning. The tool is designed to save time for students and lifelong learners who want to create effective study materials from their reading.

## Features

- Extract highlighted text from PDFs
- Group extracted content by user-defined sections/chapters
- Generate flashcards using Gemma 3 LLM
- Edit and refine generated flashcards
- Export to Obsidian-compatible formats (single-line and multi-line)

## Requirements

- Python 3.8+
- Ollama (with Gemma 3 model installed)
- BAML

## Installation

1. Clone this repository
2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Make sure Ollama is installed and the Gemma 3 model is available

## Usage

Run the application:
```
streamlit run src/app.py
```

Then follow the step-by-step process:
1. Upload a PDF file
2. Define section boundaries (page numbers)
3. Extract highlights
4. Generate flashcards
5. Edit flashcards as needed
6. Export to your preferred format

## Limitations

- Currently only supports PDFs where highlights are properly marked as annotations
- Requires Ollama and Gemma 3 to be installed locally

## License

MIT