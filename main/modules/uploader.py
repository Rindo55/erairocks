import asyncio
import os
import time
import aiohttp
import requests
import aiofiles

from main.modules.utils import format_time, get_duration, get_epnum, get_filesize, status_text, tags_generator

from main.modules.anilist import get_anime_name

from main.modules.anilist import get_anime_img

from main.modules.thumbnail import generate_thumbnail

from config import UPLOADS_ID

from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from main.modules.progress import progress_for_pyrogram

from os.path import isfile

import os

import time

from main import app, status

from pyrogram.errors import FloodWait

from main.inline import button1

async def upload_video(msg: Message,file,id,tit,name,ttl,subtitle):

    try:

        fuk = isfile(file)

        if fuk:

            r = msg

            c_time = time.time()

            duration = get_duration(file)

            size = get_filesize(file)

            ep_num = get_epnum(name)
            
            rest = tit

            thumbnail = await generate_thumbnail(id,file)

            tags = tags_generator(tit)

            buttons = InlineKeyboardMarkup([

                [

                    InlineKeyboardButton(text="Info", url="https://t.me/AnimeXT"),

                    InlineKeyboardButton(text="Comments", url=f"https://t.me/ANIMECHATTERBOX")

                ]

            ])
            filed = os.path.basename(file)
            filed = filed.replace("[1080p Web-DL]", "[720p x265] @animxt")
            fukpath = "downloads/" + filed
            caption = f"{filed}"
            caption = caption.replace("[720p x265] @animxt.mkv", "") 
            gcaption=f"**{caption}**" + "\n" +  f"__({tit})__" + "\n" + "━━━━━━━━━━━━━━━━━━━" + "\n" + "✓  `720p x265 10Bit`" + "\n" + f"✓  `{subtitle} ~ Subs`" + "\n" + "#Encoded #HEVC"
            kayo_id = -1001159872623
            x = await app.send_document(

                kayo_id,

            document=file,

            caption=gcaption,

            file_name=filed,

            force_document=True,
                
            thumb=thumbnail
            ) 
        os.rename(file,fukpath)
        files = {'file': open(fukpath, 'rb')}
        nanix = await x.edit(gcaption + "\n" "━━━━━━━━━━━━━━━━━━━" + "\n" + "Generating Link", parse_mode = "markdown")
        callapi = requests.post("https://api.filechan.org/upload", files=files)
        text = callapi.json()
        long_url = text['data']['file']['url']['full']
        api_url = f"https://flashlink.in/api?api=aafa2d36a38398631679a74769a071b2154e08e7&url={long_url}&format=text"
        result = requests.get(api_url)
        nai_text = result.text
        da_url = "https://da.gd/"
        url = nai_text
        shorten_url = f"{da_url}shorten"
        response = requests.get(shorten_url, params={"url": url})
        nyaa_text = response.text.strip()                                     
        await asyncio.sleep(6)
        server = requests.get(url="https://api.gofile.io/getServer").json()["data"]["server"]
        uploadxz = requests.post(url=f"https://{server}.gofile.io/uploadFile", files={"upload_file": open(fukpath, 'rb')}).json()
        directlink = uploadxz["data"]["downloadPage"]    
        gotn_url = f"https://flashlink.in/api?api=aafa2d36a38398631679a74769a071b2154e08e7&url={directlink}&format=text"
        gofinal = requests.get(gotn_url)
        go_text = gofinal.text
        gourl = go_text
        gofile_url = f"{da_url}shorten"
        goresponse = requests.get(gofile_url, params={"url": gourl})
        gofuk_text = goresponse.text.strip()
        await asyncio.sleep(6)
        krakenapi = requests.get(url="https://krakenfiles.com/api/server/available").json()
        krakenxurl = krakenapi['data']['url']
        krakentoken = krakenapi['data']['serverAccessToken']
        params = {'serverAccessToken': krakentoken} 
        krakenupload = requests.post(krakenxurl, files={'file': open(fukpath, 'rb')}, data=params).json()
        krakenlink = krakenupload['data']['url']
        krtn_url = f"https://flashlink.in/api?api=aafa2d36a38398631679a74769a071b2154e08e7&url={krakenlink}&format=text"
        krfinal = requests.get(krtn_url)
        kr_text = krfinal.text
        krurl = kr_text
        krfile_url = f"{da_url}shorten"
        krresponse = requests.get(krfile_url, params={"url": krurl})
        krfuk_text = krresponse.text.strip()
        output = f"""
{gcaption}
━━━━━━━━━━━━━━━━━━━
**External Download Links**
[Filechan]({nyaa_text}) | [Gofile]({gofuk_text}) | [KrakenFiles]({krfuk_text})"""
        daze = await x.edit(output, parse_mode = "markdown")               
    except Exception:
       await app.send_message(message.chat.id, text="Something Went Wrong!")
    try:

            await r.delete()

            os.remove(file)
            
            os.remove(fukpath)

            os.remove(thumbnail)

    except:

        pass

    return x.message_id
