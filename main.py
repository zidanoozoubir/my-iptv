import base64
from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "IPTV Proxy Server is Running Perfectly!"

@app.route('/play')
def play():
    # جلب الرابط المشفر الممرر عبر الـ URL
    encoded_url = request.args.get('url', '')
    if not encoded_url:
        return "رابط القناة غير موجود.", 400
    
    try:
        # فك تشفير الرابط
        live_url = base64.b64decode(encoded_url).decode('utf-8')
    except Exception:
        return "خطأ في قراءة الرابط.", 400

    # إعداد الحماية المطلوبة لتخطي المنع
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "Referer": "https://x.com/"
    }

    # جلب البث وتمريره مباشرة للريسيفر (Streaming)
    def generate():
        with requests.get(live_url, headers=headers, stream=True, timeout=10) as r:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    yield chunk

    return Response(generate(), content_type="application/vnd.apple.mpegurl")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
