import asyncio
from pyrogram import filters, Client
from pyrogram.methods import messages
from AdityaHalder.modules.helpers.filters import command
from AdityaHalder.modules.helpers.program import get_arg, denied_users
import AdityaHalder.modules.databases.pmpermit_db as Kaal

FLOOD_CTRL = 0
ALLOWED = []
USERS_AND_WARNS = {}


@Client.on_message(command(["pmguard", "انتیپیم"]) & filters.me)
async def antipm(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**من فقط روشن یا خاموش را می فهمم**")
        return
    if arg == "off":
        await Kaal.set_pm(False)
        await message.edit("**PM Guard غیرفعال شد**")
    if arg == "on":
        await Kaal.set_pm(True)
        await message.edit("**PM Guard فعال شد**")




@Client.on_message(command(["setlimit", "تعیین حد"]) & filters.me)
async def pmguard(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**تعیین حد برای چه؟**")
        return
    await Kaal.set_limit(int(arg))
    await message.edit(f"**محدودیت تنظیم شده است {arg}**")


@Client.on_message(command("setpmmsg") & filters.me)
async def setpmmsg(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**چه پیامی تنظیم کنیم**")
        return
    if arg == "default":
        await Kaal.set_permit_message(Kaal.PMPERMIT_MESSAGE)
        await message.edit("**پیام Anti_PM روی پیش‌فرض تنظیم شد**.")
        return
    await Kaal.set_permit_message(f"`{arg}`")
    await message.edit("**مجموعه سفارشی پیام ضد ظهر**")


@Client.on_message(command(["setblockmsg" , "بلاک مسیج"]) & filters.me)
async def setblkmsg(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**چه پیامی تنظیم کنیم**")
        return
    if arg == "default":
        await Kaal.set_block_message(Kaal.BLOCKED)
        await message.edit("**مسدود کردن پیام روی پیش‌فرض تنظیم شده است**.")
        return
    await Kaal.set_block_message(f"`{arg}`")
    await message.edit("**مجموعه پیام بلاک سفارشی**")


@Client.on_message(command(["allow", "ap", "approve", "اجازه"]) & filters.me & filters.private)
async def allow(client, message):
    chat_id = message.chat.id
    pmpermit, pm_message, limit, block_message = await Kaal.get_pm_settings()
    await Kaal.allow_user(chat_id)
    await message.edit(f"**من اجازه داده ام [kE تو ](tg://user?id={chat_id}) به من پیام بدی.**")
    async for message in app.search_messages(
        chat_id=message.chat.id, query=pm_message, limit=1, from_user="me"
    ):
        await message.delete()
    USERS_AND_WARNS.update({chat_id: 0})


@Client.on_message(command(["deny", "انکار", "dap", "disapprove", "dapp"]) & filters.me & filters.private)
async def deny(client, message):
    chat_id = message.chat.id
    await Kaal.deny_user(chat_id)
    await message.edit(f"**من اجازه داده ام [kE تو ](tg://user?id={chat_id}) به من پیام بدی.**")


@Client.on_message(
    filters.private
    & filters.create(denied_users)
    & filters.incoming
    & ~filters.service
    & ~filters.me
    & ~filters.bot
)
async def reply_pm(app: Client, message):
    global FLOOD_CTRL
    pmpermit, pm_message, limit, block_message = await Kaal.get_pm_settings()
    user = message.from_user.id
    user_warns = 0 if user not in USERS_AND_WARNS else USERS_AND_WARNS[user]
    if user_warns <= limit - 2:
        user_warns += 1
        USERS_AND_WARNS.update({user: user_warns})
        if not FLOOD_CTRL > 0:
            FLOOD_CTRL += 1
        else:
            FLOOD_CTRL = 0
            return
        async for message in app.search_messages(
            chat_id=message.chat.id, query=pm_message, limit=1, from_user="me"
        ):
            await message.delete()
        await message.reply(pm_message, disable_web_page_preview=True)
        return
    await message.reply(block_message, disable_web_page_preview=True)
    await app.block_user(message.chat.id)
    USERS_AND_WARNS.update({user: 0})




__MODULE__ = "انتی پیام "
__HELP__ = f""" این ماژول فقط برای صاحب ربات

`.pmguard [on or off]` - روشن یا خاموش بودن  Aɴᴛɪ-Pᴍ

`.setpmmsg [message or default]` - تنظیم پیشفرض Pᴍ Mᴇssᴀɢᴇ

`.setblockmsg [message or default]` - تنظیم پیشفرض Bʟᴏᴄᴋ Mᴇssᴀɢᴇ

`.setlimit [value]` - تنظیم بیشترین Pᴍ Mᴇssᴀɢᴇ Lɪᴍɪᴛ.
Ex:- `.setlimit 3` [ولوم  پیشقرض  - 5]

`.a/.allow` - تایید یک کاربر برای پیام

`.da/.deny` - دیس-تایید یک کاربر برای پیام

**نکته:**
-Sᴜᴅᴏ Usᴇʀ Cᴀɴ'ᴛ Cᴏɴᴛʀᴏʟ Tʜɪs Pʟᴜɢɪɴ
"""
