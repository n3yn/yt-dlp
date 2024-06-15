from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import urllib.parse
import requests
import bs4

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    # Get the query from the client
    query = request.form['query']
    
    # Encode the query for the URL
    query = urllib.parse.quote(query)
    
    # Set the base domain
    domain = 'https://www.melon365.com'
    
    # Construct the search URL
    url = domain + '/video/search?sk=' + query
    
    # Make the request and parse the HTML
    res = requests.get(url)
    r = bs4.BeautifulSoup(res.text, "html.parser")
    
    # Extract the titles and URLs
    m_titles = []
    m_urls = []
    content_div = r.find_all('div', class_='newslistsearchtextrighttitle')
    for content in content_div:
        a = content.find('a')
        m_urls.append(domain + a.get('href').split('.html')[0] + '.html')
        m_titles.append(content.text.replace('\n', '').replace('\t', ''))
    
    # Return the results as JSON
    return jsonify({'m_titles': m_titles, 'm_urls': m_urls})

if __name__ == '__main__':
    app.run(debug=True)
