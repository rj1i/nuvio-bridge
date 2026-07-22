import json
from urllib.parse import quote
from flask import Flask, Response, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
@app.route('/manifest.json')
def manifest():
    data = {
        'id': 'com.arabic.specific.servers',
        'version': '2.2.0',
        'name': 'السيرفرات العربية (قرمزي & قصة عشق)',
        'description': 'جلب سيرفرات رامو، قطاع الطرق، وتحت الأرض بدقة',
        'resources': ['stream'],
        'types': ['series', 'movie'],
        'idPrefixes': ['tt'],
    }
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')

@app.route('/stream/<type>/<id>.json')
def stream(type, id):
    parts = id.split(':')
    imdb_id = parts[0]
    season = parts[1] if len(parts) > 1 else '1'
    episode = parts[2] if len(parts) > 2 else '1'

    all_streams = []

    # ربط معرفات الـ IMDb بالأسماء الصحيحة لكل موقع
    shows_database = {
        'tt39222526': {
            'title': 'تحت الأرض',
            'krmizi_slug': 'مسلسل-تحت-الأرض',
            ' عشق_slug': 'تحت-الأرض'
        },
        'tt5175270': {
            'title': 'قطاع الطرق لن يحكموا العالم',
            'krmizi_slug': 'مسلسل-قطاع-الطرق',
            'عشق_slug': 'قطاع-الطرق-لن-يحكموا-العالم'
        },
        'tt11051886': {
            'title': 'رامو (Ramo)',
            'krmizi_slug': 'مسلسل-رامو',
            'عشق_slug': 'رامو'
        }
    }

    if imdb_id in shows_database:
        show = shows_database[imdb_id]
        show_title = show['title']
        krmizi_slug = show['krmizi_slug']
        
        # 1. رابط موقع قرمزي
        krmizi_url = f"https://krmizi.onl/episode/{krmizi_slug}-الحلقة-{episode}/"
        
        # 2. رابط موقع قصة عشق (بالصيغة المباشرة للصفحة)
        asq_url = f"https://3s9q.net/series/{quote(show_title)}/episode-{episode}"

        all_streams.append({
            'name': f'🎬 {show_title} | قرمزي (Krmizi)',
            'title': f'الحلقة {episode} - صفحة السيرفرات',
            'url': krmizi_url
        })
        
        all_streams.append({
            'name': f'❤️ {show_title} | قصة عشق (3s9q)',
            'title': f'الحلقة {episode} - المشاهدة المباشرة',
            'url': asq_url
        })

    return Response(
        json.dumps({'streams': all_streams}, ensure_ascii=False),
        mimetype='application/json',
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
