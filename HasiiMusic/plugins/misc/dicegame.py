# ==============================================================================
# dicegame.py - Telegram Dice Game Commands
# ==============================================================================
# Fun emoji dice games using Telegram's built-in dice feature.
# Commands: /dice, /dart, /basket, /jackpot, /ball, /football
# Can also be triggered by sending the emoji directly: 🎲, 🎯, 🏀, 🎰, 🎳, ⚽
# ==============================================================================

from pyrogram import filters
from HasiiMusic import app

# Dice 🎲
@app.on_message(filters.command("dice"))
async def roll_dice(bot, message):
    try:
        x = await bot.send_dice(message.chat.id, "🎲")
        m = x.dice.value
        await message.reply_text(f"🎲 Hey {message.from_user.mention}, your score is: {m}", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.regex(r"^🎲$") & filters.text)
async def roll_dice_emoji(bot, message):
    try:
        x = await bot.send_dice(message.chat.id, "🎲")
        m = x.dice.value
        await message.reply_text(f"🎲 Hey {message.from_user.mention}, your score is: {m}", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

# Dart 🎯
@app.on_message(filters.command("dart"))
async def throw_dart(bot, message):
    try:
        x = await bot.send_dice(message.chat.id, "🎯")
        m = x.dice.value
        await message.reply_text(f"🎯 Hey {message.from_user.mention}, your score is: {m}", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.regex(r"^🎯$") & filters.text)
async def throw_dart_emoji(bot, message):
    try:
        x = await bot.send_dice(message.chat.id, "🎯")
        m = x.dice.value
        await message.reply_text(f"🎯 Hey {message.from_user.mention}, your score is: {m}", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

# Basketball 🏀
@app.on_message(filters.command("basket"))
async def shoot_basket(bot, message):
    try:
        x = await bot.send_dice(message.chat.id, "🏀")
        m = x.dice.value
        await message.reply_text(f"🏀 Hey {message.from_user.mention}, your score is: {m}", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.regex(r"^🏀$") & filters.text)
async def shoot_basket_emoji(bot, message):
    try:
        x = await bot.send_dice(message.chat.id, "🏀")
        m = x.dice.value
        await message.reply_text(f"🏀 Hey {message.from_user.mention}, your score is: {m}", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

# Jackpot 🎰
@app.on_message(filters.command("jackpot"))
async def spin_jackpot(bot, message):
    try:
        x = await bot.send_dice(message.chat.id, "🎰")
        m = x.dice.value
        await message.reply_text(f"🎰 Hey {message.from_user.mention}, your score is: {m}", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.regex(r"^🎰$") & filters.text)
async def spin_jackpot_emoji(bot, message):
    try:
        x = await bot.send_dice(message.chat.id, "🎰")
        m = x.dice.value
        await message.reply_text(f"🎰 Hey {message.from_user.mention}, your score is: {m}", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

# Bowling Ball 🎳
@app.on_message(filters.command("ball"))
async def roll_ball(bot, message):
    try:
        x = await bot.send_dice(message.chat.id, "🎳")
        m = x.dice.value
        await message.reply_text(f"🎳 Hey {message.from_user.mention}, your score is: {m}", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.regex(r"^🎳$") & filters.text)
async def roll_ball_emoji(bot, message):
    try:
        x = await bot.send_dice(message.chat.id, "🎳")
        m = x.dice.value
        await message.reply_text(f"🎳 Hey {message.from_user.mention}, your score is: {m}", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

# Football ⚽
@app.on_message(filters.command("football"))
async def kick_football(bot, message):
    try:
        x = await bot.send_dice(message.chat.id, "⚽")
        m = x.dice.value
        await message.reply_text(f"⚽ Hey {message.from_user.mention}, your score is: {m}", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.regex(r"^⚽$") & filters.text)
async def kick_football_emoji(bot, message):
    try:
        x = await bot.send_dice(message.chat.id, "⚽")
        m = x.dice.value
        await message.reply_text(f"⚽ Hey {message.from_user.mention}, your score is: {m}", quote=True)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
