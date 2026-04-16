from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESUME_FOLDER = os.path.join(BASE_DIR, "..", "resumes")

def clean(text):
    return text.lower()

def get_experience(text):
    match = re.search(r'(\d+)\s*year', text)
    return int(match.group(1)) if match else 0

def read_resumes():
    texts, names = [], []
    for file in os.listdir(RESUME_FOLDER):
        if file.endswith(".txt"):
            with open(os.path.join(RESUME_FOLDER, file), "r", encoding="utf-8") as f:
                texts.append(f.read())
                names.append(file)
    return texts, names

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    skills = data.get("skills", [])

    if not skills:
        return jsonify({"error": "No skills provided"})

    job_desc = " ".join(skills)

    resumes, names = read_resumes()

    documents = [job_desc] + resumes

    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform(documents)

    similarity = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

    results = []

    for i in range(len(names)):
        text = clean(resumes[i])

        matched = []
        for s in skills:
            if s.lower().replace("+","") in text.replace("+",""):
                matched.append(s)

        keyword_score = (len(matched)/len(skills))*100
        ai_score = similarity[i]*100
        exp = get_experience(text)

        final_score = round(0.7*ai_score + 0.3*keyword_score + exp*5, 2)

        results.append({
            "name": names[i],
            "score": final_score,
            "match": round(ai_score,2),
            "matched": matched
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return jsonify(results)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file.save(os.path.join(RESUME_FOLDER, file.filename))
    return jsonify({"msg": "uploaded"})

if __name__ == "__main__":
    app.run(debug=True)