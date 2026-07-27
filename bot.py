import os
import json
import asyncio
import feedparser
import requests
from bs4 import BeautifulSoup
from telegram import Bot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
POSTED_FILE = "posted.json"

# আপনি যেসব RSS ফিড চালাতে চান তার লিস্ট
RSS_FEEDS = [
    # Top Crypto & Market News
    "https://cointelegraph.com/rss",
    "https://decrypt.co/feed",
    "https://bitcoinmagazine.com/feed",
    "https://cryptoslate.com/feed/",
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    
    # Altcoin & On-Chain Analysis
    "https://beincrypto.com/feed/",
    "https://news.bitcoin.com/feed/",
    "https://blockworks.co/feed"
]

def load_posted():
    if os.path.exists(POSTED_FILE):
        with open(POSTED_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_posted(posted_list):
    # সর্বশেষ ১০০টি লিংক সেভ রাখা হবে
    with open(POSTED_FILE, "w") as f:
        json.dump(posted_list[-100:], f, indent=2)

async def main():
    bot = Bot(token=BOT_TOKEN)
    posted_links = load_posted()
    new_posted = list(posted_links)

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        # সবচেয়ে পুরনোটি আগে পোস্ট করার জন্য রিভার্স
        for entry in reversed(feed.entries[:5]):
            link = entry.link
            if link in new_posted:
                continue

            title = entry.title
            
            # মেটা ট্যাগ থেকে কভার ইমেজ ফেচ করা
            image_url = None
            try:
                res = requests.get(link, timeout=5)
                soup = BeautifulSoup(res.text, 'html.parser')
                og_img = soup.find("meta", property="og:image")
                if og_img and og_img.get("content"):
                    image_url = og_img["content"]
            except Exception as e:
                pass

            # হাইপারলিঙ্ক ফরম্যাটে ক্যাপশন
caption = (
            f"<a href='{link}'>{title}</a>\n\n"
            f"<b>Subscribe - @hiddengemnews</b>\n"
            f"<i>Powered by Hidden Gem</i>"
        )

        try:
            if image_url:
                await bot.send_photo(
                    chat_id=CHANNEL_ID,
                    photo=image_url,
                    caption=caption,
                    parse_mode="HTML"
                )
            else:
                await bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=caption,
                    parse_mode="HTML"
                )
            print(f"Posted: {title}")
            new_posted.append(link)
            await asyncio.sleep(2)
        except Exception as e:
            print(f"Error posting {title}: {e}")
