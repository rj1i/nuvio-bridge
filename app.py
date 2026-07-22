from flask import Flask, jsonify
import feedparser
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

SOURCES = {
    "qesset": "https://qesset.net/feed/",
    "krmizi": "https://krmizi.onl/feed/"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://qesset.net/"
}

@app.route('/')
def home():
    return jsonify({"message": "Server is running successfully!"})

@app.route('/episodes/<source>')
def get_episodes(source):
    if source not in SOURCES:
        return jsonify({"error": "المصدر غير موجود"}), 404
        
    feed = feedparser.parse(SOURCES[source])
    data = []
    
    for entry in feed.entries[:10]:
        try:
            res = requests.get(entry.link, headers=HEADERS, timeout=5)
            soup = BeautifulSoup(res.text, 'html.parser')
            iframes = [i.get('src') for i in soup.find_all('iframe') if i.get('src')]
            
            data.append({
                "title": entry.title,
                "url": entry.link,
                "streams": iframes
            })
        except:
            continue
            
    return jsonify({"status": "ok", "source": source, "episodes": data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
