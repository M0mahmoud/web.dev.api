# https://t.me/webdev_m05
import os
import requests
from telegram import Bot
from flask import Flask
from dotenv import load_dotenv
import asyncio
import pickle
from keep_alive import keep_alive

app = Flask(__name__)
keep_alive()
load_dotenv()


token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')
bot = Bot(token)

API_URL = 'https://web-dev-api-05.vercel.app/'
DATA_FILE = 'WebDevFile.pkl'
CHECK_INTERVAL = 3 * 60 * 60


def get_api_data(endpoint):
    try:
        url = API_URL + endpoint
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(
                f"Failed to fetch data from {endpoint}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching data from {endpoint}: {e}")
        return None


def load_data():
    try:
        with open(DATA_FILE, 'rb') as f:
            return set(pickle.load(f))
    except FileNotFoundError:
        return set()


def save_data(data):
    with open(DATA_FILE, 'wb') as f:
        pickle.dump(list(data), f)


async def send_message(bot, chat_id, text, blog_data):
    try:
        title = blog_data['title']
        paragraph = blog_data['paragraph']
        link = blog_data['link']
        image_url = blog_data['image_url']
        html_message = f'<b><a href="{link}">{title}</a></b>\n<b>{text}</b>\n\n{paragraph}'

        await bot.send_photo(chat_id, photo=image_url,
                             caption=html_message, parse_mode='HTML')
        print("Message sent successfully")
    except Exception as e:
        print("Failed to send message:", e)


async def main():
    last_data = load_data()

    while True:
        print(last_data)
        blog_data = get_api_data('/blog')
        articles_data = get_api_data('/articles')
        if blog_data:
            for item in blog_data:
                key = item.get('time_as_key')
                if key and key not in last_data:
                    last_data.add(key)
                    await send_message(bot, chat_id,  "New blog", item)

        if articles_data:
            for item in articles_data:
                key = item.get('time_as_key')
                if key and key not in last_data:
                    last_data.add(key)
                    await send_message(bot, chat_id,  "New Article", item)

        save_data(last_data)
        print('--------------new check--------------')
        await asyncio.sleep(CHECK_INTERVAL)


if __name__ == '__main__':
    asyncio.run(main())
    app.run(debug=True)
