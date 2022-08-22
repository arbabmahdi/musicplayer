from pyrogram import filters
from pyrogram.types import Message

from AdityaHalder.config import MONGO_DB_URL, OWNER_ID

from AdityaHalder.modules.clientbot.clientbot import client as app
from AdityaHalder.modules.helpers.command import commandpro
from AdityaHalder.utilities.misc import SUDOERS
from AdityaHalder.utilities.utils import add_sudo, remove_sudo



@app.on_message(
    commandpro([".addsudo", "مدیر"]) & filters.user(OWNER_ID)
)
async def useradd(client, message: Message):
    if MONGO_DB_URL is None:
        return await message.reply_text(
            "**به دلیل مشکلات حریم خصوصی ربات، وقتی از پایگاه داده Yukki استفاده می کنید، نمی توانید کاربران sudo را مدیریت کنید.\n\n لطفاً برای استفاده از این ویژگی، MONGO_DB_URI خود را در vars خود پر کنید**"
        )
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text("به پیام یک کاربر پاسخ دهید یا نام کاربری بدهید/user_id.")
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id in SUDOERS:
            return await message.reply_text(
                "{0} قبلاً یک کاربر sudo است.".format(user.mention)
            )
        added = await add_sudo(user.id)
        if added:
            SUDOERS.add(user.id)
            await message.reply_text("Added **{0}** to Sudo Users.".format(user.mention))
        else:
            await message.reply_text("Failed")
        return
    if message.reply_to_message.from_user.id in SUDOERS:
        return await message.reply_text(
            "{0} قبلاً یک کاربر sudo استr.".format(
                message.reply_to_message.from_user.mention
            )
        )
    added = await add_sudo(message.reply_to_message.from_user.id)
    if added:
        SUDOERS.add(message.reply_to_message.from_user.id)
        await message.reply_text(
            "Added **{0}** to Sudo Users.".format(
                message.reply_to_message.from_user.mention
            )
        )
    else:
        await message.reply_text("Failed")
    return


@app.on_message(
    commandpro([".delsudo","حذف مدیر"]) & filters.user(OWNER_ID)
)
async def userdel(client, message: Message):
    if MONGO_DB_URL is None:
        return await message.reply_text(
            "**به دلیل مشکلات حریم خصوصی ربات، وقتی از پایگاه داده Yukki استفاده می کنید، نمی توانید کاربران sudo را مدیریت کنید.\n\n لطفاً برای استفاده از این ویژگی، MONGO_DB_URI خود را در vars خود پر کنید**"
        )
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text("Reply to a user's message or give username/user_id.")
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id not in SUDOERS:
            return await message.reply_text("Not a part of Bot's Sudo.")
        removed = await remove_sudo(user.id)
        if removed:
            SUDOERS.remove(user.id)
            await message.reply_text("Removed from Bot's Sudo User")
            return
        await message.reply_text(f"Something wrong happened.")
        return
    user_id = message.reply_to_message.from_user.id
    if user_id not in SUDOERS:
        return await message.reply_text("Not a part of Bot's Sudo.")
    removed = await remove_sudo(user_id)
    if removed:
        SUDOERS.remove(user_id)
        await message.reply_text("Removed from Bot's Sudo User")
        return
    await message.reply_text(f"Something wrong happened.")


@app.on_message(commandpro([".sudousers", ".sudolist"]) & SUDOERS)
async def sudoers_list(client, message: Message):
    text = "⭐️<u> **Owners:**</u>\n"
    count = 0
    for x in OWNER_ID:
        try:
            user = await app.get_users(x)
            user = (
                user.first_name if not user.mention else user.mention
            )
            count += 1
        except Exception:
            continue
        text += f"{count}➤ {user}\n"
    smex = 0
    for user_id in SUDOERS:
        if user_id not in OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user = (
                    user.first_name
                    if not user.mention
                    else user.mention
                )
                if smex == 0:
                    smex += 1
                    text += "\n⭐️<u> **Sudo Users:**</u>\n"
                count += 1
                text += f"{count}➤ {user}\n"
            except Exception:
                continue
    if not text:
        await message.reply_text("No Sudo Users")
    else:
        await message.reply_text(text)



__MODULE__ = "Sᴜᴅᴏ"
__HELP__ = f"""
**🇮🇳 Sᴜᴅᴏ Usᴇʀs Cᴏɴᴛʀᴏʟᴇʀ :**

`.addsudo` - **Aᴅᴅ Aɴ Usᴇʀ Tᴏ Sᴜᴅᴏ Usᴇʀ**

`.delsudo` - **Rᴇᴍᴏᴠᴇ Aɴ Usᴇʀ Fʀᴏᴍ Sᴜᴅᴏ Usᴇʀ**

`.sudolist` - **Gᴇᴛ A Lɪsᴛ Oғ Aʟʟ Sᴜᴅᴏ Usᴇʀs**
"""
