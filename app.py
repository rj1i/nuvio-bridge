from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "Server is running successfully!"})

@app.route('/manifest.json')
def manifest():
    return jsonify({
        "id": "com.nuvio.arabic.bridges",
        "version": "1.0.0",
        "name": "المسلسلات العربية والتركية",
        "description": "جلب حلقات قصة عشق وقرمزي",
        "resources": ["catalog", "stream"],
        "types": ["series"],
        "idPrefixes": ["qesset_", "krmizi_"],
        "catalogs": [
            {
                "type": "series",
                "id": "qesset_catalog",
                "name": "قصة عشق"
            },
            {
                "type": "series",
                "id": "krmizi_catalog",
                "name": "قرمزي"
            }
        ]
    })

@app.route('/episodes/qesset')
def qesset():
    return jsonify({
        "status": "success",
        "source": "qesset",
        "data": [
            {"title": "قصة عشق - تجربة", "url": "https://example.com/video.mp4"}
        ]
    })

@app.route('/episodes/krmizi')
def krmizi():
    return jsonify({
        "status": "success",
        "source": "krmizi",
        "data": [
            {"title": "قرمزي - تجربة", "url": "https://example.com/video.mp4"}
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
