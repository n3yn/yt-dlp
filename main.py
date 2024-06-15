from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import urllib.parse
import requests
import bs4
import re

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    # Get the query from the client
    query = request.form.get('query')
    
    # Encode the query for the URL
    query = urllib.parse.quote(query)
    
    # Set the base domain
    domain = 'https://www.melon365.com'
    
    # Construct the search URL
    url = domain + '/video/search?sk=' + query
    
    # Make the request and parse the HTML
    res = requests.get(url)
    r = bs4.BeautifulSoup(res.text, "html.parser")

    pattern = r'\n\t+([^\n]+)\n\t+'
    
    # Extract the titles and URLs
    m_titles = []
    m_urls = []
    content_div = r.find_all('div', class_='newslistsearchtextrighttitle')
    a_tags = r.find_all('a', class_='reglink12 expand')
    for content in content_div:
        a = content.find('a')
        m_urls.append(domain + a.get('href').split('.html')[0] + '.html')
        match = re.search(pattern, content.text)
        m_titles.append(match.group(1).strip())
    page_num = 0
    for tag in a_tags:
    	text = tag.get_text(strip=True)
    	if text.isdigit():
    		number = int(text)
    		if number > page_num:
    			page_num = number
    return jsonify({'m_titles': m_titles, 'm_urls': m_urls, 'page_num': page_num})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
