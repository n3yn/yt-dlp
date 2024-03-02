function convertUrl() {
    var url = document.getElementById('urlInput').value;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/convert_url', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            document.getElementById('url2Display').innerHTML = "<p>URL2: " + response.url2 + "</p>";
        }
    };
    xhr.send(JSON.stringify({url: url}));
}

document.getElementById('submitButton').addEventListener('click', convertUrl);
