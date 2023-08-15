import PyPDF2
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog

def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    pdf_text = ""
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pdf_text += page.get_text()
    
    pdf_document.close()
    return pdf_text

def extract_qna_pairs(text):
    qna_pairs = []
    lines = text.split('\n')  # Split text into lines

    current_question = None
    for line in lines:
        if '?' in line:  # Identify lines containing questions
            if current_question:  # Save previous question-answer pair
                qna_pairs.append((current_question, current_answer))
            current_question = line
            current_answer = ""
        elif current_question is not None:  # Collect lines as answer
            current_answer += line + " "

    # Append the last question-answer pair
    if current_question:
        qna_pairs.append((current_question, current_answer))

    return qna_pairs



def find_answer(question, qna_pairs):
    for q, a in qna_pairs:
        if question.lower() in q.lower():
            return a.strip()
    return "No answer found"


def search_in_pdf():
    search_term = search_entry.get()
    if not search_term:
        result_label.config(text="Please enter a search term.")
        return
    
    #-------------------------------------------------------
    #pdf_path = '/content/sample.pdf'
    
    pdf_path = file_path_label["text"]
    pdf_text = extract_text_from_pdf(pdf_path)

    qna_pairs = extract_qna_pairs(pdf_text)
    #question_to_check = "What is an attribute?"
    # Find the answer for the question
    answer = find_answer(search_term, qna_pairs)
    result_label.config(text=answer)
    
def upload_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        file_path_label.config(text=file_path)
        result_label.config(text="")
        
    

# Create the main application window
root = tk.Tk()
root.title("PDF Search App")

# Create widgets
upload_button = tk.Button(root, text="Upload PDF", command=upload_pdf)
search_entry = tk.Entry(root, width=30)
search_button = tk.Button(root, text="Search", command=search_in_pdf)
file_path_label = tk.Label(root, text="")
result_label = tk.Label(root, text="")

# Pack widgets
upload_button.pack(pady=10)
search_entry.pack(pady=5)
search_button.pack(pady=5)
file_path_label.pack(pady=5)
result_label.pack(pady=5)

# Start the main event loop
root.mainloop()
