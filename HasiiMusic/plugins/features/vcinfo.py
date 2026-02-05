from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram.raw import functions

from HasiiMusic import app, db


@app.on_message(filters.command(["vcinfo", "vcmembers"]) & filters.group)
async def vc_info_command(client, message: Message):
    """
    Show information about members currently in the voice chat.
    Displays mute status, volume levels, and screen sharing status.
    """
    chat_id = message.chat.id
    
    # Check if user is admin
    try:
        member = await app.get_chat_member(chat_id, message.from_user.id)
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.reply_text(
                "❌ <b>Admin Only!</b>\n<blockquote>Only administrators can use this command.</blockquote>",
                parse_mode=ParseMode.HTML
            )
    except Exception:
        return await message.reply_text(
            "⚠️ <b>Error checking admin status.</b>",
            parse_mode=ParseMode.HTML
        )
    
    try:
        # Get the assistant client (Pyrogram) for this chat
        userbot = await db.get_client(chat_id)
        if not userbot:
            return await message.reply_text(
                "❌ <b>No assistant found!</b>\n<blockquote>Bot assistant is not available for this chat.</blockquote>",
                parse_mode=ParseMode.HTML
            )
        
        # Get voice chat participants using raw API with pagination
        try:
            # Resolve peer
            peer = await userbot.resolve_peer(chat_id)
            
            # Get full chat to find the group call input
            full_chat = await userbot.invoke(
                functions.channels.GetFullChannel(channel=peer)
            )
            
            if not full_chat.full_chat.call:
                return await message.reply_text(
                    "❌ <b>No active voice chat found!</b>\n<blockquote>There is no ongoing voice chat in this group.</blockquote>",
                    parse_mode=ParseMode.HTML
                )
            
            input_group_call = full_chat.full_chat.call
            
            participants_raw = []
            next_offset = ""
            
            while True:
                res = await userbot.invoke(
                    functions.phone.GetGroupCallParticipants(
                        call=input_group_call,
                        ids=[],
                        sources=[],
                        offset=next_offset,
                        limit=200
                    )
                )
                
                participants_raw.extend(res.participants)
                next_offset = res.next_offset
                
                if not next_offset:
                    break
            
            # Helper class to adapt raw response to existing logic
            class VCParticipant:
                def __init__(self, raw_p):
                    self.user_id = raw_p.peer.user_id
                    self.muted = raw_p.muted
                    self.volume = raw_p.volume if hasattr(raw_p, "volume") and raw_p.volume is not None else 10000
                    # Check for video/presentation usage
                    self.video = getattr(raw_p, "video", False)
                    self.presentation = getattr(raw_p, "presentation", False)
                    self.screen_sharing = self.presentation or self.video

            participants = [VCParticipant(p) for p in participants_raw]

        except Exception as e:
            return await message.reply_text(
                f"❌ <b>Error fetching VC info.</b>\n<blockquote>{str(e)}</blockquote>",
                parse_mode=ParseMode.HTML
            )
        
        if not participants:
            return await message.reply_text(
                "❌ <b>No users found in the voice chat.</b>",
                parse_mode=ParseMode.HTML
            )
        
        # Build the response
        msg_lines = ["🎧 <b>VC Members Info:</b>\n"]
        member_list = []
        
        for p in participants:
            try:
                user = await app.get_users(p.user_id)
                name = user.mention if user else f"<code>{p.user_id}</code>"
            except Exception:
                name = f"<code>{p.user_id}</code>"
            
            # Get status indicators
            mute_status = "🔇" if p.muted else "👤"
            screen_status = "🖥️" if getattr(p, "screen_sharing", False) else ""
            volume_level = getattr(p, "volume", "N/A")
            
            # Build the info line
            info = f"{mute_status} {name} | 🎚️ {volume_level}"
            if screen_status:
                info += f" | {screen_status}"
            
            member_list.append(info)
        
        msg_lines.append("<blockquote>" + "\n".join(member_list) + "</blockquote>")
        msg_lines.append(f"\n👥 <b>Total:</b> {len(participants)}")
        
        await message.reply_text(
            "\n".join(msg_lines),
            parse_mode=ParseMode.HTML
        )
        
    except Exception as e:
        await message.reply_text(
            f"⚠️ <b>Failed to fetch VC info.</b>\n<blockquote>Error: {str(e)}</blockquote>",
            parse_mode=ParseMode.HTML
        )
