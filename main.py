from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import urllib.parse
import requests
import bs4
import re
import logging

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    try:
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
        
        # Extract the titles and URLs
        m_titles = []
        m_urls = []
        content_div = r.find_all('div', class_='newslistsearchtextrighttitle')
        for content in content_div:
            a = content.find('a')
            if a:
                m_urls.append(domain + a.get('href').split('.html')[0] + '.html')
                ttt = content.text.replace('\n', '').replace('\t', '')
                pattern = r"\(音\) (\w+)\("
                matches = re.findall(pattern, ttt)
                if matches:
                    mtitle = matches[0]
                    m_titles.append(mtitle)
        
        # Return the results as JSON
        return jsonify({'m_titles': m_titles, 'm_urls': m_urls})
    
    except Exception as e:
        logging.error(f"Error occurred during search: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
