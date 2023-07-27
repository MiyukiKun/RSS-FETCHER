import asyncio
from config import bot, database_channel
from mongo import RssDB
import requests
from bs4 import BeautifulSoup
from coindesk_formating import get_article
from telethon.errors.rpcerrorlist import MediaCaptionTooLongError

RssDB = RssDB()

loop = asyncio.get_event_loop()

async def read_rss():
    while True:
        url = "https://www.coindesk.com/arc/outboundfeeds/rss/"

        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'xml').find_all("item")[::-1]
        for i in soup:
            aid = i.find("guid").text
            if RssDB.find({"_id": aid}) == None:
                data = await get_article(i)
                image = data["image"]
                headline = data["headline"]
                subheadline = data["subheadline"]
                creator = data["creator"]
                pub_date = data["pub_date"]
                text_data = data["text_data"]
                tags = data["tags"]
                article_url = data["url"]
                category = data["category"]

                try:
                    await bot.send_message(database_channel, f"**{headline}**\n\nTopics: `{tags}`\n\n{subheadline}\n\n{text_data}\n[Read more]({article_url})\n\n{category} By: {creator}\n{pub_date}\n\nJoin @Crypto_Current_Affairs to receive latest updates", file=image, force_document=False)
                except MediaCaptionTooLongError:
                    await bot.send_message(database_channel, f"**{headline}**\n\nTopics: `{tags}`\n\n{subheadline}\n\n{text_data[:100]}...\n[Read more]({article_url})\n\n{category} By: {creator}\n{pub_date}\n\nJoin @Crypto_Current_Affairs to receive latest updates", file=image, force_document=False)


                RssDB.add({"_id": aid})
            else:
                pass
        await asyncio.sleep(900)


loop.run_until_complete(read_rss())

bot.start()

bot.run_until_disconnected()