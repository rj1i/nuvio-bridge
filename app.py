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
        'version': '2.0.0',
        'name': 'السيرفرات العربية للمسلسلات التركية المخصصة',
        'description': 'جلب سيرفرات رامو، قطاع الطرق، وتحت الأرض بدقة تامة',
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

    # قاعدة بيانات دقيقة تربط كل رقم IMDb بمسلسله واسمه الصحيح في المواقع العربية
    shows_database = {
        'tt39222526': {
            'title': 'تحت الأرض',
            'slug': 'تحت-الأرض'
        },
        'tt5175270': {
            'title': 'قطاع الطرق لن يحكموا العالم',
            'slug': 'قطاع-الطرق-لن-يحكموا-العالم'
        },
        'tt11051886': {
            'title': 'رامو (Ramo)',
            'slug': 'رامو'
        }
    }

    # التحقق مما إذا كان المسلسل المطلوب موجوداً في قائمتنا المخصصة
    if imdb_id in shows_database:
        show = shows_database[imdb_id]
        show_title = show['title']
        show_slug = show['slug']

        # تجهيز السيرفرات الخاصة بهذا المسلسل فقط
        servers_list = [
            ("المشغل الأول - Arab HD", f"https://krmizi.com/watch/{show_slug}-الحلقة-{episode}-arab-hd"),
            ("المشغل الثاني - Turk", f"https://krmizi.com/watch/{show_slug}-الحلقة-{episode}-turk"),
            ("المشغل الثالث - Dally", f"https://krmizi.com/watch/{show_slug}-الحلقة-{episode}-dally"),
            ("قصة عشق - سيرفر رئيسي", f"https://3s9q.net/series/{show_slug}/episode-{episode}")
        ]

        for s_name, s_url in servers_list:
            all_streams.append({
                'name': f'🎬 {show_title} | {s_name}',
                'title': f'الحلقة {episode} - مشاهدة مباشرة',
                'url': s_url
            })

    return Response(
        json.dumps({'streams': all_streams}, ensure_ascii=False),
        mimetype='application/json',
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
