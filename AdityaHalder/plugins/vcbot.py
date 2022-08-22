import re
import asyncio
from AdityaHalder.modules.cache.admins import admins
from AdityaHalder.modules.helpers.filters import command
from AdityaHalder.utilities.utils import bash, skip_current_song, skip_item
from AdityaHalder.modules.clientbot.queues import QUEUE, add_to_queue, clear_queue
from AdityaHalder.modules.clientbot import client as app, pytgcalls as aditya
from AdityaHalder.modules.helpers.decorators import sudo_users_only
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch
from AdityaHalder.utilities.misc import SUDOERS


def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        return [songname, url]
    except Exception as e:
        print(e)
        return 0

async def ytdl(link: str):
    stdout, stderr = await bash(
        f'yt-dlp -g -f "best[height<=?720][width<=?1280]" {link}'
    )
    if stdout:
        return 1, stdout
    return 0, stderr


async def ytdl_(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(command(["ply", "play", "پخش"]) & SUDOERS)
async def play(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    user_id = m.from_user.id
    if replied:
        if replied.audio or replied.voice:
            suhu = await replied.reply("**🔄 درحال پردازش...**")
            dl = await replied.download()
            link = replied.link
            
            try:
                if replied.audio:
                    songname = replied.audio.title[:70]
                    songname = replied.audio.file_name[:70]
                elif replied.voice:
                    songname = "Voice Note"
            except BaseException:
                songname = "Audio"
            
            if chat_id in QUEUE:
                title = songname
                userid = m.from_user.id
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await suhu.delete()
                await m.reply_text(f"**💥 ❰MeTi✘پلیر❱ 💿 جدید 💞 \n🔊 به صف شد 💞در » #{pos} 🌷 ...**",
                )
            else:
                try:
                    title = songname
                    userid = m.from_user.id
                    await suhu.edit("**🔄 درحال پردازش ...**")
                    await aditya.join_group_call(
                        chat_id,
                        AudioPiped(
                            dl,
                            HighQualityAudio(),
                        ),
                        stream_type=StreamType().local_stream,
                    )
                    add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                    await suhu.delete()
                    requester = (
                        f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    )
                    await m.reply_text("**💥 ❰MeTi✘پلیر❱ 💿 [جدید] 💞\n🔊 درحال پخش 😍 𝐎𝐏 🥀 ...**",
                    )
                except Exception as e:
                    await suhu.delete()
                    await m.reply_text(f"🚫 اروررررر:\n\n» {e}")
        else:
            if len(m.command) < 2:
                await m.reply(
                    "**🤖 هدیه 🙃 Aمقداری 💿 پرسو جوA 😍\n💞 به 🔊 Aپخش 🥀 A موزیک 🌷...**"
                )
            else:
                suhu = await c.send_message(chat_id, "**🔎 جستجو ...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                if search == 0:
                    await suhu.edit("**🚫 موزیک پیدا نشد❗...**")
                else:
                    songname = search[0]
                    title = search[0]
                    url = search[1]
                    userid = m.from_user.id
                    coders, ytlink = await ytdl(url)
                    if coders == 0:
                        await suhu.edit(f"**❌مشکلات دانلود شناسایی شد\n\n» `{ytlink}`**")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Audio", 0
                            )
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_text(f"**💥 ❰MeTi✘پلیر❱ 💿 [جدید] 💞 \n🔊 موزیک 💞 در » #{pos} 🌷 ...**",
                            )
                        else:
                            try:
                                await suhu.edit("**🔄 درحال پردازش ...**")
                                await aditya.join_group_call(
                                    chat_id,
                                    AudioPiped(
                                        ytlink,
                                        HighQualityAudio(),
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                                await suhu.delete()
                                requester = (
                                    f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                )
                                await m.reply_text("**💥 ❰MeTi✘پلیر❱ 💿💞\n🔊موزیک جدید 🥀 ...**",
                                )
                            except Exception as ep:
                                await suhu.delete()
                                await m.reply_text(f"🚫 اروررر: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "**🤖 هدیه 🙃 Aمقداری 💿 پرسو جوA 😍\n💞 به 🔊 Aپخش 🥀 A موزیک 🌷...**"
            )
        else:
            suhu = await c.send_message(chat_id, "**🔎 جستجو ...**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await suhu.edit("**🚫 موزیک پیدا نشد❗❗...**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                userid = m.from_user.id
                coders, ytlink = await ytdl(url)
                if coders == 0:
                    await suhu.edit(f"**❌ مشکلات دانلود شناسایی شد𝐝\n\n» `{ytlink}`**")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await suhu.delete()
                        requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        await m.reply_text(f"**💥 ❰MeTi✘پلیر❱ 💿 [جدید] 💞 \n🔊 موزیک 💞 در » #{pos} 🌷 ...**",
                        )
                    else:
                        try:
                            await suhu.edit("**🔄 درحال پردازش ...**")
                            await aditya.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                    HighQualityAudio(),
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_text("**💥 ❰MeTi✘پلیر❱ 💿 [جدید] 💞 \n🔊 موزیک 💞 در »🥀 ...**",
                            )
                        except Exception as ep:
                            await suhu.delete()
                            await m.reply_text(f"🚫 اروررر: `{ep}`")


@Client.on_message(command(["vply", "vplay","ویدیو "]) & SUDOERS)
async def vplay(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    user_id = m.from_user.id
    if replied:
        if replied.video or replied.document:
            loser = await replied.reply("**🔄 درحال پردازش...**")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await loser.edit(
                        "» __فقطA 720, 480, 360مجاز __ \n💡 ** ویدیو جدید با کیفیت 720 پلی داده شد𝐏**"
                    )
            try:
                if replied.video:
                    songname = replied.video.file_name[:70]
                    duration = replied.video.duration
                elif replied.document:
                    songname = replied.document.file_name[:70]
                    duration = replied.document.duration
            except BaseException:
                songname = "Video"

            if chat_id in QUEUE:
                title = songname
                userid = m.from_user.id
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_text(f"**💥 ❰MeTi✘پلیر❱ 💿 [جدید] 💞 \n🔊 موزیک 💞 در »#{pos} 🌷 ...**",
                )
            else:
                title = songname
                userid = m.from_user.id
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                await loser.edit("**🔄 درحال پردازش ...**")
                await aditya.join_group_call(
                    chat_id,
                    AudioVideoPiped(
                        dl,
                        HighQualityAudio(),
                        amaze,
                    ),
                    stream_type=StreamType().local_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_text("**💥  ❰MeTi✘پلیر❱ 💿💞\n🔊موزیک جدید 🥀 ...**",
                )
        else:
            if len(m.command) < 2:
                await m.reply(
                    "**🤖 هدیه 🙃 Aمقداری 💿 پرسو جوA 😍\n💞 به 🔊 Aپخش 🥀 A موزیک 🌷...**"
                )
            else:
                loser = await c.send_message(chat_id, "**🔎 جستجو ...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                Q = 720
                amaze = HighQualityVideo()
                if search == 0:
                    await loser.edit("**🚫 موزیک پیدا نشد❗❗...**")
                else:
                    songname = search[0]
                    title = search[0]
                    url = search[1]
                    userid = m.from_user.id
                    coders, ytlink = await ytdl_(url)
                    if coders == 0:
                        await loser.edit(f"**❌ مشکلات دانلود شناسایی شد\n\n» `{ytlink}`**")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Video", Q
                            )
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_text(f"**💥 ❰MeTi✘پلیر❱ 💿 [جدید] 💞 \n🔊 موزیک 💞 در »#{pos} 🌷 ...**",
                            )
                        else:
                            try:
                                await loser.edit("**🔄 درحال پردازش ...**")
                                await aditya.join_group_call(
                                    chat_id,
                                    AudioVideoPiped(
                                        ytlink,
                                        HighQualityAudio(),
                                        amaze,
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                                await loser.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                await m.reply_text("**💥  ❰MeTi✘پلیر❱ 💿💞\n🔊موزیک جدید 🥀 ...**",
                                )
                            except Exception as ep:
                                await loser.delete()
                                await m.reply_text(f"🚫 ارورررر: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "**🤖 هدیه 🙃 Aمقداری 💿 پرسو جوA 😍\n💞 به 🔊 Aپخش 🥀 A موزیک 🌷...**"
            )
        else:
            loser = await c.send_message(chat_id, "**🔎 جستجو ...**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            amaze = HighQualityVideo()
            if search == 0:
                await loser.edit("**🚫 موزیک پیدا نشد❗❗...**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                userid = m.from_user.id
                coders, ytlink = await ytdl_(url)
                if coders == 0:
                    await loser.edit(f"**❌ مشکلات دانلود شناسایی شد\n\n» `{ytlink}`**")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await loser.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        await m.reply_text(f"**💥 ❰MeTi✘پلیر❱ 💿 [جدید] 💞 \n🔊 موزیک 💞 در »#{pos} 🌷 ...**",
                        )
                    else:
                        try:
                            await loser.edit("**🔄 درحال پردازش ...**")
                            await aditya.join_group_call(
                                chat_id,
                                AudioVideoPiped(
                                    ytlink,
                                    HighQualityAudio(),
                                    amaze,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_text("**💥  ❰MeTi✘پلیر❱ 💿💞\n🔊موزیک جدید 🥀 ...**",
                            )
                        except Exception as ep:
                            await loser.delete()
                            await m.reply_text(f"🚫 ارورررر: `{ep}`")


@Client.on_message(command(["pse", "pause", "توقف"]) & SUDOERS)
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await aditya.pause_stream(chat_id)
            await m.reply(
                f"**▶️ متوقف شد 🌷 ...**"
            )
        except Exception as e:
            await m.reply(f"🚫 **ارورررر:**\n\n`{e}`")
    else:
        await m.reply("**❌ هیچ چیزپخش نمی کند❗...**")


@Client.on_message(command(["rsm", "resume", "ادامه"]) & SUDOERS)
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await aditya.resume_stream(chat_id)
            await m.reply(
                f"**⏸ ادامه یافت 🌷 ...**"
            )
        except Exception as e:
            await m.reply(f"🚫 **ارورررر:**\n\n`{e}`")
    else:
        await m.reply("**❌ هیچ چیزپخش نمی کند❗...**")
        
        
@Client.on_message(command(["skp", "skip","بعدی"]) & SUDOERS)
async def skip(c: Client, m: Message):
    await m.delete()
    user_id = m.from_user.id
    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("**❌ هیچ چیزپخش نمی کند❗...**")
        elif op == 1:
            await m.reply("**🥀لیست پخش خالی , A ربات از\nویس کال خارج میشود ✨...**")
        elif op == 2:
            await m.reply("**🥀 𝐂𝐥𝐞𝐚𝐫𝐢𝐧𝐠 𝐐𝐮𝐞𝐮𝐞, 𝐋𝐞𝐚𝐯𝐢𝐧𝐠\n𝐅𝐫𝐨𝐦 𝐕𝐂 ✨...**")
        else:
            await m.reply("**🥀موزیک بعدی پلی شد 💞 ...**",
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "🗑 **𝐈 𝐚𝐦 𝐑𝐞𝐦𝐨𝐯𝐞𝐝 𝐒𝐨𝐧𝐠 𝐅𝐫𝐨𝐦 𝐐𝐮𝐞𝐮𝐞:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(command(["end", "stp", "اتمام", "stop"]) & SUDOERS)
async def stop(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await aditya.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("**❌ 𝐒𝐭𝐨𝐩𝐩𝐞𝐝 ✨ ...**")
        except Exception as e:
            await m.reply(f"🚫 **ارورررر:**\n\n`{e}`")
    else:
        await m.reply("**❌ هیچ چیزپخش نمی کند❗...**")




__MODULE__ = "Vᴄ Bᴏᴛ"
__HELP__ = f"""
**Yᴏᴜ Cᴀɴ Pʟᴀʏ Mᴜsɪᴄ Oɴ VC**

`.ply .پخش  پخش.  ` - A پخش موزیک 
`.ویدیو    ویدیو.` - A پخش موزیک ویدیو
`.pse` - Pᴀᴜsᴇ Yᴏᴜʀ Mᴜsɪᴄ
`.rsm` - Rᴇsᴜᴍᴇ Yᴏᴜʀ Mᴜsɪᴄ
`.skp` - Sᴋɪᴘ Tᴏ Tʜᴇ Nᴇxᴛ Sᴏɴɢ
`.stp` - Sᴛᴏᴘ Pʟᴀʏɪɴɢ Aɴᴅ Lᴇᴀᴠᴇ
`.sng` - Dᴏᴡɴʟᴏᴀᴅ Sᴏɴɢ Yᴏᴜ Wᴀɴᴛ
`.rld` - Rᴇʟᴏᴀᴅ Yᴏᴜʀ VC Cʟɪᴇɴᴛ

(__.sng Cᴏᴍᴍᴀɴᴅ Nᴏᴛ Aᴠᴀɪʟᴀʙʟᴇ Aᴛ Tʜɪs Mᴏᴍᴇɴᴛ ...__) 
"""
