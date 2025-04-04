import time
import os
import asyncio
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import config
from VIKRANT import app
from VIKRANT.misc import _boot_
from VIKRANT.utils.database import add_served_chat, add_served_user, is_banned_user, is_on_off
from VIKRANT.utils.decorators.language import LanguageStart
from VIKRANT.utils.formatters import get_readable_time
from VIKRANT.utils.inline import private_panel, start_panel
from config import BANNED_USERS
from strings import get_string


async def get_user_profile_pic(client, user_id):
    try:
        user = await client.get_users(user_id)  
        photos = client.get_chat_photos(user.id)  # Returns async generator
        
        async for photo in photos:  # Iterate properly
            file_path = await client.download_media(photo.file_id, file_name=f"{user_id}.jpg")
            return file_path

        print(f"[LOG] No profile photo for {user_id}, using default.")
        return "VIKRANT/assets/dp.jpg"

    except Exception as e:
        print(f"[ERROR] Failed to get profile photo for {user_id}: {e}")
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

    background = background.convert("RGB")  # Fix: Convert to RGB before saving as JPEG
    background.save(output_path, "JPEG")


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)

    typing_message = await message.reply("<b>Loading... 🔥</b>")
    await asyncio.sleep(2)
    await typing_message.delete()

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
            text=f"{message.from_user.mention} started the bot.\n\n"
                 f"**User ID:** <code>{message.from_user.id}</code>\n"
                 f"**Username:** @{message.from_user.username}",
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


