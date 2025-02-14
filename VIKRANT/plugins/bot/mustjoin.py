from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from PURVIMUSIC import app

#--------------------------

MUST_JOIN = "Guppppp_Shuppppp"  # First channel
MUST_JOIN_2 = "SYNTAX_WORLD"  # Second channel
#------------------------

@app.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(app: Client, msg: Message):
    if not MUST_JOIN or not MUST_JOIN_2:
        return
    try:
        try:
            await app.get_chat_member(MUST_JOIN, msg.from_user.id)
            await app.get_chat_member(MUST_JOIN_2, msg.from_user.id)
        except UserNotParticipant:
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + MUST_JOIN
            else:
                chat_info = await app.get_chat(MUST_JOIN)
                link = chat_info.invite_link

            if MUST_JOIN_2.isalpha():
                link2 = "https://t.me/" + MUST_JOIN_2
            else:
                chat_info2 = await app.get_chat(MUST_JOIN_2)
                link2 = chat_info2.invite_link

            try:
                await msg.reply_photo(
                    photo="https://telegra.ph/file/030360ba737587d0fb147.jpg", 
                    caption=f"๏ ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ʏᴏᴜ'ᴠᴇ ɴᴏᴛ ᴊᴏɪɴᴇᴅ [๏sᴜᴘᴘᴏʀᴛ๏]({link}) ᴏʀ [๏ᴀɴᴏᴛʜᴇʀ ᴄʜᴀɴɴᴇʟ๏]({link2}) ʏᴇᴛ, ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜsᴇ ᴍᴇ �ʜᴇɴ ᴊᴏɪɴ ʙᴏᴛʜ ᴄʜᴀɴɴᴇʟs ᴀɴᴅ sᴛᴀʀᴛ ᴍᴇ ᴀɢᴀɪɴ ! ",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("๏Jᴏɪɴ Sᴜᴘᴘᴏʀᴛ๏", url=link),
                                InlineKeyboardButton("๏Jᴏɪɴ Aɴᴏᴛʜᴇʀ Cʜᴀɴɴᴇʟ๏", url=link2),
                            ]
                        ]
                    )
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"๏ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀs ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ᴍᴜsᴛ_Jᴏɪɴ ᴄʜᴀᴛs ๏: {MUST_JOIN} ᴀɴᴅ {MUST_JOIN_2} !")
