import os
import json
import asyncio
import feedparser
import requests
from bs4 import BeautifulSoup
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
POSTED_FILE = "posted.json"

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
        try:
            with open(POSTED_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_posted(posted_links):
    with open(POSTED_FILE, "w") as f:
        json.dump(posted_links, f, indent=4)

def get_image_from_url(link):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(link, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            return og_image['content']
    except Exception:
        pass
    return None

async def main():
    if not BOT_TOKEN or not CHANNEL_ID:
        print("Missing BOT_TOKEN or CHANNEL_ID")
        return

    bot = Bot(token=BOT_TOKEN)
    posted_links = load_posted()
    new_posted = list(posted_links)

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:
            link = entry.link
            title = entry.title

            if link in posted_links:
                continue

            image_url = get_image_from_url(link)

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

    save_posted(new_posted)

if __name__ == "__main__":
    asyncio.run(main())
