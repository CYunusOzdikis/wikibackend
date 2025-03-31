from flask import Flask, Response
from flask_cors import CORS
import wikipediaapi
import random
import json
import os
import zeyrek

app = Flask(__name__)
CORS(app)

# Wikipedia Türkçe ayarı
wiki_tr = wikipediaapi.Wikipedia(
    language='tr',
    user_agent='WikibulyaApp/1.0 (cyunusozdikis@gmail.com)'
)

# Zeyrek kök bulucu başlat
analyzer = zeyrek.MorphAnalyzer()

# Kök çıkaran fonksiyon
def get_root(word):
    analyses = analyzer.analyze(word)
    if analyses:
        lemmas = analyses[0].lemma_root_candidates
        if lemmas:
            return lemmas[0][0]
    return word.lower()

@app.route("/daily", methods=["GET"])
def get_random_article():
    try:
        # Türkçe Wikipedia’daki rastgele sayfalardan biri
        random_titles = [
            "Türkiye", "Matematik", "Fizik", "Tarih", "İstanbul",
            "Sanat", "Felsefe", "Biyoloji", "Bilgisayar", "Müzik"
        ]
        title = random.choice(random_titles)
        page = wiki_tr.page(title)

        if not page.exists():
            raise Exception("Makale bulunamadı.")

        print("📄 Seçilen makale:", title)  # Terminal log

        data = {
            "title": page.title,
            "content": page.summary
        }

        return Response(
            json.dumps(data, ensure_ascii=False),
            content_type="application/json; charset=utf-8"
        )

    except Exception as e:
        return Response(
            json.dumps({"error": str(e)}, ensure_ascii=False),
            status=500,
            content_type="application/json; charset=utf-8"
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
