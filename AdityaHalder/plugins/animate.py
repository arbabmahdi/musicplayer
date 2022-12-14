import asyncio
import random
from pyrogram import *
from pyrogram.types import *
from AdityaHalder.modules.helpers.filters import command
from AdityaHalder.modules.helpers.command import commandpro
from AdityaHalder.modules.helpers.basics import edit_or_reply
from AdityaHalder.modules.helpers.decorators import errors, sudo_users_only
from pyrogram.errors.exceptions.flood_420 import FloodWait
from AdityaHalder.utilities.misc import SUDOERS



R = "โค๏ธ"
W = "๐ค"

heart_list = [
    W * 9,
    W * 2 + R * 2 + W + R * 2 + W * 2,
    W + R * 7 + W,
    W + R * 7 + W,
    W + R * 7 + W,
    W * 2 + R * 5 + W * 2,
    W * 3 + R * 3 + W * 3,
    W * 4 + R + W * 4,
    W * 9,
]
joined_heart = "\n".join(heart_list)
heartlet_len = joined_heart.count(R)
SLEEP = 0.1


async def _wrap_edit(message, text: str):
    """Floodwait-safe utility wrapper for edit"""
    try:
        await message.edit(text)
    except FloodWait as fl:
        await asyncio.sleep(fl.x)


async def phase1(message):
    """Big scroll"""
    BIG_SCROLL = "๐งก๐๐๐๐๐ค๐ค"
    await _wrap_edit(message, joined_heart)
    for heart in BIG_SCROLL:
        await _wrap_edit(message, joined_heart.replace(R, heart))
        await asyncio.sleep(SLEEP)


async def phase2(message):
    """Per-heart randomiser"""
    ALL = ["โค๏ธ"] + list("๐งก๐๐๐๐๐ค๐ค")  # don't include white heart

    format_heart = joined_heart.replace(R, "{}")
    for _ in range(5):
        heart = format_heart.format(*random.choices(ALL, k=heartlet_len))
        await _wrap_edit(message, heart)
        await asyncio.sleep(SLEEP)


async def phase3(message):
    """Fill up heartlet matrix"""
    await _wrap_edit(message, joined_heart)
    await asyncio.sleep(SLEEP * 2)
    repl = joined_heart
    for _ in range(joined_heart.count(W)):
        repl = repl.replace(W, R, 1)
        await _wrap_edit(message, repl)
        await asyncio.sleep(SLEEP)


async def phase4(message):
    """Matrix shrinking"""
    for i in range(7, 0, -1):
        heart_matrix = "\n".join([R * i] * i)
        await _wrap_edit(message, heart_matrix)
        await asyncio.sleep(SLEEP)


@Client.on_message(command(["hearts", "ููุจ"]) & filters.me)
async def hearts(client: Client, message: Message):
    await phase1(message)
    await asyncio.sleep(SLEEP * 3)
    await message.edit("**โค๏ธ I**")
    await asyncio.sleep(0.5)
    await message.edit("**โค๏ธ I Love**")
    await asyncio.sleep(0.5)
    await message.edit("**โค๏ธ I Love You**")
    await asyncio.sleep(3)
    await message.edit("**โค๏ธ I Love You <3**")


@Client.on_message(command(["emoji" , "ุง?ููุฌ?"])& SUDOERS)
async def hello_world(client: Client, message: Message):
    mg = await edit_or_reply(message, "๐")
    await asyncio.sleep(1)
    await mg.edit("๐")
    await asyncio.sleep(1)
    await mg.edit("๐")
    await asyncio.sleep(1) 
    await mg.edit("๐")
    await asyncio.sleep(1) 
    await mg.edit("๐")
    await asyncio.sleep(1) 
    await mg.edit("๐ฅฐ") 
    await asyncio.sleep(1) 
    await mg.edit("๐") 
    await asyncio.sleep(1) 
    await mg.edit("๐คฉ")
    await asyncio.sleep(1) 
    await mg.edit("๐")
    await asyncio.sleep(1) 
    await mg.edit("๐")
    await asyncio.sleep(1) 
    await mg.edit("๐")
    await asyncio.sleep(1) 
    await mg.edit("๐คช")
    await asyncio.sleep(1) 
    await mg.edit("๐")
    await asyncio.sleep(1) 
    await mg.edit("๐ค")
    await asyncio.sleep(1) 
    await mg.edit("๐คญ")
    await asyncio.sleep(1) 
    await mg.edit("๐ฅณ")
    await asyncio.sleep(1) 
    await mg.edit("๐")
    await asyncio.sleep(1) 
    await mg.edit("๐")
    

__MODULE__ = "ุณุฑฺฏุฑู?"
__HELP__ = f"""
**ุณุฑฺฏุฑู?  :**

`.emoji .ุง?ููุฌ?   ุง?ููุฌ.` - **a ุชุบ??ุฑ ูพุดุช ุณุฑ ูู ุง?ููุฌ? *
`.heart  .ููุจ   ููุจ. - ** A+ ุชุบ??ุฑ ุง?ููุฌ? ููุจ **
"""
