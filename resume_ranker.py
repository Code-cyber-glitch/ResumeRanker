import os
import re
import csv
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import PyPDF2

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import classification_report

# ================= SETTINGS ================= #

BOOST_KEYWORDS = [
    'python','machine learning','deep learning','nlp','tensorflow',
    'pandas','numpy','sql','data analysis','flask','django'
]

MIN_WORDS = 50   # ignore resumes with too little text


# ================= TEXT PROCESSING ================= #

def read_job_description(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
    except Exception as e:
        print("PDF error:", e)
    return text


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)   # keep letters only
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def keyword_boost(text):
    score = 0
    matched = []
    for k in BOOST_KEYWORDS:
        if k in text:
            score += 0.03
            matched.append(k)
    return score, matched


# ================= CORE RANKING ================= #

def rank_resumes(resume_folder, jd_text):

    resumes = {}
    ignored = []

    for file in os.listdir(resume_folder):
        if file.endswith(".pdf"):
            path = os.path.join(resume_folder, file)
            txt = extract_text_from_pdf(path)

            if len(txt.split()) < MIN_WORDS:
                ignored.append(file)
                continue

            resumes[file] = txt

    if not resumes:
        return None, None, ignored, None

    documents = [jd_text] + list(resumes.values())

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform(documents)

    similarities = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()

    results = []
    all_predictions = []
    all_true = []

    for i, (name, text) in enumerate(resumes.items()):
        cleaned = clean_text(text)

        boost, matched_keywords = keyword_boost(cleaned)
        score = similarities[i] + boost

        results.append((name, score, matched_keywords))

        # ======= Fake labels for evaluation =======
        # If similarity > threshold -> relevant
        pred = 1 if score > 0.2 else 0
        true = 1 if len(matched_keywords) > 2 else 0

        all_predictions.append(pred)
        all_true.append(true)

    ranked = sorted(results, key=lambda x: x[1], reverse=True)

    report = classification_report(
        all_true, all_predictions,
        target_names=["Not Relevant","Relevant"],
        output_dict=True
    )

    return ranked, report, ignored, resumes


# ================= GUI ================= #

def launch_gui():

    root = tk.Tk()
    root.title("AI Resume Ranker")
    root.geometry("750x650")

    selected_folder = None
    selected_jd = None

    # ---------- FUNCTIONS ---------- #

    def choose_folder():
        nonlocal selected_folder
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            folder_label.config(text=f"Resumes: {os.path.basename(selected_folder)}")

    def choose_jd():
        nonlocal selected_jd
        selected_jd = filedialog.askopenfilename(filetypes=[("Text files",".txt")])
        if selected_jd:
            jd_label.config(text=f"JD: {os.path.basename(selected_jd)}")

    def start():

        if not selected_folder or not selected_jd:
            messagebox.showwarning("Missing", "Select both resumes and JD")
            return

        jd_text = read_job_description(selected_jd)

        progress['value'] = 10
        root.update_idletasks()

        ranked, report, ignored, resumes = rank_resumes(selected_folder, jd_text)

        if ranked is None:
            messagebox.showerror("Error","No valid resumes found")
            return

        progress['value'] = 70

        # ---------- SHOW RESULTS ---------- #

        result_box.delete('1.0', tk.END)
        result_box.insert(tk.END,"===== RANKED RESUMES =====\n\n")

        for i,(name,score,keywords) in enumerate(ranked,1):
            result_box.insert(tk.END,
                f"{i}. {name}\n"
                f"   Score: {score:.3f}\n"
                f"   Matched Skills: {', '.join(keywords) if keywords else 'None'}\n\n"
            )

        # ---------- SHOW METRICS ---------- #

        result_box.insert(tk.END,"\n===== MODEL METRICS =====\n")

        for label,data in report.items():
            if label in ["Relevant","Not Relevant"]:
                result_box.insert(tk.END,
                    f"\n{label}:\n"
                    f"Precision: {data['precision']:.2f}\n"
                    f"Recall: {data['recall']:.2f}\n"
                    f"F1-score: {data['f1-score']:.2f}\n"
                    f"Support: {data['support']}\n"
                )

        # ---------- SAVE CSV ---------- #

        with open("ranked_resumes.csv","w",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Rank","Resume","Score"])
            for i,(name,score,_) in enumerate(ranked,1):
                writer.writerow([i,name,f"{score:.3f}"])

        progress['value'] = 100
        messagebox.showinfo("Done","Ranking complete. CSV saved.")

    # ---------- UI ---------- #

    tk.Label(root,text="AI Resume Ranking System",font=("Arial",18,"bold")).pack(pady=15)

    tk.Button(root,text="Select Resume Folder",font=("Arial",12),command=choose_folder).pack(pady=5)
    folder_label = tk.Label(root,text="No folder selected")
    folder_label.pack()

    tk.Button(root,text="Select Job Description",font=("Arial",12),command=choose_jd).pack(pady=5)
    jd_label = tk.Label(root,text="No JD selected")
    jd_label.pack()

    tk.Button(root,text="Start Ranking",font=("Arial",14,"bold"),bg="#4CAF50",fg="white",command=start).pack(pady=15)

    progress = ttk.Progressbar(root,length=400,mode="determinate")
    progress.pack(pady=10)

    result_box = tk.Text(root,height=20,width=85,font=("Courier",10))
    result_box.pack(pady=10)

    root.mainloop()


# ================= RUN ================= #

launch_gui()