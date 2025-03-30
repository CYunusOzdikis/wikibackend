from flask import Flask, Response
from flask_cors import CORS
import wikipedia
import json
import os

# Flask uygulamasını oluştur
app = Flask(__name__)
CORS(app)

# Wikipedia dili Türkçe olarak ayarlanıyor
wikipedia.set_lang("tr")

# Günlük rastgele makaleyi getiren endpoint
@app.route("/daily", methods=["GET"])
def get_random_article():
    try:
        page = wikipedia.random()  # Rastgele başlık seç
        summary = wikipedia.summary(page, sentences=5)  # Özetini al (5 cümle)
        data = {
            "title": page,
            "content": summary
        }
        return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')

# Uygulama çalıştırma komutu (Render için özel port ayarı)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
