# ======================================== IMPORTS ==================================================

import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# ========================================= CONFIGURATION =================================================

API_ID = int(getenv("API_ID")) # Get this value from my.telegram.org/apps

API_HASH = getenv("API_HASH") # Get this value from my.telegram.org/apps

BOT_TOKEN = getenv("BOT_TOKEN") # Get your token from @BotFather on Telegram.

MONGO_DB_URI = getenv("MONGO_DB_URI", None) # Get your mongo url from cloud.mongodb.com

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 10000)) # Duration limit for playing bot on vc

LOGGER_ID = int(getenv("LOGGER_ID", None)) # Chat id of a group for logging bot's activities

OWNER_ID = int(getenv("OWNER_ID", 7403621976)) # Get this value from @MissRose_bot on Telegram by /id

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/SYNTAX_WORLD")

SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/Guppppp_Shuppppp")

# Get your pyrogram v2 session from https://telegram.tools/session-string-generator#pyrogram on Telegram

STRING1 = getenv("STRING_SESSION", None)

STRING2 = getenv("STRING_SESSION2", None)

STRING3 = getenv("STRING_SESSION3", None)

STRING4 = getenv("STRING_SESSION4", None)

STRING5 = getenv("STRING_SESSION5", None)


START_IMG_URL = getenv(
    "START_IMG_URL", "https://files.catbox.moe/v3q694.jpg"
)

PING_IMG_URL = getenv(
    "PING_IMG_URL", "https://files.catbox.moe/rxsc0h.jpg"
)

PLAYLIST_IMG_URL = "https://files.catbox.moe/i493lf.jpg"

STATS_IMG_URL = "https://files.catbox.moe/i0qmgf.jpg"

TELEGRAM_AUDIO_URL = "https://files.catbox.moe/xn98c5.jpg"

TELEGRAM_VIDEO_URL = "https://files.catbox.moe/xn98c5.jpg"

STREAM_IMG_URL = "https://files.catbox.moe/xn98c5.jpg"

SOUNCLOUD_IMG_URL = "https://files.catbox.moe/xn98c5.jpg"

YOUTUBE_IMG_URL = "https://files.catbox.moe/xn98c5.jpg"

SPOTIFY_ARTIST_IMG_URL = "https://files.catbox.moe/xn98c5.jpg"

SPOTIFY_ALBUM_IMG_URL = "https://files.catbox.moe/xn98c5.jpg"

SPOTIFY_PLAYLIST_IMG_URL = "https://files.catbox.moe/xn98c5.jpg"

AUTO_LEAVING_ASSISTANT = bool(getenv("AUTO_LEAVING_ASSISTANT", False)) # Set this to True if you want the assistant to automatically leave chats after an interval

SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", None) # Get this credentials from https://developer.spotify.com/dashboard

SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", None) # Get this credentials from https://developer.spotify.com/dashboard

PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))# Maximum limit for fetching playlist's track from youtube, spotify, apple links.

TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600)) # Telegram audio and video file size limit (in bytes)

TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", 1073741824))# Telegram audio and video file size limit (in bytes)

HEROKU_APP_NAME = getenv("HEROKU_APP_NAME") # Your heroku app name

HEROKU_API_KEY = getenv("HEROKU_API_KEY") # Get it from http://dashboard.heroku.com/account

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/syntaxworldcodes/VIKRANT_MUSIC",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)  # Fill this variable if your upstream repository is private

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}



def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))


if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )

if SUPPORT_CHAT:
    if not re.match("(?:http|https)://", SUPPORT_CHAT):
        raise SystemExit(
            "[ERROR] - Your SUPPORT_CHAT url is wrong. Please ensure that it starts with https://"
        )
