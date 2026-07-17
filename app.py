import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt-dlp

app = Flask(__name__)
CORS(app) # यह ब्लॉगर से आने वाली रिक्वेस्ट्स को अलाउ करेगा

@app.route('/')
def home():
    return "YouTube Downloader API is running successfully!"

@app.route('/get-download-link', methods=['POST'])
def get_download_link():
    data = request.get_json()
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({'error': 'कृपया एक वैध YouTube URL डालें!'}), 400

    ydl_opts = {
        'format': 'best', 
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt-dlp.YoutubeDL(ydl_opts) as ydl:
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
    # Render के लिए पोर्ट सेटिंग्स
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)