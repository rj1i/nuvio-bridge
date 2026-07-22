from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
@app.route('/manifest.json')
def manifest():
    return jsonify({
        "id": "com.arabic.servers.bridge",
        "version": "1.0.0",
        "name": "السيرفرات العربية (قصة عشق & قرمزي)",
        "description": "جلب سيرفرات المشاهدة للمسلسلات التركية والعربية",
        "resources": ["stream"],  # الاعتماد فقط على نظام الـ Stream للمسلسلات الموجودة في التطبيق
        "types": ["series", "movie"],
        "idPrefixes": ["tt"]  # الاستجابة لمعرفات IMDb القياسية
    })

# استقبال طلب التشغيل بناءً على ID المسلسل من IMDb
# التنسيق بيكون: tt1234567:season:episode
@app.route('/stream/<type>/<id>.json')
def stream(type, id):
    # تفكيك المعرف لمعرفة المسلسل والموسم والحلقة
    parts = id.split(':')
    imdb_id = parts[0]
    season = parts[1] if len(parts) > 1 else "1"
    episode = parts[2] if len(parts) > 2 else "1"

    # هنا يتم وضع كود البحث (Scraper) للبحث عن السيرفرات الحقيقية
    # سنضع روابط توضيحية لبيان كيفية ظهور السيرفرات للمستخدم:
    streams = [
        {
            "name": "قصة عشق 360p/720p",
            "title": f"🎬 سيرفر قصة عشق - الموسم {season} الحلقة {episode}\nجودة عالية HD",
            "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
        },
        {
            "name": "قرمزي FHD",
            "title": f"🎬 سيرفر قرمزي - الموسم {season} الحلقة {episode}\nسيرفر سريع 1080p",
            "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4"
        }
    ]

    return jsonify({"streams": streams})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
