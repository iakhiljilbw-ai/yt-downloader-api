import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "YouTube Downloader API is running with Cookies!"

@app.route('/get-download-link', methods=['POST'])
def get_download_link():
    if not request.is_json:
        return jsonify({'error': 'डेटा JSON फॉर्मेट में होना चाहिए!'}), 400
        
    data = request.get_json()
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({'error': 'कृपया एक वैध YouTube URL डालें!'}), 400

    # कुकीज़ फ़ाइल का सही पाथ सेट करना
    cookies_path = os.path.join(os.path.dirname(__file__), 'cookies.txt')

    ydl_opts = {
        'format': 'best', 
        'quiet': True,
        'no_warnings': True,
    }

    # अगर कुकी फ़ाइल मौजूद है, तो उसे लागू करें
    if os.path.exists(cookies_path):
        ydl_opts['cookiefile'] = cookies_path

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get('url')
            title = info.get('title')
            thumbnail = info.get('thumbnail')

            return jsonify({
                'success': True,
                'title': title,
                'download_url': download_url,
                'thumbnail': thumbnail
            })
            
    except Exception as e:
        return jsonify({'error': f'लिंक प्रोसेस करने में दिक्कत आई: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
