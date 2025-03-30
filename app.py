from flask import Flask, Response
from flask_cors import CORS
import wikipediaapi
import json
import os
import random

app = Flask(__name__)
CORS(app)

wiki_tr = wikipediaapi.Wikipedia(
    language='tr',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='WikibulyaApp/1.0 (cyunusozdikis@gmail.com)'
)

@app.route("/daily", methods=["GET"])
def get_random_article():
    try:
        # Türkçe Wikipedia'nın tüm sayfalarından rastgele bir tane seç (kategori üzerinden)
        popular_pages = [
            "Türkiye", "Ankara", "İstanbul", "Atatürk", "Mehmet Akif Ersoy",
            "Matematik", "Tarih", "Müzik", "Osmanlı İmparatorluğu", "Spor"
        ]
        title = random.choice(popular_pages)
        page = wiki_tr.page(title)

        if not page.exists():
            raise Exception("Makale bulunamadı.")

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
