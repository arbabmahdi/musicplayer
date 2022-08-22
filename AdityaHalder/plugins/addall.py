import asyncio
from pyrogram import Client, filters 
from pyrogram.types import Message
from AdityaHalder.modules.helpers.basics import edit_or_reply
from AdityaHalder.modules.helpers.filters import command
from AdityaHalder.modules.helpers.command import commandpro
from AdityaHalder.utilities.misc import SUDOERS


@Client.on_message(command(["addall", "inviteall"]) & SUDOERS)
async def inviteall(client: Client, message: Message):
    kaal = await edit_or_reply(message, "در حال پردازش ...")
    text = message.text.split(" ", 1)
    queryy = text[1]
    chat = await client.get_chat(queryy)
    tgchat = message.chat
    await kaal.edit_text(f"**🥀دعوت از کاربران از {chat.username} ✨ ...**")
    async for member in client.iter_chat_members(chat.id):
        user= member.user
        kal= ["online", "offline" , "recently", "within_week"]
        if user.status in kal:
           try:
            await client.add_chat_members(tgchat.id, user.id)
           except Exception as e:
            mg= await client.send_message("me", f"error-   {e}")
            await asyncio.sleep(0.3)
            await mg.delete()



__MODULE__ = "Aᴅᴅ Aʟʟ"
__HELP__ = f"""
`.addall [@groupusername]` **-از این دستور برای افزودن اعضا به چت خود استفاده کنید**

**سابق:-** `.addall @COALW`
"""
