import json
from urllib.parse import quote
from flask import Flask, Response, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
        ' like Gecko) Chrome/122.0.0.0 Safari/537.36'
    ),
    'Accept-Language': 'ar,en-US;q=0.9,en;q=0.8',
}


# 1. دالة جلب اسم المسلسل من المعرف (Cinemeta ثم TMDB كبديل)
def get_series_title(imdb_id):
    # محاولة جلب الاسم من Cinemeta
    try:
        url = f'https://v3-cinemeta.strem.fun/meta/series/{imdb_id}.json'
        res = requests.get(url, headers=HEADERS, timeout=5)
        if res.status_code == 200:
            name = res.json().get('meta', {}).get('name', '')
            if name:
                return name
    except Exception as e:
        print(f'Cinemeta Error: {e}')

    # محاولة جلب الاسم بالعربي من TMDB
    try:
        tmdb_url = f'https://api.themoviedb.org/3/find/{imdb_id}?api_key=15d2aea6d22616440e08306727222858&external_source=imdb_id&language=ar'
        res = requests.get(tmdb_url, headers=HEADERS, timeout=5)
        if res.status_code == 200:
            results = res.json().get('tv_results', [])
            if results:
                return results[0].get('name') or results[0].get('original_name', '')
    except Exception as e:
        print(f'TMDB Error: {e}')

    return ''


# 2. دالة البحث في موقع قصة عشق
def scrape_qesset(title, episode):
    streams = []
    if not title:
        return streams
    try:
        search_query = quote(f'{title} حلقة {episode}')
        search_url = f'https://3s9q.net/?s={search_query}'

        res = requests.get(search_url, headers=HEADERS, timeout=5)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            articles = soup.find_all('article')
            for art in articles[:3]:
                link_tag = art.find('a')
                if link_tag and 'href' in link_tag.attrs:
                    ep_url = link_tag['href']
                    ep_res = requests.get(ep_url, headers=HEADERS, timeout=5)
                    ep_soup = BeautifulSoup(ep_res.text, 'html.parser')

                    iframes = ep_soup.find_all('iframe')
                    for idx, iframe in enumerate(iframes, start=1):
                        src = iframe.get('src', '')
                        if src and 'http' in src:
                            streams.append({
                                'name': f'قصة عشق #{idx}',
                                'title': f'🎬 قصة عشق | {title} - حلقة {episode} (سيرفر {idx})',
                                'url': src,
                            })
    except Exception as e:
        print(f'Qesset Scrape Error: {e}')
    return streams


# 3. دالة البحث في موقع قرمزي
def scrape_krmizi(title, episode):
    streams = []
    if not title:
        return streams
    try:
        search_query = quote(f'{title} حلقة {episode}')
        search_url = f'https://krmizi.com/?s={search_query}'

        res = requests.get(search_url, headers=HEADERS, timeout=5)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            articles = soup.find_all('article')
            for art in articles[:3]:
                link_tag = art.find('a')
                if link_tag and 'href' in link_tag.attrs:
                    ep_url = link_tag['href']
                    ep_res = requests.get(ep_url, headers=HEADERS, timeout=5)
                    ep_soup = BeautifulSoup(ep_res.text, 'html.parser')

                    iframes = ep_soup.find_all('iframe')
                    for idx, iframe in enumerate(iframes, start=1):
                        src = iframe.get('src', '')
                        if src and 'http' in src:
                            streams.append({
                                'name': f'قرمزي #{idx}',
                                'title': f'🎬 قرمزي | {title} - حلقة {episode} (سيرفر {idx})',
                                'url': src,
                            })
    except Exception as e:
        print(f'Krmizi Scrape Error: {e}')
    return streams


@app.route('/')
@app.route('/manifest.json')
def manifest():
    data = {
        'id': 'com.arabic.servers.bridge',
        'version': '1.3.0',
        'name': 'السيرفرات العربية (قصة عشق & قرمزي)',
        'description': 'جلب سيرفرات المشاهدة المباشرة للمسلسلات',
        'resources': ['stream'],
        'types': ['series', 'movie'],
        'idPrefixes': ['tt'],
    }
    return Response(
        json.dumps(data, ensure_ascii=False), mimetype='application/json'
    )


@app.route('/stream/<type>/<id>.json')
def stream(type, id):
    parts = id.split(':')
    imdb_id = parts[0]
    season = parts[1] if len(parts) > 1 else '1'
    episode = parts[2] if len(parts) > 2 else '1'

    # جلب عنوان المسلسل
    series_title = get_series_title(imdb_id)

    all_streams = []
    if series_title:
        qesset_streams = scrape_qesset(series_title, episode)
        krmizi_streams = scrape_krmizi(series_title, episode)
        all_streams = qesset_streams + krmizi_streams

    # إرجاع السيرفرات المتوفرة (أو قائمة فارغة في حال عدم العثور على نتائج)
    return Response(
        json.dumps({'streams': all_streams}, ensure_ascii=False),
        mimetype='application/json',
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
