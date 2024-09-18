# PDF Q&A Viewer

## Overview

PDF Q&A Viewer is a Python application designed to help users memorize questions and answers for tests, exams, or any learning scenario. This tool allows users to load a PDF file containing questions and answers, and then presents them in an interactive, randomized format for effective studying.

## Features

- Load questions and answers from a PDF file
- Display questions and answers in a clean, easy-to-read interface
- Randomize question order for varied practice
- Track progress with a question counter
- Simple and intuitive user interface

## Requirements

- Python 3.x
- tkinter
- PyPDF2

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/pdf-qa-viewer.git
   ```
2. Navigate to the project directory:
   ```
   cd pdf-qa-viewer
   ```
3. Install the required dependencies:
   ```
   pip install PyPDF2
   ```

## Usage

1. Run the script:
   ```
   python pdf_qa_viewer.py
   ```
2. Click the "Load PDF" button to select your PDF file.
3. Use the "Show Answer" button or press the spacebar to toggle between questions and answers.
4. Click "Next Question" or press the spacebar to move to the next question.

## PDF Format Requirements

For the application to work correctly, your PDF file must follow this format:

```
1.Q: Your question goes here?
R: Your answer goes here.

2.Q: Another question?
R: Another answer.
```

- Each question should start with a number followed by ".Q:"
- Each answer should start with "R:"
- Questions and answers can span multiple lines
- There should be a blank line between each Q&A pair

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/dhilanIM/Question-Shuffler).


Project Link: [https://github.com/dhilanIM/Question-Shuffler](https://github.com/dhilanIM/Question-Shuffler)
