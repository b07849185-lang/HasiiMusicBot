# ==============================================================================
# cleangroups.py - Clean Inactive Groups (Sudo Only)
# ==============================================================================
# This plugin allows sudo users to find and leave inactive groups.
# Helps keep the bot clean by removing it from groups with no recent activity.
#
# Commands:
# - /cleangroups [days] - Find groups inactive for X days (default: 30)
# - /cleangroups check [days] - Only check, don't leave
# - /cleangroups leave [days] - Find and leave inactive groups
#
# Only sudo users can use this command.
# ==============================================================================

import asyncio
from datetime import datetime, timedelta
from pyrogram import filters, types, errors

from HasiiMusic import app, db, logger


@app.on_message(filters.command(["cleangroups"]) & app.sudo_filter)
async def _cleangroups(_, m: types.Message):
    """Find and optionally leave inactive groups."""
    
    # Parse command arguments
    args = m.command[1:] if len(m.command) > 1 else []
    mode = "check"  # Default mode: only check
    days = 30  # Default: 30 days
    
    if len(args) >= 1:
        if args[0] in ["check", "leave"]:
            mode = args[0]
            if len(args) >= 2:
                try:
                    days = int(args[1])
                except ValueError:
                    days = 30
        else:
            try:
                days = int(args[0])
            except ValueError:
                days = 30
    
    if days < 1 or days > 365:
        return await m.reply_text(
            "<blockquote>❌ Please provide a valid number of days (1-365)</blockquote>"
        )
    
    processing = await m.reply_text(
        f"<blockquote>🔍 Checking groups inactive for <b>{days} days</b>...\n"
        f"Mode: <b>{mode.upper()}</b></blockquote>"
    )
    
    try:
        # Get all groups bot is in
        inactive_groups = []
        active_groups = []
        error_groups = []
        checked_count = 0
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Get all chats
        all_chats = await db.get_chats()
        
        for chat_id in all_chats:
            checked_count += 1
            
            # Update progress every 10 groups
            if checked_count % 10 == 0:
                try:
                    await processing.edit_text(
                        f"<blockquote>🔍 Checking groups...\n"
                        f"Checked: {checked_count}/{len(all_chats)}\n"
                        f"Inactive: {len(inactive_groups)}</blockquote>"
                    )
                except Exception:
                    pass
            
            try:
                # Try to get chat info
                chat = await app.get_chat(chat_id)
                
                # Skip if not a group/supergroup
                if chat.type not in [types.ChatType.GROUP, types.ChatType.SUPERGROUP]:
                    continue
                
                # Get recent messages (check last 10 messages)
                try:
                    messages = []
                    async for msg in app.get_chat_history(chat_id, limit=10):
                        messages.append(msg)
                    
                    if not messages:
                        # No messages found, consider inactive
                        inactive_groups.append({
                            "id": chat_id,
                            "title": chat.title,
                            "members": getattr(chat, "members_count", 0),
                            "last_activity": "No messages"
                        })
                    else:
                        # Check last message date
                        last_msg = messages[0]
                        if last_msg.date < cutoff_date:
                            inactive_groups.append({
                                "id": chat_id,
                                "title": chat.title,
                                "members": getattr(chat, "members_count", 0),
                                "last_activity": last_msg.date.strftime("%Y-%m-%d")
                            })
                        else:
                            active_groups.append(chat_id)
                
                except errors.ChatAdminRequired:
                    # Bot is restricted, can't read messages
                    error_groups.append({
                        "id": chat_id,
                        "title": chat.title,
                        "error": "No message access"
                    })
                except Exception as e:
                    error_groups.append({
                        "id": chat_id,
                        "title": chat.title,
                        "error": str(e)[:50]
                    })
                
            except errors.ChannelPrivate:
                # Bot was removed from group
                inactive_groups.append({
                    "id": chat_id,
                    "title": "Removed/Private",
                    "members": 0,
                    "last_activity": "Bot removed"
                })
            except Exception as e:
                error_groups.append({
                    "id": chat_id,
                    "title": "Unknown",
                    "error": str(e)[:50]
                })
            
            # Small delay to avoid flood
            await asyncio.sleep(0.5)
        
        # Generate report
        report = f"<blockquote><u><b>🧹 INACTIVE GROUPS REPORT</b></u>\n\n"
        report += f"<b>Checked:</b> {checked_count} groups\n"
        report += f"<b>Inactive (>{days} days):</b> {len(inactive_groups)}\n"
        report += f"<b>Active:</b> {len(active_groups)}\n"
        report += f"<b>Errors:</b> {len(error_groups)}\n\n"
        
        if mode == "leave" and inactive_groups:
            report += f"<b>🚪 Leaving inactive groups...</b></blockquote>\n\n"
            await processing.edit_text(report)
            
            left_count = 0
            failed_count = 0
            
            for group in inactive_groups[:50]:  # Limit to 50 at a time
                try:
                    await app.leave_chat(group["id"])
                    await db.rm_chat(group["id"])
                    left_count += 1
                    await asyncio.sleep(1)
                except Exception as e:
                    logger.error(f"Failed to leave {group['id']}: {e}")
                    failed_count += 1
            
            report += f"<blockquote><b>✅ Left {left_count} groups</b>\n"
            if failed_count:
                report += f"<b>❌ Failed: {failed_count}</b>\n"
            report += "</blockquote>"
        
        elif inactive_groups:
            report += f"<b>📋 Inactive Groups (showing first 20):</b></blockquote>\n\n"
            
            for i, group in enumerate(inactive_groups[:20], 1):
                report += f"<blockquote>{i}. <b>{group['title']}</b>\n"
                report += f"   ID: <code>{group['id']}</code>\n"
                report += f"   Last Activity: {group['last_activity']}\n"
                report += f"   Members: {group['members']}</blockquote>\n\n"
            
            if len(inactive_groups) > 20:
                report += f"<blockquote>... and {len(inactive_groups) - 20} more</blockquote>\n\n"
            
            report += (
                f"<blockquote><b>To leave these groups, use:</b>\n"
                f"<code>/cleangroups leave {days}</code></blockquote>"
            )
        else:
            report += f"<b>✅ No inactive groups found!</b></blockquote>"
        
        await processing.edit_text(report[:4000])  # Telegram message limit
        
    except Exception as e:
        logger.error(f"Error in cleangroups: {e}", exc_info=True)
        await processing.edit_text(
            f"<blockquote>❌ Error occurred: {str(e)[:200]}</blockquote>"
        )
