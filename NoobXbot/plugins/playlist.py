from youtubesearchpython import VideosSearch
import os
from os import path
import random
import asyncio
import shutil
from time import time
import yt_dlp
from NoobXbot import converter
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.types import Voice
from NoobXbot import (
    app, BOT_USERNAME,
    BOT_ID,
)
from NoobXbot.NoobXUtilities.noobxruns import (
    music,
    convert,
    download,
    clear,
    get,
    is_empty,
    put,
    task_done,
    smexy,
)
from NoobXbot.NoobXUtilities.database.queue import (
    is_active_chat,
    add_active_chat,
    remove_active_chat,
    music_on,
    is_music_playing,
    music_off,
)
from NoobXbot.NoobXUtilities.database.onoff import (is_on_off, add_on, add_off)
from NoobXbot.NoobXUtilities.database.blacklistchat import (
    blacklisted_chats,
    blacklist_chat,
    whitelist_chat,
)
from NoobXbot.NoobXUtilities.database.gbanned import (
    get_gbans_count,
    is_gbanned_user,
    add_gban_user,
    add_gban_user,
)
from NoobXbot.NoobXUtilities.database.playlist import (
    get_playlist_count,
    _get_playlists,
    get_note_names,
    get_playlist,
    save_playlist,
    delete_playlist,
)
from NoobXbot.NoobXUtilities.helpers.inline import (
    play_keyboard,
    confirm_keyboard,
    play_list_keyboard,
    close_keyboard,
    confirm_group_keyboard,
)
from NoobXbot.NoobXUtilities.database.theme import (
    _get_theme,
    get_theme,
    save_theme,
)
from NoobXbot.NoobXUtilities.database.assistant import (
    _get_assistant,
    get_assistant,
    save_assistant,
)
from NoobXbot.config import DURATION_LIMIT, ASS_ID
from NoobXbot.NoobXUtilities.helpers.decorators import errors
from NoobXbot.NoobXUtilities.helpers.filters import command
from NoobXbot.NoobXUtilities.helpers.gets import (
    get_url,
    themes,
    random_assistant,
)
from NoobXbot.NoobXUtilities.helpers.thumbnails import gen_thumb
from NoobXbot.NoobXUtilities.helpers.chattitle import CHAT_TITLE
from NoobXbot.NoobXUtilities.helpers.ytdl import ytdl_opts 
from NoobXbot.NoobXUtilities.helpers.inline import (
    play_keyboard,
    search_markup,
    play_markup,
    playlist_markup,
)
from pyrogram import filters
from typing import Union
from youtubesearchpython import VideosSearch
from pyrogram.types import Message, Audio, Voice
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)


options = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "all","16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",]   


@app.on_message(filters.command("playlist"))
async def pause_cmd(_, message):
    thumb ="cache/IMG_20211129_031406_576.jpg"
    await message.reply_photo(
    photo=thumb, 
    caption=("**__Music's Playlist Feature__**\n\nSelect The Playlist, You want to check!"),    
    reply_markup=play_list_keyboard) 
    return 


@app.on_message(filters.command("delmyplaylist"))
async def pause_cmd(_, message):
    usage = ("Usage:\n\n/delmyplaylist [Numbers between 1-30] ( to delete a particular music in playlist )\n\nor\n\n /delmyplaylist all ( to delete whole playlist )")
    if len(message.command) < 2:
        return await message.reply_text(usage)
    name = message.text.split(None, 1)[1].strip()
    if not name:
        return await message.reply_text(usage)
    if name not in options:
        return await message.reply_text(usage)
    if len(message.text) == 18:
        return await message.reply_text(f"Confirmation!!\nYou sure you want to delete your whole playlist?", reply_markup=confirm_keyboard)
    else:
         _playlist = await get_note_names(message.from_user.id)
    if not _playlist:
        await message.reply_text("You have no Playlist on Music's Server")
    else:
        titlex = []
        j = 0
        count = int(name)
        for note in _playlist:
            j += 1
            _note = await get_playlist(message.from_user.id, note)
            if j == count:
                deleted = await delete_playlist(message.from_user.id, note)
                if deleted:
                    return await message.reply_text(f"**Deleted the {count} music in playlist**")
                else:
                    return await message.reply_text(f"**No such saved music in playlist.**")                                
        await message.reply_text("You have no such music in Playlist.")                             

        
@app.on_message(filters.command("delgroupplaylist"))
async def delgroupplaylist(_, message):
    a = await app.get_chat_member(message.chat.id , message.from_user.id)
    if not a.can_manage_voice_chats:
        return await message.reply_text("I don't have the required permission to perform this action.\n**Permission:** __MANAGE VOICE CHATS__")
    usage = ("Usage:\n\n/delgroupplaylist [Numbers between 1-30] ( to delete a particular music in playlist )\n\nor\n\n /delgroupplaylist all ( to delete whole playlist )")
    if len(message.command) < 2:
        return await message.reply_text(usage)
    name = message.text.split(None, 1)[1].strip()
    if not name:
        return await message.reply_text(usage)
    if name not in options:
        return await message.reply_text(usage)
    if len(message.text) == 21:
        return await message.reply_text(f"Confirmation!!\nYou sure you want to delete whole whole playlist?", reply_markup=confirm_group_keyboard)
    else:
         _playlist = await get_note_names(message.chat.id)
    if not _playlist:
        await message.reply_text("Group has no Playlist on Music's Server")
    else:
        titlex = []
        j = 0
        count = int(name)
        for note in _playlist:
            j += 1
            _note = await get_playlist(message.chat.id, note)
            if j == count:
                deleted = await delete_playlist(message.chat.id, note)
                if deleted:
                    return await message.reply_text(f"**Deleted the {count} music in group's playlist**")
                else:
                    return await message.reply_text(f"**No such saved music in Group playlist.**")                                
        await message.reply_text("You have no such music in Group Playlist.")
