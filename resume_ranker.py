import os
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv
import re
from sklearn.feature_extraction import text as sklearn_text
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

BOOST_KEYWORDS = ['python','machine learning','django','rest api','tensorflow','flask']
selected_folder_path = r"C:\Projects\ResumeRanker\resumes"
selected_jd_path = r"C:\Projects\ResumeRanker\job_description.txt"

def read_job_description(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text_from_pdf(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def clean_text(text_data):
    text_data = text_data.lower()
    text_data = re.sub(r'[a-z\s]','',text_data)
    return text_data

def calculate_keyword_boost(text):
    boost = 0
    for keyword in BOOST_KEYWORDS:
        if keyword in text:
            boost += 0.05
    return boost

def update_button_state(start_button):
    if selected_folder_path and selected_jd_path:
        start_button.config(state="normal")
    else:
        start_button.config(state="disabled")
        
def display_ranked_resumes():
        
    def choose_resume_folder():
        global selected_folder_path
        selected_folder_path = filedialog.askdirectory(title="Select folder containing all Resumes")
        if selected_folder_path:
            print(f"Resumes will be loaded from: {selected_folder_path}")

    def choose_jd_file():
        global selected_jd_path
        selected_jd_path = filedialog.askopenfilename(title="Select Job Description Text file", filetypes=[("Text files", ".txt")])
        if selected_jd_path:
            progress_label.config(text=f"Job decription loaded: {os.path.basename(selected_jd_path)}")

    def start_program():
        if not selected_folder_path:
            messagebox.showwarning("No folder", "Please select a resume folder first!")
            return
        try:
            if not selected_jd_path:
                messagebox.showwarning("NO JD", "Please select a Job Description file first!")
                return
            job_description = read_job_description(selected_jd_path)
        except FileNotFoundError:
            messagebox.showerror("Error",f"Job description file '{JD_FILE}' not found")
            return
        except Exception as e:
            messagebox.showerror("Error", f"An error ocurred while reading the job description: {str(e)}")
            return
            
        resumes_text = {}
        for filename in os.listdir(selected_folder_path):
            if filename.endswith('.pdf'):
                path = os.path.join(selected_folder_path, filename)
                try:
                    resume_text = extract_text_from_pdf(path)
                    resumes_text[filename] = resume_text
                except Exception as e:
                    messagebox.showwarning("PDF Error", f"Could not process {filename}.Error: {str(e)}")

        if not resumes_text:
            messagebox.showinfo("Info", "No resumes found in the folder!")
            return

        documents = [job_description] + list(resumes_text.values())

        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(documents)

        similarity_scores = cosine_similarity(tfidf_matrix[0:1],tfidf_matrix[1:]).flatten()

        progress_bar['value'] = 10
        
        final_scores = []
        for idx,(name, content) in enumerate(resumes_text.items()):
            cleaned_content = clean_text(content)
            boost = calculate_keyword_boost(cleaned_content)
            final_score = similarity_scores[idx] + boost
            final_scores.append((name, final_score))
            
            progress = int(((idx+1)/ len(resumes_text))*100)
            progress_bar['value'] = progress
            root.update_idletasks()
    
        ranked_resumes = sorted(final_scores, key=lambda x: x[1], reverse=True)

        output_file = 'ranked_resumes.csv'

        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Rank','Resume Name', 'Similarity Score'])
            for rank, (name, score) in enumerate(ranked_resumes, 1):
                writer.writerow([rank, name, f"{score:.4f}"])

        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, "Ranked resumes:\n\n")
        for rank, (name, score) in enumerate(ranked_resumes, 1):
            result_text.insert(tk.END, f"{rank}.{name} - Score: {score:.4f}\n")

        progress_bar['value'] = 100
        root.update_idletasks()
        
        messagebox.showinfo("Success", f"Ranking complete! Results saved to '{output_file}'.")

    root = tk.Tk()
    root.title("Ranked Resumes")
    root.geometry("700x600")
    
    label = tk.Label(root, text="Welcome to Resume ranker \n Choose a folder to load resumes.",font=("Arial",14))
    label.pack(pady=20)

    choose_button = tk.Button(root, text="Choose resume folder", font=("Arial", 14), command=choose_resume_folder)
    choose_button.pack(pady=10)
    choose_button.config(command=lambda: (choose_resume_folder(), update_button_state(start_button)))

    jd_button = tk.Button(root, text="Choose Job Description", font=("Arial", 14), command=choose_jd_file)
    jd_button.pack(pady=10)
    jd_button.config(command=lambda: (choose_jd_file(), update_button_state(start_button)))

    progress_label = tk.Label(root, text="Progress: waiting for action", font=("Arial", 14))
    progress_label.pack(pady=10)

    start_button = tk.Button(root, text="Start Processing", font=("Arial", 14), command=start_program)
    start_button.pack(pady=10)
    
    result_text = tk.Text(root, height=10, width=60, font=("Courier", 10))
    result_text.pack(pady=10)
    result_text.insert(tk.END, "Ranked Resumes: \n")
    result_text.insert(tk.END, "{:<5} {:<25} {:<15} \n".format("Rank", "Resume Name", "Similarity Score"))
    result_text.insert(tk.END, "-"*60 + "\n")

    progress_bar = ttk.Progressbar(root, length=300, mode="determinate", maximum=100, value=0)
    progress_bar.pack(pady=20)

    root.mainloop()
        
display_ranked_resumes()
