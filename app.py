import os
import re
from flask import Flask, request, jsonify
from search import search

app = Flask(__name__)

def clean_text(text):
    text = re.sub(r'[\uf0b7\u2022]', '-', text)
    text = re.sub(r'"', 'inch', text)
    text = re.sub(r'[^\x00-\x7F£]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@app.route("/search", methods=["POST"])
def search_route():
    data = request.json
    # query = data.get("query", "")
    query = data.get("args", {}).get("query", "")
    results = search(query)

    print(query)

    combined = ""
    for i, chunk in enumerate(results):
        combined += f"ITEM {i+1}: {clean_text(chunk)} "

    return jsonify({"result": combined.strip()})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)