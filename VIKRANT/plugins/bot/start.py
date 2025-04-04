import time
import os
import asyncio
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from pyrogram import filters
from pyrogram.errors import ChannelInvalid
from pyrogram.enums import ChatType, ChatMembersFilter
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch
import config
from VIKRANT import app
from VIKRANT.misc import _boot_
from VIKRANT.plugins.sudo.sudoers import sudoers_list
from VIKRANT.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
    connect_to_chat,
)
from VIKRANT.utils.decorators.language import LanguageStart
from VIKRANT.utils.formatters import get_readable_time
from VIKRANT.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string


async def get_user_profile_pic(client, user_id):
    try:
        photos = await client.get_profile_photos(user_id, limit=1)
        if not photos.photos:
            return "VIKRANT/assets/dp.jpg"
        file_path = await client.download_media(photos.photos[0].file_id, file_name=f"{user_id}.jpg")
        return file_path
    except Exception:
        return "VIKRANT/assets/dp.jpg"


async def get_group_profile_pic(client, chat_id):
    try:
        chat = await client.get_chat(chat_id)
        if chat.photo:
            file_path = await client.download_media(chat.photo.big_file_id, file_name=f"{chat_id}.jpg")
            return file_path
        else:
            return "VIKRANT/assets/dp.jpg"
    except Exception:
        return "VIKRANT/assets/dp.jpg"


def make_glowing_circle_image(input_path, output_path):
    base = Image.open(input_path).convert("RGBA").resize((400, 400))
    mask = Image.new("L", base.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 400, 400), fill=255)
    base.putalpha(mask)

    glow = base.copy().filter(ImageFilter.GaussianBlur(15))
    glow = ImageOps.expand(glow, border=30, fill=(255, 0, 90, 100))

    background = Image.new("RGBA", glow.size, (15, 15, 30, 255))
    background.paste(glow, (0, 0), glow)
    background.paste(base, (30, 30), base)

    background.save(output_path)


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)

    typing_message = await message.reply("<b>ᵤɪɴɢ..ᵤɔɴɢ..❤️‍🔥</b>")
    typing_text = "<b>ᵉᴅᴀʀᴛɪɴɢ...❤️‍🔥</b>"
    for i in range(1, len(typing_text) + 1):
        try:
            await typing_message.edit_text(typing_text[:i])
            await asyncio.sleep(0.001)
        except Exception as e:
            print(f"Error while editing message: {e}")

    await asyncio.sleep(2)
    await typing_message.delete()

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:3] == "del":
            await del_plist_msg(client=client, message=message, _=_)
        elif name[0:4] == "help":
            keyboard = help_pannel(_)
            return await message.reply_photo(
                photo=config.START_IMG_URL,
                caption=_['help_1'].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )
        elif name[:8] == "connect_":
            chat_id = name[8:]
            try:
                title = (await app.get_chat(chat_id)).title
            except ChannelInvalid:
                return await message.reply_text(f"ʟɔɔʟ ʟɪɐɛ ɪ ᴀᴍ ɴɔᴛ ɐɴ ɐɟᴍɪɴ ɔᴏ ʁɪᴇ ɐᴅ {chat_id}")

            admin_ids = [member.user.id async for member in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS)]
            if message.from_user.id not in admin_ids:
                return await message.reply_text(f"sɔʀʀʀʀʀʀʀy sɪʀ ʃʌʋ ɪ ʁᴛɪɴɪɴɢ ʁɪɐᴛ ʏɔᴜ ɴɔᴛ ɐɴ ɐɟᴍɪɴ ɔᴏ {title}")
            a = await connect_to_chat(message.from_user.id, chat_id)
            return await message.reply_text(f"ʏɔᴜ ɐʀᴇ ɴɔᴛ ᴄɔɴɴᴇᴄᴇɐ ᴛɔ {title}" if a else a)

        elif name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴟʀʀ ʏʏʀᴛ ᴝᴀʀᴛᴇᴅ ᴝʀᴇ ʀʀʀ ʀʀʀ ʀʀʀ <b>sᴜᴅᴏʟɪᴛ</b>.

<b>ᴜᴄᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>
<b>ᴜᴄᴇʀɴɐᴛᴇ :</b> @{message.from_user.username}",
                )
            return

        elif name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(text=_["S_B_8"], url=link),
                    InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                ]]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴟʀʀ ʏʏʀᴛ ᴝᴀʀᴇᴅ ᴝʀᴇ ʀʀʀ ʀʀʀ ʀʀʀ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍɐᴛɪᴏɴ</b>.

<b>ᴜᴄᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>
<b>ᴜᴄᴇʀɴɐᴛᴇ :</b> @{message.from_user.username}",
                )
    else:
        pp_path = await get_user_profile_pic(client, message.from_user.id)
        final_pp = f"{message.from_user.id}_start.jpg"
        make_glowing_circle_image(pp_path, final_pp)
        out = private_panel(_)
        await message.reply_photo(
            photo=final_pp,
            caption=_['start_2'].format(message.from_user.mention, app.mention),
            reply_markup=InlineKeyboardMarkup(out),
        )
        if await is_on_off(2):
            return await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"{message.from_user.mention} ᴊᴟʀʀ ʏʏʀᴛᴇᴅ ᴝʀᴇ ʀʀʀ ʀʀʀ ʀʀʀ.

<b>ᴜᴄᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>
<b>ᴜᴄᴇʀɴɐᴛᴇ :</b> @{message.from_user.username}",
            )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    pp_path = await get_group_profile_pic(client, message.chat.id)
    final_pp = f"{message.chat.id}_group.jpg"
    make_glowing_circle_image(pp_path, final_pp)

    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        photo=final_pp,
        caption=_['start_1'].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)
