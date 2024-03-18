import requests
from json import loads
from flask import Flask, jsonify
app = Flask(__name__)

url = "https://web.dev/_d/dynamic_content"


@app.route('/blog', methods=['GET'])
def scrape_dynamic_blog():
    headers = {
        "Content-Type": "text/plain;charset=UTF-8",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en;q=0.8",
        "Cookie": "_ga_devsite=GA1.2.737878519.1698001498; cookies_accepted=true; django_language=en",
        "Origin": "https://web.dev",
        "Referer": "https://web.dev/blog",
        "Sec-Ch-Ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Brave\";v=\"122\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Gpc": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    data = [
        None,
        None,
        None,
        "type:blog",
        None,
        None,
        None,
        None,
        31,
        None,
        None,
        None,
        2
    ]
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        if response.status_code == 200:
            textData = response.text
            scraped_data = []
            textData = textData.lstrip(")]}'\n ")
            json_data = loads(textData)
            for post in json_data[0]:
                time_as_key = post[5][0]
                title = post[0]
                paragraph = post[4]
                link = post[6]
                image = post[3]

                scraped_data.append({
                    "time_as_key": time_as_key,
                    "title": title,
                    "paragraph": paragraph,
                    "link": link,
                    "image_url": image
                })
            return jsonify(scraped_data)
        else:
            return jsonify({"error": "Unexpected status code", "status_code": response.status_code}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error occurred while scraping: {e}"}), 500


@app.route('/articles', methods=['GET'])
def scrape_dynamic_articles():
    articles_headers = {
        "Content-Type": "text/plain;charset=UTF-8",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en;q=0.8",
        "Cookie": "_ga_devsite=GA1.2.737878519.1698001498; cookies_accepted=true; django_language=en",
        "Origin": "https://web.dev",
        "Referer": "https://web.dev/articles",
        "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Gpc": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    articles_data = [
        None,
        None,
        None,
        "family_url:/articles",
        None,
        None,
        None,
        None,
        501,
        None,
        None,
        None,
        2
    ]
    try:
        response = requests.post(
            url, headers=articles_headers, json=articles_data)
        response.raise_for_status()
        if response.status_code == 200:
            textData = response.text
            scraped_data = []
            textData = textData.lstrip(")]}'\n ")
            json_data = loads(textData)
            for post in json_data[0]:
                time_as_key = post[5][0]
                title = post[0]
                paragraph = post[4]
                link = post[6]
                image = post[3]

                scraped_data.append({
                    "time_as_key": time_as_key,
                    "title": title,
                    "paragraph": paragraph,
                    "link": link,
                    "image_url": image
                })
            return jsonify(scraped_data)
        else:
            return jsonify({"error": "Unexpected status code", "status_code": response.status_code}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error occurred while scraping: {e}"}), 500


@app.route('/')
def home():
    return jsonify({
        "msg": "API For Scraping web.dev Articles and Blogs, join to channel telegram to get updates on the web.dev site :)",
        "Telegram Channel": "https://t.me/webdev_m05",
        "Blogs": "/blog",
        "Articles": "/articles",
        "developer": "Mahmoud",
        "GitHuub": "https://github.com/M0mahmoud",
        "Telegram": "https://t.me/dev_mahmoud_05",
    })
