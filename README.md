# 🚀 RSS Telegram Auto-News Poster Bot

An automated Python-based Telegram bot that fetches the latest news from top Crypto, Market, and On-Chain RSS feeds and posts them directly to your Telegram Channel with custom cover images and hyperlinks.

Powered by **GitHub Actions**, it runs 100% free in the cloud without needing any external VPS or hosting server.

---

## ✨ Features

- 🔄 **Fully Automated:** Periodically checks RSS feeds (every 10–15 mins).
- 🖼️ **Image Auto-Scraping:** Fetches article cover images via Open Graph (`og:image`) tags.
- 🔗 **Clean Hyperlinks:** Formats post titles with direct news links to keep posts sleek.
- 💾 **Duplicate Prevention:** Tracks posted links in `posted.json` to prevent re-posting.
- ☁️ **Serverless:** Runs entirely on GitHub Actions for $0/month.

---

## 🛠️ Setup Instructions

Follow these step-by-step instructions to set up your own bot instance:

### Step 1: Fork or Clone this Repository
Click the **Fork** button at the top right of this page to copy this project to your GitHub account.

---

### Step 2: Create a Telegram Bot & Get IDs
1. Open Telegram and search for [@BotFather](https://t.me/BotFather).
2. Send `/newbot` and follow the prompts to create your bot.
3. Save the **API BOT TOKEN** provided by BotFather.
4. Add your newly created bot to your Telegram Channel as an **Admin** with **Post Messages** permissions.
5. Get your Channel ID (e.g., `@yourchannelusername` or `-100xxxxxxxxx`).

---

### Step 3: Configure GitHub Secrets
To keep your credentials secure, add them to your repository secrets:

1. Go to your GitHub Repository -> **Settings** -> **Secrets and variables** -> **Actions**.
2. Click **New repository secret** and add the following two secrets:

| Secret Name | Description / Value |
| :--- | :--- |
| `BOT_TOKEN` | Your Telegram Bot Token from BotFather |
| `CHANNEL_ID` | Your Telegram Channel Username (e.g., `@hiddengemnews`) or ID |

---

### Step 4: Enable GitHub Actions Permissions
1. Go to **Settings** -> **Actions** -> **General**.
2. Scroll down to **Workflow permissions**.
3. Select **Read and write permissions**.
4. Click **Save**.

---

### Step 5: Test and Run
1. Go to the **Actions** tab in your repository.
2. Click on **RSS Telegram Feeder** on the left menu.
3. Click **Run workflow** -> Select `main` branch -> Click the green **Run workflow** button.

Once triggered successfully, the bot will run automatically in the background on schedule!

---

## ⚙️ Customization

### Adding / Removing RSS Feeds
To change news sources, open `bot.py` and modify the `RSS_FEEDS` list:

```python
RSS_FEEDS = [
    "[https://cointelegraph.com/rss](https://cointelegraph.com/rss)",
    "[https://decrypt.co/feed](https://decrypt.co/feed)",
    "[https://bitcoinmagazine.com/feed](https://bitcoinmagazine.com/feed)"
]
