import requests
from datetime import datetime
from pyrogram import filters, Client
from AdityaHalder.utilities.misc import SUDOERS
# ping checker

@Client.on_message(filters.command(["ping"], ["/", ".", "پینگ", "!"]) & SUDOERS)
async def ping(Client, message):
    start = datetime.now()
    loda = await message.reply_text("**» نابغه**")
    end = datetime.now()
    mp = (end - start).microseconds / 1000
    await loda.edit_text(f"**🤖 پینگ \n»** `{mp} ms`")


__MODULE__ = "پینگ"
__HELP__ = f"""
**🥀 برای دریافت سرعت ربات.**

`.ping  .پینگ  پینگ.` - **A+ برای چک کردن سرعت دستور**
"""
