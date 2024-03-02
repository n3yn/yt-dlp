from yt_dlp import YoutubeDL
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	url = None
	if request.method == 'POST':
		url = request.form['url']
		ydl_opts = {
			"quiet":    True,
			"simulate": True,
			"forceurl": True,
			'format': 'best'
		}
	with YoutubeDL(ydl_opts) as ydl:
		info = ydl.extract_info(url)
		url = info["url"]
  return render_template('index.html', url=url)

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
