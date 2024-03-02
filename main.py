from flask import Flask, request, jsonify, render_template
from yt_dlp import YoutubeDL

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert_url', methods=['POST'])
def convert_url():
    data = request.get_json()
    url = data['url']
    
    ydl_opts = {
        "quiet":    True,
        "simulate": True,
        "forceurl": True,
        'format': 'best'
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
        url2 = info["url"]
    
    return jsonify({'url2': url2})

if __name__ == '__main__':
    app.run(debug=True)
