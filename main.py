from flask import Flask, render_template, request, jsonify
from yt_dlp import YoutubeDL


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_url():
    data = request.json
    url = data['url']
    ydl_opts = {
        "cookiefile": "twcookies.txt",
		"quiet": True,
		"simulate": True,
		"forceurl": True,
		'format': 'best'
	}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
        r = info["url"]
    converted_url = r
    return jsonify({'converted_url': converted_url})

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
