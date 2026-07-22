from flask import Flask, jsonify, Response
from flask_cors import CORS
import json
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

app.config['JSON_AS_ASCII'] = False

@app.route('/')
@app.route('/manifest.json')
def manifest():
    data = {
        "id": "com.arabic.servers.bridge",
        "version": "1.0.0",
        "name": "السيرفرات العربية (قصة عشق & قرمزي)",
        "description": "جلب سيرفرات المشاهدة المباشرة والخارجية للمسلسلات",
        "resources": ["stream"],
        "types": ["series", "movie"],
        "idPrefixes": ["tt"]
    }
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')

# دالة البحث والاستخراج الحقيقي من المواقع
def fetch_real_streams(series_title, season, episode):
    found_streams = []
    
    # 1. البحث في موقع قصة عشق وقرمزي باستخدام اسم المسلسل والحلقة
    # 2. استخراج مشغلات الفيديو المتعددة (Dailymotion, OK.ru, HLS Streams)
    # 3. إضافتها إلى قائمة found_streams
    
    # مثال للتأكيد على كيفية تحويل السيرفرات الخارجية إلى قائمة Nuvio:
    # found_streams.append({
    #     "name": "قصة عشق - Dailymotion",
    #     "title": f"🎬 سيرفر Dailymotion - حلقة {episode}",
    #     "url": "رابط_الفيديو_المستخرج"
    # })
    
    return found_streams

@app.route('/stream/<type>/<id>.json')
def stream(type, id):
    parts = id.split(':')
    imdb_id = parts[0]
    season = parts[1] if len(parts) > 1 else "1"
    episode = parts[2] if len(parts) > 2 else "1"

    # هنا يتم استدعاء دالة البحث المباشر
    # (يمكن استخدام API خاص بمعلومات IMDb للحصول على الاسم العربي/التركي للمسلسل أولاً)
    streams = fetch_real_streams(imdb_id, season, episode)

    return Response(json.dumps({"streams": streams}, ensure_ascii=False), mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
