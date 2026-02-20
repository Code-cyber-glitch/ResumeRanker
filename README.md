# 🚀 AI Resume Ranker – NLP-Based Candidate Screening System

An intelligent Resume Ranking System that automatically evaluates and ranks candidate resumes against a given job description using Natural Language Processing (NLP) techniques.

This project simulates how modern Applicant Tracking Systems (ATS) filter candidates by analyzing skills, experience, and keyword relevance.

---

## 🎯 Project Objective

Recruiters often receive hundreds of resumes for a single role.
This system helps automate the screening process by:

* Extracting text from resumes (PDF)
* Cleaning and preprocessing candidate data
* Comparing resumes with a job description
* Ranking candidates based on relevance score
* Generating evaluation metrics for model performance

---

## 🧠 Key Features

✔ Resume parsing from **text-based PDFs**
✔ Job Description vs Resume similarity scoring
✔ TF-IDF based NLP matching
✔ Cosine similarity ranking system
✔ Automatic candidate classification (Relevant / Not Relevant)
✔ Performance metrics:

* Accuracy
* Precision
* Recall
* F1-score
* Support

✔ Clean console output with ranked candidate list
✔ Modular and reproducible code structure

---

## 🛠 Tech Stack

* Python
* Scikit-learn
* Pandas
* NumPy
* PDF text extraction libraries
* NLP preprocessing techniques

---

## 📂 Project Structure

```
AI-Resume-Ranker/
│
├── resumes/                # Sample candidate resumes (PDF)
├── job_description.txt      # Target job role description
├── main.py                  # Resume ranking pipeline
├── requirements.txt
└── README.md
```

---

## ⚙️ How It Works

1. Load job description text
2. Extract text from each resume PDF
3. Preprocess text (lowercase, remove stopwords, clean tokens)
4. Convert documents into TF-IDF vectors
5. Compute cosine similarity scores
6. Rank resumes from highest to lowest relevance
7. Classify resumes as **Relevant / Not Relevant**
8. Print performance metrics

---

### 🚀 How to Use

### 1️⃣ Add resumes and job description

- Place all **text-based PDF resumes** inside the folder:

/resumes

- Add your target job description in the file:

job_description.txt

Make sure the job description clearly includes required:
- Skills  
- Tools  
- Responsibilities  
- Technologies  

Better job descriptions = better ranking results.

---

### 2️⃣ Run the program

Execute the script from the project folder:

python resume_ranker.py

---

### 3️⃣ View results

After running, the system will:

- 📊 Rank resumes based on similarity score  
- ✅ Classify candidates as **Relevant / Not Relevant**  
- 📈 Show evaluation metrics:
  - Accuracy
  - Precision
  - Recall
  - F1-score
- 📁 Save ranked results into a CSV file  

---

### ⚠️ Important Notes

- Only **text-based PDFs** are supported  
- Scanned/image resumes will not work  
- Keep resumes inside the `/resumes` folder only  
- Ensure Python dependencies are installed before running  

---

## 📊 Example Output

```
===== RANKED RESUMES =====

1. sample_1.pdf
   Score: 0.481
   Matched Skills: python, machine learning, pandas, numpy, sql, data analysis

2. sample_2.pdf
   Score: 0.471
   Matched Skills: python, machine learning, deep learning, sql, data analysis, flask

3. sample_3.pdf
   Score: 0.383
   Matched Skills: python, machine learning, deep learning, tensorflow, pandas, sql, flask

4. sample_7.pdf
   Score: 0.324
   Matched Skills: python, deep learning, tensorflow, pandas, numpy, sql

5. sample_4.pdf
   Score: 0.071
   Matched Skills: None

6. sample_8.pdf
   Score: 0.058
   Matched Skills: None

7. sample_5.pdf
   Score: 0.056
   Matched Skills: None

8. sample_10.pdf
   Score: 0.053
   Matched Skills: None

9. sample_6.pdf
   Score: 0.043
   Matched Skills: None

10. sample_9.pdf
   Score: 0.034
   Matched Skills: None


===== MODEL METRICS =====

Not Relevant:
Precision: 1.00
Recall: 1.00
F1-score: 1.00
Support: 6.0

Relevant:
Precision: 1.00
Recall: 1.00
F1-score: 1.00
Support: 4.0
```

---

## 📥 Dataset Credits

Sample resumes used in this project are sourced from publicly available datasets on **Kaggle** for educational and research purposes.

Proper credit belongs to the original dataset creators on Kaggle.
These resumes are used solely to demonstrate the functionality of the resume ranking system.

If you plan to reuse the dataset, please refer to the original Kaggle dataset license and attribution guidelines.

Dataset source:
🔗https://www.kaggle.com/datasets/hadikp/resume-data-pdf

---

## 👨‍💻 Author

**Manan Pal**
B.Tech CSE Student | Aspiring Software & AI Developer

---

## ⭐ If you like this project

Give it a ⭐ on GitHub — it motivates further improvements!

---
