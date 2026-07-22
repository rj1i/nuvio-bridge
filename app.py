from flask import Flask, jsonify, Response
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# إجبار Flask على عدم تشفير الأحرف العربية إلى Unicode
app.config['JSON_AS_ASCII'] = False

@app.route('/')
@app.route('/manifest.json')
def manifest():
    data = {
        "id": "com.arabic.servers.bridge",
        "version": "1.0.0",
        "name": "السيرفرات العربية (قصة عشق & قرمزي)",
        "description": "جلب سيرفرات المشاهدة للمسلسلات التركية والعربية",
        "resources": ["stream"],
        "types": ["series", "movie"],
        "idPrefixes": ["tt"]
    }
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')

@app.route('/stream/<type>/<id>.json')
def stream(type, id):
    parts = id.split(':')
    season = parts[1] if len(parts) > 1 else "1"
    episode = parts[2] if len(parts) > 2 else "1"

    # استخدام روابط HLS (.m3u8) المتوافقة كلياً مع iOS والشاشات الذكية
    streams = [
        {
            "name": "قصة عشق",
            "title": f"🎬 قصة عشق - S{season} E{episode} (1080p Auto)",
            "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8",
            "behaviorHints": {
                "notSupported": False
            }
        },
        {
            "name": "قرمزي",
            "title": f"🎬 قرمزي - S{season} E{episode} (720p HD)",
            "url": "https://playertest.longtailvideo.com/adaptive/oceans/oceans.m3u8",
            "behaviorHints": {
                "notSupported": False
            }
        }
    ]

    return Response(json.dumps({"streams": streams}, ensure_ascii=False), mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
