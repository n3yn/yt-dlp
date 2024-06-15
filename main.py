from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import urllib.parse
import requests

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    query = urllib.parse.quote(query)
    domain = 'https://www.melon365.com'
    url = f"{domain}/video/search?sk={query}"
    
    res = requests.get(url)
    r = BeautifulSoup(res.text, "html.parser")
    
    m_titles = []
    m_urls = []

    content_div = r.find_all('div', class_='newslistsearchtextrighttitle')
    for content in content_div:
        a = content.find('a')
        if a:
            m_urls.append(domain + a.get('href').split('.html')[0] + '.html')
            m_titles.append(a.text.replace('\n', '').replace('\t', ''))

    return jsonify({"titles": m_titles, "urls": m_urls})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
