import asyncio

import feedparser

from main import status, queue

from main.inline import button1

from main.modules.db import get_animesdb, get_uploads, save_animedb

from main.modules.schedule import update_schedule

from main.modules.usschedule import update_schedulex

from main.modules.utils import status_text

def trim_title(title: str):

    title, ext = title.replace("[Magnet]", "").strip().split("[", maxsplit=2)

    _, ext = ext.split("]", maxsplit=2)

    title = title.strip() + ext

    return title

async def parse():

    url = "https://www.erai-raws.info/episodes/feed/?res=1080p&type=magnet&0879fd62733b8db8535eb1be24e23f6d"

    a = feedparser.parse(url)

    entries = a.get("entries", [])[:10]

    data = []

    for entry in entries:

        title = trim_title(entry.get("title", ""))

        link = entry.get("link", "")

        size = entry.get("erai_size", "")

        if ".mkv" in title or ".mp4" in title:

            data.append({"title": title, "link": link, "size": size})

    return data

async def auto_parser():

    while True:

        try:

            await status.edit(await status_text("Parsing Rss, Fetching Magnet Links..."), reply_markup=button1)

        except:

            pass

        rss = await parse()

        saved_anime = {anime["name"] for anime in await get_animesdb()}

        uanimes = {anime["name"] for anime in await get_uploads()}

        for entry in rss:

            title = entry["title"]

            if title not in uanimes and title not in saved_anime:

                await save_animedb(title, entry)

                saved_anime.add(title)

        for anime in await get_animesdb():

            if anime["data"] not in queue:

                queue.append(anime["data"])

                print("Saved", anime["name"])

        try:

            await status.edit(await status_text("Idle..."), reply_markup=button1)

            await update_schedule()

            await asyncio.sleep(6)

            await update_schedulex()

        except:

            pass

        await asyncio.sleep(30)
