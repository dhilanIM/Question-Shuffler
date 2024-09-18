import tkinter as tk
from tkinter import filedialog, font, ttk
import PyPDF2
import random
import re

class PDFQAViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Q&A Viewer")
        self.master.geometry("800x600")
        self.master.minsize(400, 300)  # Set minimum window size
        self.master.configure(bg='#f0f0f0')

        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.qa_pairs = []
        self.current_pair = None
        self.showing_question = True
        self.total_questions = 0
        self.current_question = 0

        self.create_widgets()

    def create_widgets(self):
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=1)

        # Title
        self.title_label = ttk.Label(self.master, text="PDF Q&A Viewer", font=("Arial", 24, "bold"))
        self.title_label.grid(row=0, column=0, pady=(20, 10), sticky="nsew")
        self.master.grid_columnconfigure(0, weight=1)

        # Main frame for text and scrollbar
        main_frame = ttk.Frame(self.master, padding="20 10 20 10")
        main_frame.grid(row=1, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # Text widget
        self.text = tk.Text(main_frame, wrap=tk.WORD, font=("Georgia", 14), relief=tk.RIDGE, borderwidth=2, state='disabled')
        self.text.grid(row=0, column=0, sticky="nsew")
        self.text.configure(bg='#ffffff', fg='#333333', padx=10, pady=10)

        self.text.tag_configure("question", font=("Georgia", 14, "bold"), foreground="#0066cc")
        self.text.tag_configure("answer", font=("Georgia", 14, "italic"), foreground="#006600")
        self.text.tag_configure("counter", font=("Arial", 12), foreground="#666666")

        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.text.configure(yscrollcommand=scrollbar.set)

        # Button frame
        self.button_frame = ttk.Frame(self.master)
        self.button_frame.grid(row=2, column=0, pady=20, sticky="ew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)

        # Buttons
        self.load_button = ttk.Button(self.button_frame, text="Load PDF", command=self.load_pdf, style='Accent.TButton')
        self.load_button.grid(row=0, column=0, padx=5)

        self.toggle_button = ttk.Button(self.button_frame, text="Show Answer", command=self.toggle_qa, style='Accent.TButton')
        self.toggle_button.grid(row=0, column=1, padx=5)
        self.toggle_button.state(['disabled'])

        self.master.bind("<space>", self.toggle_qa)

        self.style.configure('Accent.TButton', font=('Arial', 12), background='#4CAF50', foreground='white')
        self.style.map('Accent.TButton', background=[('active', '#45a049')])

    def load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            try:
                self.qa_pairs = self.extract_qa_from_pdf(file_path)
                self.total_questions = len(self.qa_pairs)
                self.current_question = 0
                self.show_next_question()
                self.toggle_button.state(['!disabled'])
            except Exception as e:
                self.set_text(f"Error loading PDF: {str(e)}")

    def extract_qa_from_pdf(self, file_path):
        qa_pairs = []
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

        text = re.sub(r'\n+', ' ', text)
        
        pattern = r'(\d+\.Q:.*?)(?=\d+\.Q:|$)'
        matches = re.findall(pattern, text, re.DOTALL)

        for match in matches:
            parts = match.split('R:', 1)
            if len(parts) == 2:
                question = self.clean_text(parts[0])
                answer = self.clean_text(parts[1])
                qa_pairs.append((question, answer))

        return qa_pairs

    def clean_text(self, text):
        # Remove question number and 'Q:' prefix
        text = re.sub(r'^\d+\.Q:', '', text.strip())
        # Remove any leading whitespace after removing the prefix
        text = text.lstrip()
        # Replace multiple whitespace characters with a single space
        text = re.sub(r'\s+', ' ', text)
        return text

    def set_text(self, content, tags=None):
        self.text.config(state='normal')
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, content, tags)
        self.text.config(state='disabled')

    def show_next_question(self):
        if self.qa_pairs:
            self.current_pair = random.choice(self.qa_pairs)
            self.qa_pairs.remove(self.current_pair)
            self.current_question += 1
            counter_text = f"Question {self.current_question}/{self.total_questions}\n\n"
            self.set_text(counter_text, "counter")
            self.text.config(state='normal')
            self.text.insert(tk.END, self.current_pair[0], "question")
            self.text.config(state='disabled')
            self.showing_question = True
            self.toggle_button.config(text="Show Answer")
        else:
            self.set_text("All questions have been shown.", "question")
            self.toggle_button.config(text="Restart")
            self.load_button.state(['disabled'])

    def toggle_qa(self, event=None):
        if self.current_pair:
            if self.showing_question:
                counter_text = f"Question {self.current_question}/{self.total_questions}\n\n"
                self.set_text(counter_text, "counter")
                self.text.config(state='normal')
                self.text.insert(tk.END, f"{self.current_pair[0]}\n\n", "question")
                self.text.insert(tk.END, self.current_pair[1], "answer")
                self.text.config(state='disabled')
                self.showing_question = False
                self.toggle_button.config(text="Next Question")
            else:
                self.show_next_question()

    def restart(self):
        self.load_pdf()
        self.toggle_button.config(text="Show Answer")
        self.load_button.state(['!disabled'])

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFQAViewer(root)
    root.mainloop()