from flask import Flask, Response
from flask_cors import CORS
import wikipediaapi
import json
import os
import random

app = Flask(__name__)
CORS(app)

wiki_tr = wikipediaapi.Wikipedia('tr')

@app.route("/daily", methods=["GET"])
def get_random_article():
    try:
        # Tüm maddelerden rastgele bir başlık al
        random_titles = [page for page in wiki_tr.random(100) if ':' not in page]
        title = random.choice(random_titles)
        
        page = wiki_tr.page(title)
        if not page.exists():
            return Response(json.dumps({"error": "Sayfa bulunamadı"}), status=404, mimetype='application/json')
        
        data = {
            "title": page.title,
            "content": page.summary
        }
        return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
