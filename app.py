from flask import Flask, Response
from flask_cors import CORS
import datetime
import json
import os

app = Flask(__name__)
CORS(app)

@app.route("/daily", methods=["GET"])
def get_daily_article():
    today = datetime.date.today().isoformat()
    data = {
        "date": today,
        "title": "Türkiye",
        "content": "Türkiye, Asya ve Avrupa kıtaları arasında yer alan bir ülkedir. Başkenti Ankara'dır."
    }
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
