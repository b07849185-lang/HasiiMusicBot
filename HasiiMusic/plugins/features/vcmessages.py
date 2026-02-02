from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatType, ParseMode
from pyrogram.errors import ChatSendPlainForbidden, ChatWriteForbidden, Forbidden, ChannelPrivate

from HasiiMusic import app


async def _safe_reply_text(message: Message, text: str):
    """Safely send reply text with error handling"""
    chat = getattr(message, "chat", None)
    if not chat or chat.type == ChatType.CHANNEL:
        return
    try:
        await message.reply_text(text, parse_mode=ParseMode.HTML)
    except (ChatSendPlainForbidden, ChatWriteForbidden, Forbidden, ChannelPrivate):
        pass
    except Exception:
        pass


@app.on_message(filters.video_chat_started & filters.group)
async def on_voice_chat_started(_, message: Message):
    """Handler for voice chat started event"""
    await _safe_reply_text(message, "🎙 <b>ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ʜᴀs sᴛᴀʀᴛᴇᴅ!</b>")


@app.on_message(filters.video_chat_ended & filters.group)
async def on_voice_chat_ended(_, message: Message):
    """Handler for voice chat ended event"""
    await _safe_reply_text(message, "🔕 <b>ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴇɴᴅᴇᴅ.</b>")


@app.on_message(filters.video_chat_members_invited & filters.group)
async def on_voice_chat_members_invited(_, message: Message):
    """Handler for when members are invited to voice chat"""
    inviter = "Someone"
    if message.from_user:
        try:
            inviter = message.from_user.mention
        except Exception:
            inviter = message.from_user.first_name or "Someone"

    invited = []
    vcmi = getattr(message, "video_chat_members_invited", None)
    users = getattr(vcmi, "users", []) if vcmi else []
    
    for user in users:
        try:
            name = user.first_name or "User"
            invited.append(f"<a href='tg://user?id={user.id}'>{name}</a>")
        except Exception:
            continue

    if invited:
        await _safe_reply_text(
            message,
            f"👥 {inviter} <b>ɪɴᴠɪᴛᴇᴅ</b> {', '.join(invited)} <b>ᴛᴏ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.</b> 😉",
        )
