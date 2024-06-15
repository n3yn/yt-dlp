from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import urllib.parse
import requests

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query')

    if not query:
        return jsonify({'error': 'No query provided'}), 400

    m_titles = []
    m_urls = []

    try:
        encoded_query = urllib.parse.quote(query)
        domain = 'https://www.melon365.com'
        url = domain + '/video/search?sk=' + encoded_query
        res = requests.get(url)
        res.raise_for_status()
        
        r = BeautifulSoup(res.text, "html.parser")

        content_div = r.find_all('div', class_='newslistsearchtextrighttitle')
        for content in content_div:
            a = content.find('a')
            m_urls.append(domain + a.get('href').split('.html')[0] + '.html')
            m_titles.append(content.text.replace('\n', '').replace('\t', ''))

        return jsonify({'titles': m_titles, 'urls': m_urls})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
