from flask import Flask, Response
from flask_cors import CORS
import wikipedia
import json
import os
import html

app = Flask(__name__)
CORS(app)

wikipedia.set_lang("tr")

@app.route("/daily", methods=["GET"])
def get_random_article():
    try:
        page = wikipedia.random()
        summary = wikipedia.summary(page, sentences=5)
        clean_summary = html.unescape(summary)  # Karakter düzeltme
        data = {
            "title": page,
            "content": clean_summary
        }
        return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
